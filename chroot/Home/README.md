# Home

Long-lived personal material whose primary owner is the user, not an
application or project lifecycle.

- `Documents`: ordinary authored documents.
- `Knowledge`: notes, wikis, and application-managed knowledge bases such as
  Obsidian vaults.
- `Collections`: curated references such as bookmarks; each source gets a child
  only when it is actually used.
- `Media`: personal audio, images, and video.

Application binaries do not belong here. A knowledge base belongs here even
when an application indexes it; the app's UI state or index belongs in
`../State` or `../Cache` when its path is controllable. Active source trees and
project deliverables belong in `../Workspaces`.