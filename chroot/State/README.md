# State

Durable mutable software state whose location can sensibly be controlled. This
is an opt-in home for selected applications and tools, not a wholesale mirror
or replacement for Windows AppData and ProgramData.

- `Apps`: per-application configuration and durable application data.
- `Tools`: state for SDKs, package managers, IDEs, and command-line tools.
- `Shell`: profiles and interactive shell state not kept in `Control/Profiles`.
- `Secrets`: credentials and private keys that require a separate access and
  backup policy.

Use a stable application boundary such as `Apps/obsidian` when you control that
path. Inside it, retain the layout the program expects; `config`, `data`, or a
Windows compatibility layout are optional, not mandatory. If software insists
on using the real user profile, leave it there rather than building a fragile
semantic fiction. Anything safely regenerated belongs in `../Cache`, while
user-authored documents and knowledge belong in `../Home`.