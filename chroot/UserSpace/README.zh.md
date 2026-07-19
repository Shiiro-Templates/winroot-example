# UserSpace

用户的操作空间。"孩子那里不是家"--UserSpace 不是归宿意义上的"家"，
是用户操作和资产的所在。前六个子目录是 Windows Shell Folder 重定向目标，
后两个是自主内容，最后是凭证库。

- `Desktop`：Shell Folder 重定向。
- `Documents`：Shell Folder 重定向。
- `Downloads`：Shell Folder 重定向（用户发起下载的入口）。
- `Music`：Shell Folder 重定向。
- `Pictures`：Shell Folder 重定向。
- `Videos`：Shell Folder 重定向。
- `Knowledge`：自主内容--笔记、wiki、Obsidian vault。
- `Collections`：自主内容--书签、Github Stars 等。
- `Vault`：凭证库--KeePass/1Password 等的库文件。

Shell Folders 直接沿用 Windows 原始默认命名，不套 `Storage/` 层，也不改名。
它们是 Windows 资源管理器左侧栏认识的名字，通过注册表/属性页映射。
凭证是用户资产，由专门软件管，不单独顶层、不进 Control、不混软件配置；
独立加密/备份策略由对应软件负责。

`Downloads` 是唯一下载入口（用户发起）。机器管理的可重下载工件不存在独立目录--
它们跟着各自的软件/管理器走（如 `../Software/Scoop/cache/`）。
