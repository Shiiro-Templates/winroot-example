---
AuthorType: Human
TargetType: Human
---

# UserSpace

```tree
UserSpace/
├───Downloads/              # 浏览器与用户手动下载入口（Shell Folder 重定向）
├───Storage/                # 大体积系统默认文件夹重定向目标
│   ├───Documents/          #   文档（含各类软件与游戏默认写入的存档/杂项）
│   ├───Music/              #   音频
│   ├───Pictures/           #   图片
│   └───Videos/             #   视频
├───Knowledge/              # 自主维护的知识库：笔记、Wiki、Obsidian Vault
├───Collections/            # 个人收藏索引：书签、GitHub Stars 归档等
└───Private/                # 高敏凭证库：KeePass / 1Password 数据库文件、核心密钥
```

## 建议

- 在 Windows 资源管理器中右键系统默认的“下载 / 文档 / 音乐 / 图片 / 视频” ➔ 属性 ➔ 位置，将它们分别移动重定向到 `Downloads/` 与 `Storage/` 下的同名目录。
- `Downloads/` 仅作为用户主动下载的**临时流入区（Inbox）**，确认用途后及时归档或移入对应目录，避免在里面长期堆积。
- `Private/` 下的凭证资产交密码管理软件接管，并配置独立的冷备策略。

<!--@Nyashiiro::Note
To-Agent:
- **保留 Shell Folders 原始命名**：`Downloads` 及 `Storage/` 下的四个子目录直接对应 Windows API 与注册表映射的已知文件夹（Known Folders），保持英文原名，不改名、不套 `.pool`。
- **机器下载不进 `Downloads/`**：包管理器或构建工具自动拉取的缓存与工件跟随各自工具走（如 `../Software/Scoop/cache/` 或 `../Software/Caches/`），严禁将 `Downloads/` 用作脚本自动下载缓存区。
- **区分 `Storage/Documents` 与 `Knowledge/`**：`Storage/Documents` 是承接 Windows 软件默认倾倒的兜底目录；用户自己撰写的 Markdown 笔记与知识库归入 `Knowledge/`（具体代码仓库的开发文档则留在 `../Projects/` 对应仓库内）。
-->

## 设计思路

- **“系统污染区”与“纯净知识区”隔离**：Windows `Documents` 早已沦为各类应用与游戏乱塞存档和配置的公共杂物间。将它连同影音文件夹一起收进 `Storage/` 集中承接系统重定向，以保住外层 `Knowledge/` 的纯粹与干净。
- **流入（Flow）与驻留（Stock）分离**：同样是系统重定向目录，`Downloads/` 承载的是高频进出的待分流文件，因此与静态存放大体积文件的 `Storage/` 平级分立，方便日常随手取用与定期清空。