# chroot

`chroot` is the semantic root of this volume. It is not an operating-system
chroot and does not imply isolation. Everything intentionally owned by this
volume lives below this directory; volume-root artifacts created by Windows
remain outside it.

The first question for placing an item is: **who owns it, what role does it
serve, and what is its lifecycle?** Declarative setup is useful where
available, but it is not a premise of this layout.

## Top-level contract

| Directory | Meaning | Policy |
| --- | --- | --- |
| `Control` | Environment setup, scripts, records, and exported settings for the tree | Small and durable |
| `Software` | Actual installed or portable programs, toolchains, and package-manager roots | Preserve according to installer/tool requirements |
| `State` | Mutable configuration and durable data owned by software | Back up selectively |
| `Cache` | Derived or downloaded data that may be deleted without data loss | Disposable |
| `Home` | Long-lived personal documents, knowledge, media, and collections | Preserve |
| `Workspaces` | Active projects, repositories, experiments, and scratch work | Preserve by project |
| `Inbox` | Incoming material whose final home has not been decided | Temporary |
| `Archive` | Deliberately inactive, retained material | Preserve, mostly read-only |

## Placement rules

1. Put software where its supported installation model allows. A traditional
   installer may own `Software/Installed/<vendor-or-product>`; a portable app
   belongs in `Software/Portable/<product>`; a manager may own a complete root
   under `Software/PackageManagers/<manager>`.
2. Do not split a vendor-owned installation merely to make the tree look pure.
   Keep files beside the program when the software requires it. Separate state
   and cache only when the application officially supports choosing those
   paths.
3. Put controllable durable application state in `State` and safely disposable
   data in `Cache`. Uncontrollable state may remain in Windows AppData or
   ProgramData; `chroot` describes what you own, not a fake replacement for the
   Windows profile.
4. Put authored personal material in `Home`. Put project material in
   `Workspaces` while active and `Archive` when intentionally retired.
5. Put undecided material in `Inbox`, never in a generic permanent `Storage`
   directory.
6. Use `%CHROOT_ROOT%` in scripts and records instead of encoding a drive
   letter. Records in `Control` may document reality; they do not have to be
   capable of recreating it.
7. Top-level names are stable API. Add one only when no existing ownership and
   lifecycle category can represent the content.

## What `.pool` would mean

A `pool` is justified only when several logical consumers share one physical
store. Examples include a content-addressed store whose objects are named by a
hash, or a package manager's single download/store backend used by many
projects. These are implementation concepts, not synonyms for "put the real
files here." Ordinary installed applications and SDKs therefore do not need a
`.pool` wrapper; their category directory already is their physical home.

## Naming

- Use ASCII English names and `PascalCase` for structural directories.
- Below structural directories, retain official vendor/product names when that
  improves recognizability or is imposed by an installer.
- Use stable lowercase IDs only where you control the namespace, such as
  projects, scripts, and manually managed application-state boundaries.
- Avoid drive-specific names and do not assign meaning through case alone;
  Windows paths are normally case-insensitive.

## Realistic Windows examples

```text
Software/Installed/Microsoft VS Code/       # installer-managed payload
Software/Portable/Everything/               # self-contained portable app
Software/PackageManagers/Scoop/             # Scoop-owned root and layout
Software/Toolchains/Rust/                    # manually placed toolchain

State/Apps/obsidian/                         # only state whose path is controllable
Cache/Packages/cargo/                        # safely re-downloadable package cache
Home/Knowledge/personal-vault/               # user-authored knowledge
Workspaces/Repositories/demo/                # active source repository
```

An application-specific compatibility directory such as `Roaming` may exist
inside its own state boundary when useful, but `Local`, `LocalLow`, and
`Roaming` are Windows storage classes rather than the semantic taxonomy of this
whole tree.

See each top-level `README.md` for its local contract. `TREE.md` is the concise
reference tree.
