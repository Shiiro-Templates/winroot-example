---
Author: Agent
Target: Agent
---

# Software

`chroot` 下的软件相关一切：本体、配置、数据、缓存、包管理器、构建消费品。
第一层分类轴是"我开发用的 vs 非开发用的 + 构建消费"，不再用 v2 的"安装方式"当第一层。

```text
Software/
├───Devtool/                    # 我开发用的工具集（集体名词，非软件学意义的 toolchain）
│   ├───envs/                    #   开发环境（语言运行时、平台 SDK、框架工具链），下接 .pool/
│   ├───ide/                    #   VS Code 等，下接 .pool/
│   └───agent/                  #   Claude Code、OpenClaw 这类 harness+Agent，下接 .pool/
├───Apps/                       # 非开发应用软件（按安装方式分：卸载/更新/迁移方式不同）
│   ├───Installed/.pool/<appname the installer set>/   # installer 装的
│   └───Portable/.pool/<appname unzipped>/             # 解压即用
├───Build2Use/                  # 从源码构建来用、不维护的软件，下接 .pool/（大块非源码消费品）
├───Configs/                    # 软件配置/设置，与 Data 并列，不进 Control，不用 .pool
│   ├───Devtool/
│   └───Apps/
├───Data/                       # 装在工具上的功能载荷（扩展、全局包、插件），随工具存亡为错
│   ├───Devtool/.pool/
│   └───Apps/.pool/
├───Caches/                     # 仅按消费关系归类
│   ├───Devtool/.pool/          #   开发工具缓存，按工具名分桶
│   ├───Apps/.pool/             #   应用缓存，按应用名分桶
│   └───Temp/                   #   %TEMP% 重定向，非管理目标，不用 .pool
└───Scoop/                      # 包管理器根，挂顶层，内部自管
```

- 开发工具被当系统软件管，不区分安装方式。Devtool 内部按用途分（envs/ide/agent）。
- appname 用安装器/解压设的名，原样保留，不另套厂商层。Scoop 装的由顶层 `Scoop/` 独立管；uwp/msix 走系统，不管。
- **只使用、不维护的源码不进 `../Projects/`，进 `Build2Use/`。**
- Configs 下接配置资产（要版本控制跟踪），不用 `.pool`。Local/Roaming 等重定向锚点在 `Configs/<分类>/<tool>/` 下按需出现。
- Data 随工具存亡为错：升级/重装工具时 Data 该活下来。
- Scoop 的下载缓存跟着管理器走，不被 `Caches/` 收编。

`.pool` = 是管理目标；不用 `.pool` = 不是管理目标。详见顶层 README。
