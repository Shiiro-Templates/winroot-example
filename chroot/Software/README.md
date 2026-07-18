# Software

Actual software payloads located under `chroot`. They are not assumed to be
rebuildable from a manifest: a conventional Windows installer, package manager,
portable archive, or manual SDK setup may own each subtree.

- `Installed`: payloads placed by conventional installers whose destination can
  be selected.
- `Portable`: self-contained applications intentionally managed as portable.
- `Toolchains`: SDKs, compilers, runtimes, build systems, and development tools.
- `PackageManagers`: complete manager-owned roots such as Scoop or Chocolatey.
- `Shared`: shared runtimes and components used by several applications.
- `Shims`: stable launchers and PATH-visible command shims.

Use the vendor or product boundary expected by the installer and preserve its
internal layout. Do not force every payload into an invented lowercase ID or
split out adjacent state when the product does not support that. State and
cache should use `../State` and `../Cache` only where their locations are
actually controllable. Personal and project files never belong here.