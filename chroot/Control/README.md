# Control

The small control and reference area for `chroot`. It records how the tree is
used, but it is not expected to recreate Windows or every traditionally
installed program.

- `Environment`: environment-variable and PATH setup owned by this tree.
- `Inventory`: human- or tool-generated records of installed software and
  managed resources; descriptive records are as valid as desired-state files.
- `Profiles`: shell, editor, terminal, and tool settings you intentionally own.
- `Scripts`: launch, setup, validation, and maintenance scripts.
- `Templates`: reusable configuration and project templates.
- `Exports`: snapshots exported from Windows or applications for reference or
  restoration.

Keep credentials in `../State/Secrets`, not here. Prefer text formats where
practical and refer to the root through `%CHROOT_ROOT%` rather than a drive
letter. A record may simply say what is installed and where; automation is
optional.