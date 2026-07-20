---
Author: Agent
target: Agent
---
# chroot v3 修改计划

基于 v2 (b7943d7) + 作者批注 (d697c19) + v3 讨论结论整合。

核心方向：v2 是"按语义分类"的文件管理哲学；v3 转向"**重定向基础设施 + 按消费关系组织**"。每个目录要么是一个重定向锚点，要么是一个有明确操作语义的归宿。不存在纯分类性质的目录。

---

## 一、顶层结构（最终，5 个）

```
chroot/
├── Control/        # 环境控制层：环境变量、脚本、配置文件、命令日志（v1 Settings 语义）
├── Software/       # 软件本体、配置、数据、缓存、包管理器、构建消费品
├── UserSpace/      # 用户的操作空间（Shell Folder 重定向 + 自主内容 + 凭证）
├── Projects/       # 你开发维护的项目（原 Workspaces，改名）
└── Archive/        # 暂离的材料，注意力管理工具
```

从 v2 的 8 个变 5 个：删 `Inbox`，删 `Home`（改回 `UserSpace`），删 `State`（职责分流到 Software/Configs 与 UserSpace），`Cache` 移入 `Software/`，`Workspaces` 改名 `Projects`。

**State 删除的依据**：v2 把 State 定义为"软件拥有的可变配置和持久数据"，作者批注"语义不明"--名字本身制造歧义（state 多义），定义边界不可操作。拆解其原职责后全部有更准的归宿：软件配置 -> `Software/Configs/`（与 Data 并列，是软件生命周期之物，不归环境控制层）；凭证 -> `UserSpace/`（KeePass/1Password 管）。State 顶层空了，删。

---

## 二、`.pool` 与 `.META` 约定

两个点号前缀标记目录，分工不同，通常不共存。

### `.pool` -- 存储隔层

`.pool` 是一个**按需使用的存储隔层**，不是默认结构。它把一个用途分类的"管理语义"和"实际存储"分离：

```
<用途分类>/
├── (管理语义所在，形式不约定：可能是 manifest、别名、标签等)
└── .pool/               # 存储边界，在用途分类这层
    └── <具体工具>/       # 散装存储，无固定布局
```

**核心语义**：`.pool` = "是我们的管理目标，上层有元数据"。不用 `.pool` = "不是我们的管理目标"（要么是系统绑定我们只重定向、要么是别人管）。

- **`.pool` 之上**（用途分类层）= 管理语义所在。统一、结构化、可被统一管理软件解析。**具体形式不预先约定**，留给实际开发统一管理软件时再定。
- **`.pool` 之下**（实际存储）= 散装，无约定布局。可能是工具自带的目录结构、附属管理软件接管的布局、解压后的原始文件。
- **统一管理软件的工作**：不解析 `.pool` 里面的散装内容，只读 `.pool` 之上的语义，在自己的逻辑里构建分类视图（如标签视图、按用途视图）。散装实际文件通过上层语义被索引和虚拟分类。

**何时用 `.pool`**：是我们的管理目标、且管理语义和实际存储需要分离时。典型：附属管理软件接管的存储（rustup 管的 Rust）、从源码构建的消费软件（Build2Use）、Data（功能载荷）、Caches 中可重定向的应用缓存。内容大、非源码、要被版本控制排除。

**何时不用 `.pool`**：不是我们的管理目标时。
- 自洽官方软件单元（如 `python314`）-- 生来带官方名字和内部布局，强加隔层破坏自洽性。直接作为存储内容放在上层 `.pool` 之下（即 `.pool/python314/`），不在它内部再套 `.pool`。
- Windows 绑定文件夹（Shell Folders）-- 路径用 WinAPI 直接取得，内部布局是 Windows 的，管不了也不该管。
- `Caches/Temp` -- %TEMP% 重定向，系统属性，我们只做重定向、不管内部，不是管理目标。
- 源码项目（Projects 下）-- 内容是要被版本控制跟踪的源码，不该被忽略，用 `.META` 而非 `.pool`。

