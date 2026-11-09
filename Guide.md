---
AuthorType: Human
TargetType: Human
---
# winroot-example

## Mental Model
### 盘符之上的自主命名空间
Windows 没有直观的语义根目录，取而代之的是主文件夹与盘符。主文件夹的软件生态支持半斤八两，而盘符根目录下又总是被系统与各类软件乱塞东西，有些甚至无法移动。

`winroot-example` 是这整个卷的**语义根**（借用 `chroot` 的“换根”意象，不涉及访问隔离）
Windows 在卷根自动生成的系统产物留在它门外；该卷上一切由你主动纳管的内容，全部收束在此目录之下，构建出一棵自主决定布局、不受外部软件干扰的目录树。

### 设计依据：操作语义优先
在 `winroot` 中
**目录是有明确操作语义的归宿。**
当你需要为一个新条目寻找位置时，只需看清三件事：**谁拥有它的结构、它在工作流中扮演什么角色、它的生命周期是怎样的。**

---

## First Impression
### 顶层结构
打开 `winroot-example/`：

```text
winroot-example/
├── Control/        # 环境变量、脚本、配置文件源件、命令日志、需求记录
├── Software/       # 软件本体、运行配置、功能载荷、缓存、包管理器、源码构建消费品
├── UserSpace/      # 用户操作空间：自主知识内容、私人文件等 
├── Projects/       # 研发工作区：你开发与维护的源码项目
└── Archive/        # 暂离活跃视野的归档材料与状态快照
```

#### `Control/` · 环境控制面
掌控整个目录树运转的元配置与操作中心：
- `MotivationIndex/` 记录需求溯源（某个软件或项目是为了解决什么根源需求而引入的）；
- `Profiles/` 存放你亲手维护的 Shell、编辑器、终端等高价值 configfiles 备份；
- `Environment/` 与 `Scripts/` 承载本树所需的环境变量与启停维护脚本（脚本与记录中统一使用 `%CHROOT_ROOT%` 引用根路径，避免硬编码盘符）；
- 注意：这里只管环境基座，具体软件的庞杂配置不进 `Control/`，而是归入 `Software/Configs/`。

#### `Software/` · 软件与运行时衍生
承接一切“拿来使用的工具与应用”，并将软件本体与其运行时状态解耦：
- 开发工具进 `Devtool/`（按角色切分为 `envs` / `ide` / `agent` / `MCP`）；非开发应用进 `Apps/`（按安装模型切分为 `Installed` / `Portable`）；包管理器如 `Scoop/` 直接挂在顶层内部自管，因为我很清楚我会用 Scoop 装什么。
- 软件运行时的配置（`Configs/`）、功能载荷（`Data/`）与缓存（`Caches/`）并列分流，各自拥有独立生命周期。

#### `UserSpace/` · 用户操作与数据空间
将“系统默认入口”与“自主构建的数字资产”剥离：
- `Downloads/`（流入入口，相当于inbox）与 `Storage/`（承接大体积的 `Documents` / `Music` / `Pictures` / `Videos`）专门作为 Windows Shell Folders 的重定向目标；
- `Knowledge/` 存放你自主维护的笔记、Wiki 等；
- `Private/` 存放 KeePass / 1Password 等凭证库文件，由专门的密码软件接管.

#### `Projects/` · 创造与维护
仅收纳需要你编写、修改并纳入版本控制追踪的源码仓库（以及 `Playground/` 中的无 Git 临时实验草稿）。按仓库公开性与你在其中的维护角色（`Own-Dev` / `Own-Community` / `Forks` / `Mirrors` / `Contrib`）组织

#### `Archive/` · 时光储藏室
与活跃工作区同构（下设 `Projects`、`Knowledge`、`Software`、`Snapshot`），用于移出当前不再关注但有意保留的材料，降低日常检索与浏览的心智负担。

---

## Design Pillars
### 用 `.pool` 与 `.META` 隔离“管理”与“实体”

为了让目录树既能保持清晰的结构化语义，又不至于去强行拆改第三方软件或项目的内部结构，我们在**分类层**与**具体资产单元**之间引入了两个元语义目录，两者通常不共存

- **位置边界**：`.pool` 与 `.META` 紧贴着我们的**分类层**出现，离具体的资产单元一个目录单位


#### `.pool/` —— 表面整洁、内里自由的“收纳筐”

```tree
<用途分类>/                   # 【管理语义层】可放 README 与分类元数据，供人与管理工具解析
└── .pool/                   # 【存储边界】gitignore (**/.pool/) 与 rgignore 在此截断
    └── <具体软件或资产>/     # 【散装存储层】软件自治领地，不被上层管理工具递归解析
```
- **结构化语义在 `.pool` 之上，`.pool` 是叶子**
- **何时不用 `.pool`**：
  - 不是我们的細粒度管理目标时：如 `Caches/Temp`（仅作 `%TEMP%` 整体重定向，不管内部）、Windows Shell Folders（路径由 WinAPI 决定，内部归系统管）。
  - 源码项目（`Projects/`）：需要被 Git 跟踪与全文检索，不用 `.pool`。

#### `.META/` —— 非 `.pool` 场景下的元数据容器
- 如果某层目录已经有了 `.pool/`，管理元数据直接与 `.pool/` 并列放置即可，无需另建
- 但在 `Projects/` 分类层或 `Docs/` 等没有 `.pool/`、且用户经常需要用资产管理软件或脚本直接打开整个文件夹浏览编排的场景下，散落的元资源文件会干扰视野——此时按需建立 `.META/` 收纳分类层元数据
```tree
<用途分类>/                  
├── .META/                  # 【管理语义层】可放 README 与分类元数据，供人与管理工具解析
└── <具体软件或资产>/        # 【资产实体层】具体的项目仓库或文档目录，保持平铺以便直接打开
```

### 命名建议
- 推荐在命名风格上产生一定差异，这样可以比较直观理解层次关系: 
  - `camelCase`: 小驼峰;
  -  `PascalCase`: 大驼峰; 
  - `snake_case`: 蛇形命名<!--@Nyashiiro::Note 或许我该整个介绍文章的链接来-->
- 就通用性和老软件兼容而言，建议使用 ASCII 英文并避免使用空格
- 骨架分类层：我比较喜欢使用 `PascalCase`（如 `MotivationIndex`、`Build2Use`）。
- 用户受控子空间：如 `Devtool` 下的 `envs` / `ide` / `agent`，或 `Projects` 内的自定义分组与个人脚本，我会用小写或 `snake_case`。
- 资产实体层：在结构目录（或 `.pool`）之下，原样保留官方厂商/产品名称或仓库原名即可。

---

## Emergent Rules & Edge Cases

### `Projects/` vs `Software/Build2Use/`：同样是源码，往哪放？
取决于你对这份源码的**使用意图**：
- 如果你拉取源码是为了修改、开发、提交演进 ➔ 它属于研发资产，进 `Projects/`（受版本控制，分类层用 `.META`）。
- 如果你拉取源码是因为官方没提供合适的构建包、只打算本地编译出来当工具使用而不参与维护 ➔ 它的源码连同编译产物整体视作“消费品”，进 `Software/Build2Use/.pool/<software>/`