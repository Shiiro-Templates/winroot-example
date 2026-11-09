# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software codebase**. It is a directory-layout specification for organizing an entire Windows volume under a single semantic root called `chroot` (not an OS chroot; no isolation implied). The repository contains only Markdown documentation and an empty directory skeleton that scaffolds the proposed tree. There is no build system, no source code, no tests, no package manifest.

The actual volume layout lives under `chroot/`. `PLAN.md` at repo root is the **planning file** (design discussion record) — it is NOT part of the `chroot/` deliverable and never enters the tree. Do not apply deliverable-consistency rules (e.g. "no redundancy") to `PLAN.md`.

## Working language

The author works in Chinese. Authoritative content is written in `*_zh.md` files first; English (`*.md` without `_zh`) are placeholder stubs translated later only after the Chinese is finalized. **Always edit the `_zh.md` files.** Do not translate to English unless explicitly asked.

## File naming convention

Documentation files use the `README_Agent_zh.md` / `README_Agent_zh.md` pattern (renamed from the earlier `README.zh.md` form):
- `README_Agent_zh.md` — Chinese, authoritative, for Agent consumption (humans will later write the real READMEs)
- `README_Agent.md` — English placeholder, currently a TODO stub
- `TREE_Agent_zh.md` / `TREE_Agent.md` — the reference tree
- `glossary-map.zh-agent.md` — concept glossary (moved OUT of README because the README is a contract, not meeting minutes)

When renaming/moving these, use `git mv` to preserve history.

## Document formatting rules (author-enforced)

These come from the author's review annotations and are non-negotiable:

- **Directory structure must be shown as a tab-drawn tree** (`├──`, `└──`, `│`), never as a markdown bullet list, never as a markdown table. This applies to *directory semantics display*.
- **No markdown tables anywhere.** Concept comparisons use indented (tab) bullet lists instead:
  ```
  - `.pool` 目录
  	- 用途：...
  	- 版本控制：忽略
  ```
- **No version/migration narrative.** There is no v1/v2/v3 to the reader — the current version is the only version. Do not write "changed from X to Y" or "migrated from" in deliverable docs. (Historical evolution is fine inside `PLAN.md`.)
- `//` review annotations are working directives from the author, not deliverable content. After applying them, remove the `//` lines from deliverable files. Keep the `AuthorType: Agent / TargetType: Agent` YAML frontmatter.

## The layout's core principle

Every directory is **either a redirection anchor or a destination with explicit operational semantics. Purely-taxonomic directories do not exist.** The classification axes that matter:
- **Devtool vs Apps** (do I develop with it vs. not) — the first split under `Software/`
- **Consumption relationship** (delivered-good vs cache) — determines `Caches/` membership, NOT rebuildability
- **Maintain vs build-to-use** (Projects vs `Software/Build2Use/`) for source code

These concepts live in `glossary-map.zh-agent.md`, not in the README. Read it before reasoning about category boundaries.

## `.pool` and `.META` (two dotted-prefix markers, only these two)

- `.pool` = "is our management target, has metadata above it." Sits at a **category layer**, holds bulk non-source storage below (ignored by git/rg via `**/.pool/`). Used for SDK bodies, Build2Use, Data, redirectable caches.
- `.META` = metadata for a category whose children are **tracked source assets** (no `.pool`). Used at Projects category layers, `Control/.META`, etc.
- **Iron rule:** both sit at the category layer, **at least one directory away from any asset**, never inside an asset unit. Asset unit interiors (a project dir, a software dir) are their own world (git-managed or tool-native layout) — do not touch.
- They usually do not coexist: with `.pool`, metadata lives as sibling files above it; without `.pool` but needing metadata, use `.META`.
- A self-contained official unit (e.g. `python314`) goes directly under a `.pool/`, **never** gets its own nested `.pool`.

## Key structural decisions (verify against current files before relying)

- `Software/` first split is `Devtool/{envs,ide,agent}` (by purpose, NOT by "installation method"). `envs` covers language runtimes, platform SDKs (Android SDK), framework toolchains (Flutter) — anything "dev environment".
- `Software/Apps/{Installed,Portable}/.pool/<appname>` — appname is the installer-set or unzipped name, kept verbatim, no vendor wrapper layer.
- `Software/Configs/` holds software config (sibling to Data), **not** Control. Control is only the environment-control layer.
- `Control/MotivationIndex/` records needs and their satisfaction state (need → a project under Projects/ or software under Software/). Replaced the old `Inventory/`.
- Credentials go to `UserSpace/Private/` (managed by KeePass/1Password), never a top-level dir, never in Control, never mixed with software config.
- `UserSpace/Storage/` holds the big/heavy Shell Folder redirections (Documents/Music/Pictures/Videos). `Downloads/` stays at UserSpace root (inflow, not a destination). `Desktop` was intentionally dropped.
- `Projects/Public/`: `Own-Dev` (self-led, dev-focused) vs `Own-Community` (stewardship, community-driven, direction-maintenance) vs `Forks` (forked & maintained) vs `Mirrors` (read-only study mirror) vs `Contrib` (temporary upstream contribution).
- `Archive/` is "set aside, not dead" — an attention-management tool, not a graveyard. Subdirs mirror active areas (Projects/Knowledge/Software/Snapshot).

## Git workflow

- Branch `v3` holds current work. Commit messages follow the author's convention: `Agent: <what>` for the agent's commits, `QueryAI: <note>` for the author's review/annotation commits.
- Never commit on `main` directly from agent work without instruction. The author reviews and commits themselves.
- Before any command that could discard uncommitted work (`git checkout`/`reset`/`clean`, `rm -rf`), run `git status` first.

## When making changes

1. Read the relevant `*_Agent_zh.md` and `TREE_Agent_zh.md` first — they are the source of truth, not `PLAN.md`.
2. Keep `TREE_Agent_zh.md`, the actual directory tree on disk, and each directory's `README_Agent_zh.md` **three-way consistent**. A change to one requires updating the others.
3. Apply author `//` annotations by changing the content, then delete the `//` lines.
4. Don't invent new dotted-prefix markers or new top-level directories — both are stable API; adding requires explicit justification that no existing category fits.

---