**版本控制属性**：`.pool` 同时是版本控制排除边界。原因：**它不是源码，且可能有体积问题**。不是因为可重建。
- gitignore `**/.pool/`，rgignore 排除 `.pool`
- 装的不只是缓存：SDK 本体（交付物）也进 `.pool`，因为它大且非源码
- 反例：锁文件可重建，但是源码且小 -> 被跟踪，既不进 `.pool` 也不是缓存

**结构化语义原则**：**结构化语义永远在 `.pool` 之上，`.pool` 永远是叶子存储**。`.pool` 之下可放散装的工具目录（如 `python314/`），那只是存储内容，不是结构化语义分层。

### `.META` -- 元数据目录（无 .pool 时用）

`.META` 用于"内容不需要 `.pool`（源码、要版本控制跟踪），但仍需管理元数据"的场景。典型：Projects 分类层。

- 始终被 git 跟踪，始终被搜索包含
- 内容：资产单元的分类元数据（归属、标签、状态等），具体形式不预先约定
- **位置铁律**：`.META`（和 `.pool`）永远贴着分类层，**离资产至少一个目录的距离，绝不进资产单元内部**。资产单元（项目目录、软件目录）内部是它自己的世界（git 管或工具自带布局），我们不碰。
- **按需放**，不强制每个分类层都有；只有当该分类下的资产需要被统一管理软件索引时才放。
- 与 `.pool` 互补：有 `.pool` 时元数据直接在 `.pool` 之上兄弟位置，**不建 `.META`**；无 `.pool` 但需元数据时用 `.META`。两者通常不共存。

### 两者关系总结
//不得使用markdown表格！！！！
| | 用途 | 版本控制 | 位置 | 典型场景 |
|---|---|---|---|---|
| `.pool` | 存储隔层（大非源码） | 忽略 | 分类层，下接散装存储单元 | Devtool/langenv、Build2Use |
| `.META` | 元数据（无 .pool 时） | 跟踪 | 分类层，下接资产单元 | Projects 分类层 |

两者都在**分类层**，描述其下的单元。区别：`.pool` 下层是大块非源码存储（忽略），`.META` 下层是源码资产（跟踪，单元内部由 git 管）。共同铁律：都贴分类层，离资产/存储单元至少一个目录，绝不进单元内部。

v1 的 `.identity`、`.store` 等 ad-hoc 标记在 v3 中收敛进 `.META` 或 `.pool` 之上的语义文件，不单独保留。点号前缀特殊目录就这两个。

---

## 三、核心概念澄清（文档必须分开写，否则重犯谬误）

### 交付物 vs 缓存（按消费关系，不按可重建性）

- **交付物**：被直接消费的东西。即使可重建，它正在被使用。删除会破坏正在进行的消费关系。
- **缓存**：仅为避免重建/重新下载而保留、**不被直接消费**。删除只产生重建成本，不破坏消费关系。
- **判定测试**：删除后是否有正在进行的消费关系被破坏？有 -> 交付物；无 -> 缓存。
- **反例**：`target/` 完全可重建，但有自己的目录、不进统一缓存--它是正在被运行/测试的工作本体（交付物）。可重建 ≠ 缓存。
- **安全维度**：误标交付物为缓存 = 雷霆清理删掉正在用的资产（不可逆，危险）；误标缓存为交付物 = 浪费空间（可接受）。安全优先于整洁。

### `.pool` vs `Caches`（两套独立判定，有重叠但非同集合）

- `.pool` 键：（非源码 ∧ 大）。是版本控制层面的排除。
- `Caches` 键：（仅为避免重建/重下 ∧ 不被直接消费）。是消费关系层面的归类。
- 重叠：多数缓存也该 `.pool`。
- 不重叠例：50GB 不可重建数据集 -> `.pool`（大非源码）但非缓存（被消费）；2KB 可重定向应用缓存 -> 缓存但不值得 `.pool`。
- **"可重建 -> 缓存 -> 忽略"是三段谬误**，每个环节独立决策，互不蕴含。

