# 参考树

```text
─chroot/
    ├───README_Agent_zh.md
    ├───TREE_Agent_zh.md
    ├───glossary-map.zh-agent.md
    ├───Control/                    # 环境控制层
    │   ├───README_Agent_zh.md
    │   ├───.META/                  # Control 层元数据
    │   ├───Environment/            # 本树需要的系统/用户级环境变量和环境配置
    │   ├───MotivationIndex/        # 需求记录：需求（根源）-> Projects 里的开发或 Software 里在用的软件
    │   ├───Profiles/               # shell/编辑器/终端/工具设置的备份，即 configfiles
    │   ├───Scripts/                # 启动、设置、验证、维护脚本
    │   ├───Templates/              # 可复用的配置和项目模板
    │   └───Logs/                   # ctl-log（命令执行记录）及运维日志
    ├───Software/                   # 软件本体、配置、数据、缓存、包管理器、构建消费品
    │   ├───README_Agent_zh.md
    │   ├───Devtool/                # 开发工具集
    │   │   ├───envs/               # 开发环境（语言运行时、平台 SDK、框架工具链）
    │   │   │   └───.pool/          #   存储边界，其下散装各语言工具链
    │   │   ├───ide/                # VS Code 等
    │   │   │   └───.pool/
    │   │   └───agent/              # Claude Code、OpenClaw 这类 harness+Agent
    │   │       └───.pool/
    │   ├───Apps/                   # 非开发应用软件
    │   │   ├───Installed/          #   installer 装的
    │   │   │   └───.pool/
    │   │   │       └───<appname the installer set>/
    │   │   └───Portable/           #   解压即用
    │   │       └───.pool/
    │   │           └───<appname unzipped>/
    │   ├───Build2Use/              # 从源码构建来用的软件
    │   │   └───.pool/
    │   │       └───<software>/     #   散装，含源码与构建产物
    │   ├───Configs/                # 软件配置/设置，与 Data 并列（不进 Control）
    │   │   ├───Devtool/
    │   │   │   └───<tool>/         #   配置布局由工具定；Local/Roaming 按需作锚点
    │   │   └───Apps/
    │   │       └───<app>/
    │   ├───Data/                   # 装在工具上的功能载荷，一般不随工具卸载而抹除
    │   │   ├───Devtool/
    │   │   │   └───.pool/          #   VS Code 扩展、npm/cargo 全局包、插件
    │   │   └───Apps/
    │   │       └───.pool/
    │   ├───Caches/                 # 仅按消费关系归类
    │   │   ├───Devtool/
    │   │   │   └───.pool/          #   开发工具缓存，按工具名分桶
    │   │   ├───Apps/
    │   │   │   └───.pool/          #   应用缓存，按应用名分桶
    │   │   └───Temp/               #   %TEMP% 重定向，非管理目标，不用 .pool
    │   └───Scoop/                  # 包管理器根，挂顶层，内部自管
    ├───UserSpace/                  # 用户的操作空间
    │   ├───README_Agent_zh.md
    │   ├───Downloads/              # Shell Folder 重定向（用户发起下载入口；流入，非归宿）
    │   ├───Storage/                # 大、重、胖的 Shell Folder 重定向目标
    │   │   ├───Documents/          #   文档
    │   │   ├───Music/              #   音频
    │   │   ├───Pictures/           #   图片
    │   │   └───Videos/             #   视频
    │   ├───Knowledge/              # 自主内容：笔记、wiki、Obsidian vault
    │   ├───Collections/            # 自主内容：书签、Github Stars 等（由其它开发中的项目管理）
    │   └───Private/                # 凭证库：KeePass/1Password 等的库文件
    ├───Projects/                   # 你开发维护的项目
    │   ├───README_Agent_zh.md
    │   ├───Playground/             # gitless scratch，无 git 的草稿/实验
    │   ├───Private/                # 私有仓库
    │   │   ├───Demos/
    │   │   ├───Tools/
    │   │   └───Products/
    │   ├───Public/                 # 公开仓库
    │   │   ├───Demos/
    │   │   ├───Own-Dev/            # 自己主导，严格控制，主要工作为开发
    │   │   ├───Own-Community/      # 已进入 Steward，社区驱动，主要工作维持方向
    │   │   ├───Forks/              # fork 并维护的项目
    │   │   ├───Mirrors/            # 为学习同步的只读镜像
    │   │   └───Contrib/            # 临时贡献，不长期维护
    │   └───Orgs/                   # 组织仓库
    └───Archive/                    # 暂离的材料，注意力管理工具
        ├───README_Agent_zh.md
        ├───Projects/               # ← Projects 的归档
        ├───Knowledge/              # ← UserSpace/Knowledge 的归档
        ├───Software/               # 有意保留的安装包、软件副本
        └───Snapshot/               # 从服务/应用导出的状态快照
```

仅预创建了稳定的语义分类。在产品、源码、项目或收藏实际需要时才添加子目录。
传统安装器和包管理器可以在对应的 `Software` 边界下保留自己的命名和内部结构。
`.pool` 与 `.META` 按需出现，贴着分类层，离资产至少一个目录。
