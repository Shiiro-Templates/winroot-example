# Reference tree

```text
─chroot/
    ├───README.md
    ├───TREE.md
    ├───Control/                    # setup, records, and owned settings
    │   ├───README.md
    │   ├───Environment/            # environment variables and PATH setup
    │   ├───Inventory/              # descriptive software/resource records
    │   ├───Profiles/               # settings intentionally kept here
    │   ├───Scripts/                # launch and maintenance automation
    │   ├───Templates/              # reusable configuration templates
    │   └───Exports/                # exported Windows/application settings
    ├───Software/                   # actual software payloads
    │   ├───README.md
    │   ├───Installed/              # conventional installer destinations
    │   ├───Portable/               # self-contained portable applications
    │   ├───Toolchains/             # SDKs, runtimes, compilers, dev tools
    │   ├───PackageManagers/        # complete manager-owned roots
    │   ├───Shared/                 # shared runtimes and components
    │   └───Shims/                  # stable PATH-visible launchers
    ├───State/                      # controllable durable software state
    │   ├───README.md
    │   ├───Apps/                   # per-application configuration/data
    │   ├───Tools/                  # tool and package-manager state
    │   ├───Shell/                  # interactive shell state
    │   └───Secrets/                # credentials with a separate policy
    ├───Cache/                      # entirely disposable material
    │   ├───README.md
    │   ├───Downloads/              # machine-managed download cache
    │   ├───Packages/               # dependency and package caches
    │   ├───Builds/                 # derived build outputs
    │   ├───Apps/                   # per-application caches
    │   ├───Logs/                   # bounded diagnostic logs
    │   └───Temp/                   # process scratch data
    ├───Home/                       # long-lived personal material
    │   ├───README.md
    │   ├───Documents/
    │   ├───Knowledge/              # notes, wikis, and knowledge bases
    │   ├───Collections/
    │   │   └───Bookmarks/
    │   ├───Media/
    │   │   ├───Audio/
    │   │   ├───Images/
    │   │   └───Video/
    ├───Workspaces/                 # active units of work
    │   ├───README.md
    │   ├───Projects/               # mixed or non-repository projects
    │   ├───Repositories/           # source-control working trees
    │   ├───Labs/                   # named experiments and prototypes
    │   └───Scratch/                # explicitly short-lived work
    ├───Inbox/                      # material awaiting classification
    │   ├───README.md
    │   ├───Downloads/              # user-initiated downloads
    │   ├───Imports/                # staged imports
    │   └───Drop/                   # quick handoff area
    └───Archive/                    # inactive retained material
        ├───README.md
        ├───Projects/
        ├───Documents/
        ├───Software/
        └───Exports/
```

Only stable semantic categories are pre-created. Add product, source, project,
or collection children when they are actually needed. Conventional installers
and package managers may retain their own naming and internal structures below
the corresponding `Software` boundary.