### Projects vs Build2Use（开发维护 vs 构建消费）

- **Projects**：你**开发、维护**的源码项目。你是作者/贡献者，代码被版本控制跟踪，用 `.META` 装元数据。
- **Build2Use**：你**只构建来用、不维护**的源码软件。你是消费者，源码+构建产物对你而言是大块非源码消费品，用 `.pool` 收纳。
- 判定：这份源码你是要改它、维护它，还是只 build 出来用？前者 -> Projects；后者 -> Build2Use。**只使用的源码不应该放在 Projects**。

---

## 四、各顶层目录详细决定

### 1. Control（v1 Settings 语义，环境控制层）

Control 回归 v1 `Settings/` 的本义：**控制这个 chroot 环境本身**的东西--环境变量、脚本、配置文件、命令日志。它**不负责装软件配置**（各软件的 config 进 `Software/Configs/`）。

```
Control/
├── Environment/    # 必须注入系统级环境变量的配置（非树内项目级，那个用 direnv）
├── Inventory/      # 已安装软件/受管资源记录（人写或工具生成，说清楚即可）
├── Profiles/       # shell/编辑器/终端/工具设置的备份
├── Scripts/        # 启动、设置、验证、维护脚本
├── Templates/      # 可复用的配置和项目模板
└── Logs/           # ctl-log（命令执行记录）及其他运维日志  [新增]
```

- **新增 `Logs/`**：作者 v1 的 `ctl-log` 在 v2 被遗漏，补回。
- **`Environment/` 说明修正**：放的是"不塞进系统级就容易出故障的"配置；树内项目级环境变量用 direnv，不在这里。
- **`Inventory/` 说明修正**：去掉"描述性记录与期望状态文件同样有效"的模糊措辞；人写的记录或工具生成的快照都说清楚用途即可。
- **删除 `Exports/`**：语义模糊，作者批注"傻逼"。导出快照如需保留，作为记录放进 Inventory。
- 凭证放 `UserSpace/`（KeePass/1Password 管），不放这里。
- v1 `Settings/` 下的 `configfile/`（通用配置文件）职责：环境控制相关的配置文件留 Control；**各软件自己的配置不进 Control，进 `Software/Configs/`**。

### 2. Software（本轮核心重构）

**第一层分类轴**：我开发用的 vs 非开发用的 + 构建消费。不再用 v2 的"安装方式"当第一层。

```
Software/
├── Devtool/              # 我开发用的工具集（集体名词，非软件学意义的 toolchain）
│   ├── langenv/          # 语言环境（语言运行时、编译器、SDK、toolchain）
│   │   └── .pool/        #   存储边界，其下散装各语言工具链
│   ├── ide/              # VS Code 等
│   │   └── .pool/
│   └── agent/            # Claude Code、OpenClaw 这类 harness+Agent
│       └── .pool/
├── Apps/                 # 非开发应用软件
│   ├── Installed/        #   installer 装的（有卸载程序，注册在系统）
│   │   └── .pool/        #   下接 .pool，其下放安装器设的目录名
│   │       └── <appname the installer set>/
│   └── Portable/         #   解压即用的便携应用
│       └── .pool/
│           └── <appname unzipped>/
├── Build2Use/            # 从源码构建来用、不维护的软件  [新增]
│   └── .pool/            #   源码+构建产物作存储，大块非源码消费品
│       └── <software>/   #   如 Build2Use/.pool/ripgrep/（散装，含源码与产物）
├── Configs/              # 软件的配置/设置，与 Data 并列  [新增]
│   ├── Devtool/          #   开发工具配置（IDE、shell、agent 的设置）
│   │   └── <tool>/       #   配置布局由工具定，散装；Local/Roaming 按需作重定向锚点
│   └── Apps/             #   应用配置
│       └── <app>/
├── Data/                 # 装在工具上的功能载荷，随工具存亡为错  [新增类别]
│   ├── Devtool/          #   是管理目标 -> 下接 .pool/
│   │   └── .pool/        #   VS Code 扩展、npm/cargo 全局包、插件
│   └── Apps/             #   应用插件、浏览器扩展等
│       └── .pool/
├── Caches/               # 仅按消费关系归类（见概念澄清）
│   ├── Devtool/          #   是管理目标 -> 下接 .pool/
│   │   └── .pool/        #   开发工具缓存，按工具名分桶（cargo registry cache 等）
│   ├── Apps/             #   是管理目标 -> 下接 .pool/
│   │   └── .pool/        #   应用缓存，按应用名分桶
│   └── Temp/             #   %TEMP% 重定向，非管理目标，不用 .pool，只重定向不管内部
└── Scoop/                # 包管理器根，挂顶层（跨 Devtool/Apps，内部自管）
```

