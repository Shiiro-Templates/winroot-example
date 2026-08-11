---
AuthorType: Agent
TargetType: Agent
---

# Control

`chroot` 的环境控制层。它控制这个 chroot 环境本身--
环境变量、脚本、配置文件、命令日志、需求记录。**它不负责装软件配置**（各软件的 config 进 `../Software/Configs/`）。

```text
Control/
├───.META/            # Control 层元数据
├───Environment/      # 必须注入系统级环境变量的配置（树内项目级用 direnv，不在这里）
├───MotivationIndex/  # 需求记录：需求（根源）-> Projects 里的开发或 Software 里在用的软件
├───Profiles/         # shell/编辑器/终端/工具设置的备份，即 configfiles
├───Scripts/          # 启动、设置、验证、维护脚本
├───Templates/        # 可复用的配置和项目模板
└───Logs/             # ctl-log（命令执行记录）及运维日志
```

- `MotivationIndex` 记录需求及其满足状态：某需求（根源）指向 `../Projects/` 里的开发，或 `../Software/` 里在用的软件。
- 凭证放 `../UserSpace/Private`（KeePass/1Password 管），不放这里。
- 各软件自己的配置不进 Control，进 `../Software/Configs/`。
- 尽量使用文本格式，并通过 `%CHROOT_ROOT%` 而非盘符引用根目录。
