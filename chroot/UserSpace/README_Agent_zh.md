---
AuthorType: Agent
TargetType: Agent
---

# UserSpace

用户的操作空间。
是用户操作和资产的所在。

```text
UserSpace/
├───Downloads/              # Shell Folder 重定向（用户发起下载的入口；流入，非归宿）
├───Storage/                # 大、重、胖的 Shell Folder 重定向目标（v1 Storage 语义）
│   ├───Documents/          #   文档
│   ├───Music/              #   音频
│   ├───Pictures/           #   图片
│   └───Videos/             #   视频
├───Knowledge/              # 自主内容：笔记、wiki、Obsidian vault
├───Collections/            # 自主内容：书签、Github Stars 等
└───Private/                # 凭证库：KeePass/1Password 等的库文件
```

Shell Folders 直接沿用 Windows 原始默认命名，不套额外层，也不改名。
它们是 Windows 资源管理器左侧栏认识的名字，通过注册表/属性页映射。
Storage 收纳的是大、重、胖、不能用文本编辑器打开的媒体/文档类 shell folder；
不用 Media 是因为其语义已被滥用，Storage 就是 Storage，有拓展性。
Downloads 语义不同（是流入入口，不是存储归宿），平铺在外，不进 Storage。
凭证是用户资产，由专门软件管，不单独顶层、不进 Control、不混软件配置；
独立加密/备份策略由对应软件负责。

`Downloads` 是唯一下载入口（用户发起）。机器管理的可重下载工件不存在独立目录--
它们跟着各自的软件/管理器走（如 `../Software/Scoop/cache/`）。