**Devtool 内部按用途分**（langenv/ide/agent），不再按软件学分类。`Toolchains` 错在用软件学概念命名用户管理边界（IDE/Agent 不是 toolchain）。`sdk_toolchains` 改为 `langenv`，避免读起来像"SDK 和 toolchain 的软件学合集"。

**Devtool 的 `.pool` 层级**（`.pool` 在用途分类层，具体工具在其下）：

```
Devtool/langenv/.pool/python314/    # python314 自洽单元，整体作存储，内部不再套 .pool
Devtool/langenv/.pool/rust/         # 可能由 rustup 接管 .pool/rust/ 的内容
```

- `.pool` 在用途分类层（langenv/ide/agent），作为该分类的存储边界
- 具体工具（python314、rust、go）在 `.pool` 之下，散装存储
- 管理语义（工具归属等）在 `.pool` 之上，形式不约定
- 自洽官方单元（python314）在 `.pool` 下整体存在，不在它内部再套 `.pool`
- 附属管理软件接管的（rust）其 `.pool/rust/` 下内容由 rustup 管

**Devtool 不区分安装方式**：开发工具被当系统软件管，怎么装的不重要。内部只按用途分。

**Apps 保留安装方式分类**：普通应用软件的安装方式有实际操作语义（卸载/更新/迁移方式不同），值得分桶。installer 装的有卸载程序、注册在系统；portable 解压即用、删文件夹即卸载。Scoop 装的已由 Scoop 顶层独立管，不进 Apps；uwp/msix 走系统，不管，不进 Apps。

```
Software/Apps/
├── Installed/.pool/<appname the installer set>/   # 安装器设的目录名，原样保留
└── Portable/.pool/<appname unzipped>/             # 解压出来的目录名，原样保留
```

- **都用 .pool**：Apps 本体是管理目标（要被统一软件管），下接 .pool。
- **appname 用安装器/解压设的名，原样保留**：呼应 python314 原则--应用目录名用软件自己的官方/安装名，我们不改名。.pool 之下是散装存储，appname 是存储单元，内部布局由 installer/解压决定，我们不碰。不另套厂商层。
- **本体分安装方式、Configs/Data/Caches 的 Apps 桶不分**：配置/数据/缓存按 appname 分桶即可，安装方式对配置管理无意义。这种不对称是对的。

**Build2Use**：从源码构建出来用、但不维护的软件。源码+构建产物一起进 `.pool`（对你而言是大块非源码消费品，要被版本控制排除）。管理语义（构建配置、版本、来源）在 `.pool` 之上。**只使用、不维护的源码不进 Projects，进这里。** 与 Projects 的边界见概念澄清。

**Configs（软件配置，与 Data 并列）**：各软件自己的配置/设置（如 IDE 的 settings.json、shell 的 rc、agent 配置）。是软件生命周期之物，进 Software 下与 Data 并列，**不进 Control**（Control 只管环境控制层）。镜像 Devtool/Apps 切分。下接配置资产（你精心调的设置，要版本控制跟踪），**不用 `.pool`**。Local/Roaming 等重定向锚点在 `Configs/<分类>/<tool>/` 下按需出现--只有工具配置确实分发到 `%LOCALAPPDATA%`/`%APPDATA%` 时才作锚点，不强加给只有单一配置目录的工具。这取代了 v2 State 的"可控持久软件配置"职责，且命名无歧义。

