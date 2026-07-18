# Workspaces

Active, user-owned units of work. Each child should be movable, archivable, or
backed up as a coherent project boundary.

- `Projects`: projects that are not best modeled primarily as source-control
  repositories, including design, writing, research, and mixed deliverables.
- `Repositories`: source-control working trees, grouped by stable project ID or
  forge/owner when scale justifies it.
- `Labs`: named experiments and prototypes worth retaining.
- `Scratch`: explicitly short-lived work with no preservation promise.

Keep dependencies and build outputs inside a repository only when its tools
require that layout. Otherwise use `../Cache/Packages` and `../Cache/Builds`.
Move completed inactive work to `../Archive/Projects`; do not use `Archive` as
an automatic dumping ground.