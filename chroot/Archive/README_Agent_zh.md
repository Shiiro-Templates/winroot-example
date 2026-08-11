---
AuthorType: Agent
TargetType: Agent
---

# Archive

有意保留的非活跃材料。语义是**注意力管理工具，不是墓地**：放进去的理由是"现在不干这个"，
不是"结束了"。东西随时能拿回来。服务于注意力澄明 + 赛博囤积感，不服务于遗产管理。
Archive 不一定是 Legacy，反之亦然。

```text
Archive/
├───Projects/      # 已完成或暂离的项目（← ../Projects/ 的归档镜像）
├───Knowledge/     # 不再维护的知识库（← ../UserSpace/Knowledge/ 的归档镜像）
├───Software/      # 有意保留的安装包、软件副本
└───Snapshot/      # 从服务/应用导出的状态快照
```

归档入口和活跃内容出口保持同一粒度。未决定的文件不进 Archive（也没有 Inbox，未决定归宿是用户的临时问题）；
活跃文件属于 `../Projects/` 或 `../UserSpace/`。