**Data 是独立类别，不等于 config/缓存/binary**：
- VS Code 扩展：不是本体（卸载 VS Code 不该带走）、不是 config（不是 settings.json）、不是缓存（删了要重装、代表功能选择）。是装在工具上的功能载荷。
- npm/cargo 全局包同理。
- 核心属性：**随工具存亡是错的**--升级/重装工具时，Data 该活下来。这是"雷霆清理"担忧的反面：不只别误删，而是别让正常重装连坐清掉投资。
- 物理分离送一个安全特性：删 `Devtool/langenv/.pool/python314/` 时 `Data/Devtool/python314/` 自动幸存，不靠纪律保证。
- dev tool 大多支持改 data home（`*_HOME`、`--extensions-dir` 等），留在 C 盘 AppData 是放弃管理权 -> **提供容器**。

**Caches 不再预建 Packages/Builds/Logs/Downloads**，原因逐条：
- `Packages`：包管理器缓存跟着管理器走（Scoop cache 在 Scoop/ 内），不该被中央 `Caches/Packages/` 收编。且语义也不好（用软件分发概念命名用户边界）。
- `Builds`：构建产物要么在项目内（`target/` 是交付物），要么作为 snapshot 进 Archive，不进缓存。构建消费品有独立 `Build2Use`。
- `Logs`：不可重定向的管不了；可重定向的日志是审计物不是废料。定位模糊，删。
- `Downloads`：没几个软件单独给下载缓存路径。做不到，删。
- **保留 `Apps/`**：应用支持重定向时，它产生的可丢弃、不被直接消费的数据是真缓存。是管理目标 -> 下接 `.pool/`，按应用名分桶。不能塌进 Temp--Temp 是无分类暂存黑洞，全塞进去丧失选择性清理能力（只清某应用缓存而不碰别的）；按应用分桶才能精准丢弃。
- **保留 `Temp/`**：`%TEMP%` 重定向，系统属性、被一切进程共享、无法按消费方归类。**非管理目标，不用 `.pool`**--我们只做重定向，不管它内部。单独成桶，不跟它计较分类。
- Devtool/Apps 缓存是管理目标 -> 各下接 `.pool/`；Temp 不是 -> 不用。`.pool` 的有无即"是不是我们的管理目标"。

