#!/usr/bin/env python3
"""Build clean, reproducible zip/tar artifacts of the winroot skeleton.

Packaged content is the directory skeleton (including empty directories,
written as explicit archive members) plus the documents. Git/CI/editor
metadata, keeper placeholders, tool caches and OS noise are excluded, so
an extracted artifact is ready to use.

All CI files live under .ci. The repository root is read, never written.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

CI_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = CI_DIR.parent
DEFAULT_OUT_DIR = CI_DIR / "dist"

KEEPER_BLOCK = re.compile(rb"(?m)^# Git Keeper\r?\n\*\r?\n!\.gitignore\r?$")
SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")

EXCLUDED_DIRS = frozenset({".git", ".github", ".ci", ".vscode", ".pixi"})
CACHE_DIRS = frozenset({"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"})
EXCLUDED_FILES = frozenset({".ds_store", "thumbs.db", "desktop.ini"})
EXCLUDED_SUFFIXES = (".pyc", ".pyo")

REPARSE_BIT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
DEFAULT_EPOCH = 315532800       # 1980-01-01 00:00:00 UTC, zip lower bound
MAX_EPOCH = 4354819199          # 2107-12-31 23:59:59 UTC, zip upper bound
FORMAT_SUFFIX = {"zip": ".zip", "tar": ".tar", "tar.gz": ".tar.gz"}


class PackError(Exception):
    pass


@dataclass(frozen=True)
class Entry:
    rel: str
    path: Path
    is_dir: bool


@dataclass
class Plan:
    source: Path
    root_name: str
    artifact_name: str
    epoch: int
    entries: List[Entry]
    skipped: Dict[str, List[str]]


def is_reparse(st: os.stat_result) -> bool:
    return stat.S_ISLNK(st.st_mode) or bool(
        getattr(st, "st_file_attributes", 0) & REPARSE_BIT
    )


def out_relative(source: Path, out_dir: Path) -> Optional[str]:
    try:
        rel = out_dir.relative_to(source).as_posix()
    except ValueError:
        return None
    return None if rel == "." else rel


def validate_out_dir(source: Path, out_dir: Path) -> None:
    try:
        source.relative_to(out_dir)
    except ValueError:
        return
    raise PackError("output directory must not be the source root or one of its parents")


def exclusion_reason(name: str, rel: str, path: Path, is_dir: bool,
                     out_rel: Optional[str]) -> Optional[str]:
    lower = name.lower()
    if is_dir and lower in EXCLUDED_DIRS:
        return "git/ci/editor metadata"
    if is_dir and lower in CACHE_DIRS:
        return "tool cache"
    if rel == out_rel:
        return "build output"
    if lower == ".gitkeeper":
        return "keeper placeholder"
    if lower == ".gitignore":
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise PackError(f"cannot read {path}: {exc}") from exc
        if KEEPER_BLOCK.search(data):
            return "keeper .gitignore"
        return None
    if lower in EXCLUDED_FILES:
        return "OS noise"
    if lower.endswith(EXCLUDED_SUFFIXES):
        return "bytecode"
    return None


def collect(source: Path, out_dir: Path) -> Tuple[List[Entry], Dict[str, List[str]]]:
    src = source.resolve()
    if not src.is_dir():
        raise PackError(f"source is not a directory: {src}")
    if is_reparse(src.lstat()):
        raise PackError("the source root is a reparse point")
    out_rel = out_relative(src, out_dir)
    entries: List[Entry] = []
    skipped: Dict[str, List[str]] = {}

    def walk(folder: Path, rel: str) -> None:
        try:
            with os.scandir(folder) as it:
                items = sorted(it, key=lambda d: d.name.casefold())
        except OSError as exc:
            raise PackError(f"cannot list {folder}: {exc}") from exc
        for item in items:
            child = Path(item.path)
            try:
                st = item.stat(follow_symlinks=False)
            except OSError as exc:
                raise PackError(f"cannot stat {child}: {exc}") from exc
            if is_reparse(st):
                raise PackError(f"reparse points and symbolic links are not allowed: {child}")
            is_dir = stat.S_ISDIR(st.st_mode)
            is_file = stat.S_ISREG(st.st_mode)
            if not (is_dir or is_file):
                raise PackError(f"unsupported special file: {child}")
            child_rel = f"{rel}/{item.name}" if rel else item.name
            reason = exclusion_reason(item.name, child_rel, child, is_dir, out_rel)
            if reason:
                skipped.setdefault(reason, []).append(child_rel + ("/" if is_dir else ""))
                continue
            entries.append(Entry(child_rel, child, is_dir))
            if is_dir:
                walk(child, child_rel)

    walk(src, "")
    return entries, skipped


def validate_component(value: str, label: str) -> None:
    if not SAFE_NAME.fullmatch(value):
        raise PackError(f"invalid {label}: {value!r} (ASCII letters, digits, '.', '_', '-' only)")


def resolve_epoch(value: Optional[int]) -> int:
    raw = value if value is not None else os.environ.get("SOURCE_DATE_EPOCH")
    if raw is None or str(raw).strip() == "":
        return DEFAULT_EPOCH
    try:
        epoch = int(raw)
    except (TypeError, ValueError) as exc:
        raise PackError(f"invalid epoch: {raw!r}") from exc
    if epoch < DEFAULT_EPOCH:
        print("[pack] WARNING: epoch before 1980, clamped to 1980-01-01", file=sys.stderr)
        epoch = DEFAULT_EPOCH
    if epoch > MAX_EPOCH:
        raise PackError("epoch exceeds the zip timestamp limit (2107)")
    return epoch


def warn_if_git_dirty(source: Path) -> None:
    """Warn, never fail, when the source working tree is not clean."""
    if not (source / ".git").exists():
        return

    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(source), *args],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", check=False,
        )

    try:
        status = git("status", "--porcelain=v1", "--untracked-files=all",
                     "--ignore-submodules=none")
        stash = git("stash", "list")
    except OSError as exc:
        print(f"WARNING: cannot check git cleanliness (git unavailable): {exc}",
              file=sys.stderr)
        return
    if status.returncode != 0:
        print(f"WARNING: cannot check git cleanliness: {status.stderr.strip()}",
              file=sys.stderr)
        return
    changed = len([line for line in status.stdout.splitlines() if line.strip()])
    if stash.returncode != 0:
        print("WARNING: cannot check git stash list", file=sys.stderr)
        stashed = 0
    else:
        stashed = len([line for line in stash.stdout.splitlines() if line.strip()])
    if not changed and not stashed:
        return
    print(f"WARNING: git is not clean ({changed} changed/untracked entries, "
          f"{stashed} stash entries); the artifact reflects the current working "
          "tree, not a committed snapshot.", file=sys.stderr)


def make_plan(args: argparse.Namespace) -> Plan:
    source = args.source.resolve()
    out_dir = args.out_dir.resolve()
    validate_out_dir(source, out_dir)
    root_name = source.name if args.root_name is None else args.root_name
    if root_name:
        validate_component(root_name, "root name")
    artifact_name = args.artifact_name or (root_name or source.name)
    validate_component(artifact_name, "artifact name")
    epoch = resolve_epoch(args.epoch)
    warn_if_git_dirty(source)
    entries, skipped = collect(source, out_dir)
    return Plan(source, root_name, artifact_name, epoch, entries, skipped)


def arc_name(rel: str, root_name: str) -> str:
    return f"{root_name}/{rel}" if root_name else rel


def expected_members(plan: Plan) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    if plan.root_name:
        result[plan.root_name] = True
    for entry in plan.entries:
        result[arc_name(entry.rel, plan.root_name)] = entry.is_dir
    return result


def hash_stream(stream) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1 << 20), b""):
        digest.update(chunk)
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    with open(path, "rb") as stream:
        return hash_stream(stream)


def build_digests(plan: Plan) -> Dict[str, str]:
    return {
        arc_name(entry.rel, plan.root_name): sha256_file(entry.path)
        for entry in plan.entries if not entry.is_dir
    }


def zip_info(name: str, is_dir: bool, epoch: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name + "/" if is_dir else name, time.gmtime(epoch)[:6])
    info.create_system = 3
    info.create_version = 20
    info.extract_version = 20
    if is_dir:
        info.external_attr = (0o40755 << 16) | 0x10
        info.compress_type = zipfile.ZIP_STORED
    else:
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
    return info


def write_zip(path: Path, plan: Plan, level: int) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=level, allowZip64=True) as zf:
        if plan.root_name:
            zf.writestr(zip_info(plan.root_name, True, plan.epoch), b"")
        for entry in plan.entries:
            name = arc_name(entry.rel, plan.root_name)
            if entry.is_dir:
                zf.writestr(zip_info(name, True, plan.epoch), b"")
            else:
                with open(entry.path, "rb") as src, \
                        zf.open(zip_info(name, False, plan.epoch), "w") as dst:
                    shutil.copyfileobj(src, dst, 1 << 20)


def tar_info(name: str, is_dir: bool, size: int, epoch: int) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.type = tarfile.DIRTYPE if is_dir else tarfile.REGTYPE
    info.size = 0 if is_dir else size
    info.mode = 0o755 if is_dir else 0o644
    info.mtime = epoch
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    return info


def write_tar(path: Path, plan: Plan, fmt: str, level: int) -> None:
    def members(fileobj) -> None:
        with tarfile.open(fileobj=fileobj, mode="w", format=tarfile.PAX_FORMAT,
                          encoding="utf-8") as tf:
            if plan.root_name:
                tf.addfile(tar_info(plan.root_name, True, 0, plan.epoch))
            for entry in plan.entries:
                name = arc_name(entry.rel, plan.root_name)
                if entry.is_dir:
                    tf.addfile(tar_info(name, True, 0, plan.epoch))
                else:
                    with open(entry.path, "rb") as src:
                        tf.addfile(tar_info(name, False, entry.path.stat().st_size,
                                            plan.epoch), src)

    with open(path, "wb") as raw:
        if fmt == "tar.gz":
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw,
                               mtime=plan.epoch, compresslevel=level) as gz:
                members(gz)
        else:
            members(raw)


def check_member_name(name: str, root_name: str) -> None:
    if not name or name.startswith(("/", "\\")) or "\\" in name:
        raise PackError(f"unsafe archive path: {name!r}")
    if re.match(r"^[A-Za-z]:", name):
        raise PackError(f"absolute Windows path in archive: {name!r}")
    if any(part in ("", ".", "..") for part in name.split("/")):
        raise PackError(f"non-normalized archive path: {name!r}")
    if root_name and name != root_name and not name.startswith(root_name + "/"):
        raise PackError(f"member outside archive root: {name!r}")


def inspect_archive(path: Path, fmt: str, plan: Plan, digests: Dict[str, str]) -> int:
    expected = expected_members(plan)
    actual: Dict[str, bool] = {}
    content: Dict[str, str] = {}
    if fmt == "zip":
        with zipfile.ZipFile(path) as zf:
            for info in zf.infolist():
                name = info.filename.rstrip("/")
                check_member_name(name, plan.root_name)
                if stat.S_ISLNK(info.external_attr >> 16):
                    raise PackError(f"symbolic link in archive: {name}")
                actual[name] = info.is_dir()
                if not info.is_dir():
                    with zf.open(info) as stream:
                        content[name] = hash_stream(stream)
    else:
        with tarfile.open(path, "r:*") as tf:
            for member in tf:
                name = member.name.rstrip("/")
                check_member_name(name, plan.root_name)
                if member.isdir():
                    actual[name] = True
                elif member.isfile():
                    actual[name] = False
                    stream = tf.extractfile(member)
                    if stream is None:
                        raise PackError(f"cannot read archive member: {name}")
                    with stream:
                        content[name] = hash_stream(stream)
                else:
                    raise PackError(f"unsupported member type in archive: {name}")
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        wrong = sorted(n for n in set(expected) & set(actual) if expected[n] != actual[n])
        raise PackError(f"archive member mismatch: missing={missing[:5]}, "
                        f"extra={extra[:5]}, wrong_type={wrong[:5]}")
    for name, digest in digests.items():
        if content.get(name) != digest:
            raise PackError(f"content mismatch: {name}")
    return len(actual)


def format_list(fmt: str) -> List[str]:
    return ["zip", "tar.gz"] if fmt == "all" else [fmt]


def display(path: Path, source: Path) -> str:
    try:
        return path.resolve().relative_to(source).as_posix()
    except ValueError:
        return str(path)


def write_sums(out_dir: Path, outputs: List[Path]) -> None:
    lines = [f"{sha256_file(p)}  {p.name}\n" for p in sorted(outputs, key=lambda p: p.name)]
    with open(out_dir / "SHA256SUMS.txt", "w", encoding="utf-8", newline="\n") as stream:
        stream.writelines(lines)


def verify_sums(out_dir: Path) -> None:
    path = out_dir / "SHA256SUMS.txt"
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, sep, filename = line.partition("  ")
        if not sep or not filename.strip():
            raise PackError(f"malformed checksum line: {line!r}")
        target = out_dir / filename.strip()
        if not target.is_file() or sha256_file(target) != digest.strip():
            raise PackError(f"checksum mismatch: {filename.strip()}")


def cmd_pack(args: argparse.Namespace) -> int:
    plan = make_plan(args)
    digests = build_digests(plan)
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: List[Path] = []
    for fmt in format_list(args.format):
        target = out_dir / (plan.artifact_name + FORMAT_SUFFIX[fmt])
        tmp = target.with_name(target.name + ".tmp")
        try:
            if fmt == "zip":
                write_zip(tmp, plan, args.level)
            else:
                write_tar(tmp, plan, fmt, args.level)
            members = inspect_archive(tmp, fmt, plan, digests)
            os.replace(tmp, target)
        finally:
            if tmp.exists():
                tmp.unlink()
        outputs.append(target)
        print(f"[pack] {display(target, plan.source)}: {members} members, "
              f"{target.stat().st_size} bytes, sha256 {sha256_file(target)}")
    write_sums(out_dir, outputs)
    print(f"[pack] OK: {len(plan.entries)} source entries, "
          f"{len(outputs)} artifacts, epoch {plan.epoch}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    plan = make_plan(args)
    dirs = sum(1 for entry in plan.entries if entry.is_dir)
    files = len(plan.entries) - dirs
    parents = set()
    for entry in plan.entries:
        parts = entry.rel.split("/")
        for i in range(1, len(parts)):
            parents.add("/".join(parts[:i]))
    empty = sum(1 for entry in plan.entries
                if entry.is_dir and entry.rel not in parents)
    print(f"[check] source            : {plan.source}")
    print(f"[check] root name         : {plan.root_name or '(flat archive)'}")
    print(f"[check] included          : {dirs} directories, {files} files")
    print(f"[check] empty dirs kept   : {empty}")
    for reason, items in sorted(plan.skipped.items()):
        print(f"[check] excluded ({reason}): {len(items)}")
    if args.list:
        for entry in plan.entries:
            print(("  D  " if entry.is_dir else "  F  ") + entry.rel)
    print("[check] OK: no reparse points, no unsafe paths")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    plan = make_plan(args)
    digests = build_digests(plan)
    out_dir = args.out_dir.resolve()
    for fmt in format_list(args.format):
        target = out_dir / (plan.artifact_name + FORMAT_SUFFIX[fmt])
        if not target.is_file():
            raise PackError(f"artifact is missing: {target}")
        members = inspect_archive(target, fmt, plan, digests)
        print(f"[verify] {display(target, plan.source)}: OK "
              f"({members} members, sha256 {sha256_file(target)})")
    verify_sums(out_dir)
    print("[verify] OK")
    return 0


def cmd_clean(args: argparse.Namespace) -> int:
    out_dir = args.out_dir.resolve()
    if out_dir == CI_DIR or CI_DIR not in out_dir.parents:
        raise PackError("refuse to clean a directory outside .ci")
    if not out_dir.is_dir():
        print("[clean] nothing to remove")
        return 0
    if is_reparse(out_dir.lstat()):
        raise PackError(f"refuse to clean a reparse point: {out_dir}")
    shutil.rmtree(out_dir)
    print(f"[clean] removed {display(out_dir, DEFAULT_SOURCE)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pack the clean winroot skeleton into zip/tar artifacts.",
        epilog=(
            "Examples:\n"
            "  pixi run --manifest-path .ci/pixi.toml check\n"
            "  pixi run --manifest-path .ci/pixi.toml pack\n"
            "  pixi run --manifest-path .ci/pixi.toml verify\n"
            "  python .ci/pack.py pack --format tar.gz --root-name winroot\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                       help="repository root (default: parent of .ci)")
        p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR,
                       help="artifact directory (default: .ci/dist)")
        p.add_argument("--root-name", default=None,
                       help="top-level directory inside the archive (default: source name; "
                            "pass '' for a flat archive)")
        p.add_argument("--artifact-name", default=None,
                       help="output file basename (default: root name)")
        p.add_argument("--epoch", type=int, default=None,
                       help="fixed mtime, overrides SOURCE_DATE_EPOCH (default: 1980-01-01)")

    p_pack = sub.add_parser("pack", help="build artifacts and self-verify them")
    common(p_pack)
    p_pack.add_argument("--format", choices=("zip", "tar", "tar.gz", "all"), default="all")
    p_pack.add_argument("--level", type=int, choices=range(1, 10), default=9)

    p_check = sub.add_parser("check", help="dry run: show what would be packed")
    common(p_check)
    p_check.add_argument("--list", action="store_true", help="list every included entry")

    p_verify = sub.add_parser("verify", help="verify existing artifacts against the source")
    common(p_verify)
    p_verify.add_argument("--format", choices=("zip", "tar", "tar.gz", "all"), default="all")

    p_clean = sub.add_parser("clean", help="remove generated artifacts")
    p_clean.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR,
                         help="artifact directory (default: .ci/dist)")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "pack":
            return cmd_pack(args)
        if args.command == "check":
            return cmd_check(args)
        if args.command == "verify":
            return cmd_verify(args)
        if args.command == "clean":
            return cmd_clean(args)
    except (PackError, OSError, zipfile.BadZipFile, tarfile.TarError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
