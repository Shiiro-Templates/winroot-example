# Cache

Disposable, derived, or re-downloadable material. Deleting this entire
directory must not destroy the only copy of anything important.

- `Downloads`: machine-managed download caches.
- `Packages`: package-manager and dependency caches, grouped by tool ID.
- `Builds`: derived build outputs kept outside project trees when practical.
- `Apps`: per-application caches.
- `Logs`: non-audit diagnostic logs with bounded retention.
- `Temp`: process scratch data and temporary files.

If an item cannot be safely removed, it is not cache: place durable software
state in `../State`, incoming user downloads in `../Inbox/Downloads`, or
long-lived authored material in `../Home`.