**Data 的务实 caveat**：有些工具把 data 和 cache 塞在同一个 env-var home 里、不给你拆（cargo 的 `CARGO_HOME` 同时装 registry cache 和 installed bins）。遇到拆不开的：**整个 home 路由到 Data/，不路由到 Caches/**。因为误标 data 为 cache = 不可逆丢失（危险），误标 cache 为 data = 浪费空间（可接受）。安全优先于整洁。

**Scoop 挂顶层**：Scoop 跨 Devtool/Apps（既装语言环境也装普通应用），自己没法干净落进任何一边。作为管理器根挂 Software 顶层，内部按自身 bucket 机制自管。Scoop 的下载缓存（`Scoop/cache/*.7z`）是缓存，但位置上跟着管理器走，不被 `Caches/` 收编。

### 3. UserSpace（改回 v1 语义，不用 Home）

"孩子那里不是家"--UserSpace 是用户的**操作空间**，不是归宿意义上的"家"。Home 命名误导（让人以为是家目录/存放个人创作内容）。

```
UserSpace/
├── Desktop/         # Shell Folder 重定向
├── Documents/       # Shell Folder 重定向
├── Downloads/       # Shell Folder 重定向（用户发起下载的入口）
├── Music/           # Shell Folder 重定向
├── Pictures/        # Shell Folder 重定向
├── Videos/          # Shell Folder 重定向
├── Knowledge/       # 自主内容：笔记、wiki、Obsidian vault
├── Collections/     # 自主内容：书签、Github Stars 等
└── Vault/           # 凭证库：KeePass/1Password 等的库文件  [新增]
```

- **Shell Folders 直接沿用 Windows 原始默认命名**（Desktop/Documents/Downloads/Music/Pictures/Videos），不套 v1 的 `Storage/` 层，也不改名。它们是 Windows 资源管理器左侧栏认识的名字，通过注册表/属性页映射。
- **Knowledge/Collections 抽出**作为用户自主内容，与 Shell Folder 重定向目标并列。
- **Vault（凭证）**：凭证是用户资产，由 KeePass/1Password 等专门软件管，不单独占顶层、不进 Control（环境控制层）、不混进软件配置。库文件作为资产放 UserSpace 下。命名 Vault 而非 Secrets，避免语义过重且与软件管理职责对齐。独立加密/备份策略由对应软件负责。
- README 标注：前六个是 Windows Shell Folder 重定向目标，Knowledge/Collections 是用户自主管理内容，Vault 是凭证库。
- Downloads 冲突自然消解：`Caches/Downloads` 已删，`UserSpace/Downloads` 是唯一下载入口（用户发起）。机器管理的可重下载工件不存在独立目录--它们跟着各自的软件/管理器走。

### 4. Projects（原 Workspaces，改名 + 仓库语义分配）

独立顶层，不回 UserSpace 下--它是活跃工作的主战场，体量和 Software/Archive 对等。改名 `Projects`，因为装的就是"你开发维护的项目"。

**仓库按可见性/归属分组，加一个无 git 的 Playground：**

```
Projects/
├── Playground/          # gitless scratch，无 git 的草稿/实验
├── Private/             # 私有仓库
│   ├── Demos/           #   演示项目
│   ├── Tools/           #   工具类
│   └── Products/        #   产品类
├── Public/              # 公开仓库
│   ├── Demos/           #   演示
│   ├── Own/             #   自己的项目
│   ├── Forks/           #   fork 并维护的项目（有自己的改动、长期跟进）
│   ├── Mirrors/         #   为学习同步的只读镜像（看源码用，不贡献）
│   └── Contrib/         #   临时贡献，不长期维护
└── Orgs/                # 组织仓库
```

- **Playground**：不用 git 的草稿实验区。
- **Private**：私有仓库，按用途分 Demos/Tools/Products。
- **Public**：公开仓库。`Own` 是自己的项目；`Forks` 是 fork 并维护的项目（有自己的改动、长期跟进）；`Mirrors` 是为学习同步的只读镜像（看源码用，不贡献）；`Contrib` 是为别人项目做临时贡献的 clone（要 push 回 upstream，不长期维护）。
- **Orgs**：所属组织的仓库。
- 类型轴（git 与否、是不是 repo）已降级为属性，不再用作顶层分类；分组按**可见性/归属**（Private/Public/Orgs）+ 一个无 git 的 Playground。

**每个项目作为一个整体资产，内部由 git 管，我们不碰。** `.META` 服务于分类层（描述其下有哪些资产单元），**不进资产内部**：

```
Projects/Public/Own/
├── my-project/          # 整体是我们的资产，内部(src/.git/等)不碰
├── another-project/
└── .META/               # [按需] 描述 Own 下资产单元的分类元数据，离资产至少一个目录
```

- **`.META`（和 `.pool`）永远贴着分类层**，离资产至少一个目录的距离，绝不进资产单元内部。
- `.META` 按需放，不强制每个分类层都有；只有当该分类下的资产需要被统一管理软件索引时才放。
- **项目文档**：在项目内的 `docs/`，或对应文档站项目的 `docs/`。文档归属不属于本结构讨论范畴。
- 仓库规模大时，可在分组下按 forge/owner 进一步组织（如 `Orgs/<org>/<repo>/`），按需建，不预约定。

### 5. Archive（语义从"终态"改为"暂离"）

```
Archive/
├── Projects/         # ← Projects 的归档镜像
├── Knowledge/        # ← UserSpace/Knowledge 的归档镜像
├── Software/         # 有意保留的安装包、软件副本
└── Snapshot/         # 从服务/应用导出的状态快照（替代 v2 的 Exports）
```

- **语义重写**：归档是注意力管理工具，不是墓地。放进去的理由是"现在不干这个"，不是"结束了"。东西随时能拿回来。服务于注意力澄明 + 赛博囤积感，不服务于遗产管理。Archive 不一定是 Legacy，反之亦然。
- **子目录与活跃区镜像**：归档入口和活跃内容出口保持同一粒度。
- **删除 `Documents/`**：没有哪个源头的归档叫 "Documents"--若它是旧个人文件，应镜像到对应 UserSpace 子类；若它是旧项目资料，应进 `Archive/Projects/`。"Documents"作为分类词在任何层级都回答不了"谁写的、干什么用的、为什么在这里"。
- **`Exports` -> `Snapshot`**：Exports 语义模糊，Snapshot 更准确（状态快照）。

---

## 五、删除清单

- `Inbox/` 整个顶层目录（不创建替代；未决定归宿是用户的临时问题，不是结构问题）
- `State/` 整个顶层目录（语义不明；职责分流：软件配置 -> Software/Configs，凭证 -> UserSpace/Vault）
- `Control/Exports/`（语义模糊；导出快照作记录进 Inventory）
- `Software/PackageManagers/`（作者只用 Scoop，无需通用抽象层；Scoop 直接挂顶层）
- `Software/Toolchains/`（语义错位；被 `Devtool/langenv` 替代）
- `Software/Installed/`、`Software/Portable/`、`Software/Shared/`、`Software/Shims/`（v2 顶层安装方式轴取消；Installed/Portable 降为 `Apps/` 下子分类，Shared/Shims 删除）
- `Workspaces/` 顶层名（改名 `Projects/`，内部结构重设）
- `Archive/Documents/`（分类词无效）
- `Archive/Exports/` -> `Snapshot/`
- `Caches/` 下的 `Packages/`、`Builds/`、`Logs/`、`Downloads/`（见 Software 详述）

---

## 六、删除的 README 规则

- "不要仅通过大小写赋予含义；Windows 路径通常不区分大小写"--解决不存在的问题，作者没做过靠大小写传达信息的事。
- "使用稳定的全小写 ID"的具体措辞--场景理解错误。
- "记录可以描述现实；它们不一定具备重新创建的能力"--语义不明，"介于可执行配置和笔记之间"的位置不解决问题，只是为模糊性找体面说法。
- "chroot 描述的是你所拥有的内容，而不是 Windows 配置文件的虚假替代品"--立场对立。作者立场是主动重定向工程（哪怕软件不支持也想办法接管），v2 的 pragmatism 在作者看来是投降主义。

---

## 七、命名与格式

### 命名
- **PascalCase 已确认**用于结构目录，不修改。
- 结构目录之下保留官方厂商/产品名称。
- 用户控制的命名空间内（如 Devtool 内的用途分类 langenv/ide/agent、Projects 内的分组、项目、脚本）可用小写/snake_case。
- `Data/`、`Caches/` 下的镜像分类用 PascalCase 的 `Devtool`/`Apps`（对齐顶层结构目录）。

### 格式
- README 顶层契约表改为**缩进树形图**格式（参照 TREE.md 风格）。
- 禁止 markdown 表格（作者明确要求）。

---

## 八、待讨论

1. **`.META` 在分类层的具体内容**：形式不预先约定，待开发统一管理软件时定；当前只确立"贴分类层、按需、不进资产内部"的原则。
2. **统一管理软件本身**：如何消费 `.pool` 之上 / `.META` 中的语义、构建分类视图，属未来工程，不在本结构计划内。

---

## 九、不在范围内

- `.nixdows`：无可用的解释器，暂不处理。v1 的 `where's_my_home.nixdows` 作为设计参考保留，不试图复现。
- 双语文档：v2 已建立 EN/CN 镜像，v3 保持。
- 实际文件填充：只设计目录结构和文档，不填充真实数据。
- 项目文档归属：在项目 docs/ 或文档站项目 docs/，不属于本结构讨论。
