---
AuthorType: Human
TargetType: Human
---

# Software

```tree
Software/
├───Devtool/                    # 开发工具集（按角色分，下接 .pool/）
│   ├───envs/                   #   语言运行时、平台 SDK、框架工具链
│   ├───ide/                    #   VS Code 等编辑器与 IDE
│   ├───agent/                  #   Claude Code、OpenClaw 等 Harness + Agent
│   └───MCP/                    #   MCP Server 集合
├───Apps/                       # 日常应用软件（按安装与维护方式分，下接 .pool/）
│   ├───Installed/              #   经由安装器安装的软件
│   └───Portable/               #   解压即用的便携软件
├───Build2Use/                  # 拉取源码仅做本地编译使用的软件（下接 .pool/）
├───Configs/                    # 软件运行时的配置与设置（不用 .pool/）
│   ├───Devtool/<tool>/         #   按工具名分桶，内部按需设 Local/Roaming 等锚点
│   └───Apps/<app>/
├───Data/                       # 挂载在工具上的功能载荷（下接 .pool/）
│   ├───Devtool/                #   IDE 扩展、全局包、插件
│   └───Apps/
├───Caches/                     # 随时可清理的缓存副本
│   ├───Devtool/                #   开发工具缓存（下接 .pool/，按工具名分桶）
│   ├───Apps/                   #   应用缓存（下接 .pool/，按应用名分桶）
│   └───Temp/                   #   %TEMP% 整体重定向目标（不用 .pool/）
└───Scoop/                      # 包管理器根，挂顶层内部自管
```

## 建议

- 只编译来用、不参与开发维护的开源代码归入 `Build2Use/`
- UWP / MSIX 等强绑定系统的商店应用随系统默认机制走，不必强行迁入此目录。

<!--@Nyashiiro::Note
To-Agent:
- **顺应原生结构**：`.pool/` 下直接保留安装器或压缩包设定的原始目录名，不额外套厂商层级，不强拆软件要求同目录存放的文件。
- **包管理器自治**：由 `Scoop/` 管理的软件及其自身的下载缓存留在 `Scoop/` 内部闭环，不被 `Apps/` 或 `Caches/` 强行收编。
- **三态分流边界**：
  - `Configs/` 存放软件运行配置（不用 `.pool/`，但注意与用户手写的 `../Control/Profiles/` 区分）；
  - `Data/` 存放插件、扩展等大体积功能载荷（用 `.pool/`）；
  - `Caches/` 仅存放删除后不影响当前直接消费关系的加速副本（正在被直接消费的产物属于交付物，严禁归入 `Caches/`）。
-->

## 设计思路

- 本体与运行态解耦（工具存亡 ≠ 载荷存亡）：把 `Data/`（如 VS Code 扩展、全局包）与 `Configs/` 从软件本体目录中剥离出来独立成层——重装或升级工具本体时，挂在上面的插件载荷与配置应当无损存续；卸载工具时，也能按意愿决定是否保留数据。
- Devtool 按角色，Apps 按生命周期：开发工具（`Devtool/`）相当于开发者的系统基础设施，使用时关注的是它在工作流里的角色（`envs` / `ide` / `agent`），而非它是安装包还是解压版；普通应用（`Apps/`）则更关注日后怎么升级、迁移和卸载，因此按 `Installed` 与 `Portable` 切分。