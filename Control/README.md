
# Control

 `winroot` 的**环境控制面**与运维中枢。
管理让这棵目录树运转起来的环境变量、维护脚本、高价值配置源件与需求账本。

```tree
Control/
├───.META/            # Control 层元数据
├───Environment/      # 需注入系统/用户级的环境变量配置
├───MotivationIndex/  # 需求账本：记录“根源需求 -> Projects 项目 / Software 软件”的映射与满足状态
├───Profiles/         # 亲手维护的 shell/编辑器/终端等高价值 configfiles 源件（即 dotfiles）
├───Scripts/          # 启动、挂载、验证与日常维护脚本
├───Templates/        # 可复用的配置片段与项目脚手架模板
└───Logs/             # 控制面操作记录（ctl-log）及运维日志
```
## 建议

- 在编写 `Scripts/`、`Environment/` 及配置文件时，统一使用约定的环境变量 %WIN_ROOT% 引用根目录
- 密码库与私钥等敏感资产统一归入 `../UserSpace/Private/`，交由 KeePass / 1Password 等专门软件接管。
- 不建议在 Windows 上使用 direnv ，已知存在严重的 SystemRoot/PATH 随机覆盖问题；mise 可用但不应用作过于复杂的配置

<!--@Nyashiiro::Note
To-Agent:
- **局部项目环境不进 `Environment/`**：这里只管全局/树级环境变量；具体代码仓库内部的开发环境变量由项目自己的 `pixi.toml` 就地管理。
- `Profiles/` 只放用户**亲手编写、跨机器复用**的配置源件（如 `.gitconfig`、终端配置）；软件运行过程中自己生成的庞杂配置目录（常混杂窗口状态、会话数据等）留在 `../Software/Configs/`。
-->

## 设计思路

- **面向需求溯源（`MotivationIndex`）**：工具和项目都只是满足需求的手段。在这里记录“当初为了解决什么问题才装了这个软件/开了这个坑”，日后重装迁移或清理时，按需求是否存续来决定去留，或选用/创造更好的替代品。
- 控制状态与运行态隔离：把高频变动、软件自管的运行时状态赶去 `Software/`，让 `Control/` 保持小巧，可整体备份或纳入版本控制
- 控制面下的记录与配置优先采用轻量格式，以便检视与版本追踪。