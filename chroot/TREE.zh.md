# 参考树

```text
─chroot/
    ├───README.md
    ├───TREE.md
    ├───Control/                    # 设置、记录和自有配置
    │   ├───README.md
    │   ├───Environment/            # 环境变量和 PATH 设置
    │   ├───Inventory/              # 描述性软件/资源记录
    │   ├───Profiles/               # 有意保留在此的设置
    │   ├───Scripts/                # 启动和维护自动化脚本
    │   ├───Templates/              # 可复用的配置模板
    │   └───Exports/                # 导出的 Windows/应用配置
    ├───Software/                   # 实际软件本体
    │   ├───README.md
    │   ├───Installed/              # 传统安装器目录
    │   ├───Portable/               # 自包含的便携应用
    │   ├───Toolchains/             # SDK、运行时、编译器、开发工具
    │   ├───PackageManagers/        # 完整的包管理器根目录
    │   ├───Shared/                 # 共享运行时和组件
    │   └───Shims/                  # 稳定的 PATH 可见启动器
    ├───State/                      # 可控的持久软件状态
    │   ├───README.md
    │   ├───Apps/                   # 每应用的配置/数据
    │   ├───Tools/                  # 工具和包管理器状态
    │   ├───Shell/                  # 交互式 Shell 状态
    │   └───Secrets/                # 凭证（独立策略）
    ├───Cache/                      # 完全可丢弃的内容
    │   ├───README.md
    │   ├───Downloads/              # 机器管理的下载缓存
    │   ├───Packages/               # 依赖和包缓存
    │   ├───Builds/                 # 派生构建产物
    │   ├───Apps/                   # 每应用缓存
    │   ├───Logs/                   # 有限保留的诊断日志
    │   └───Temp/                   # 进程临时数据
    ├───Home/                       # 长期个人内容
    │   ├───README.md
    │   ├───Documents/
    │   ├───Knowledge/              # 笔记、Wiki 和知识库
    │   ├───Collections/
    │   │   └───Bookmarks/
    │   ├───Media/
    │   │   ├───Audio/
    │   │   ├───Images/
    │   │   └───Video/
    ├───Workspaces/                 # 活跃工作单元
    │   ├───README.md
    │   ├───Projects/               # 混合或非仓库项目
    │   ├───Repositories/           # 源码控制工作树
    │   ├───Labs/                   # 命名实验和原型
    │   └───Scratch/                # 明确短期的工作
    ├───Inbox/                      # 等待分类的内容
    │   ├───README.md
    │   ├───Downloads/              # 用户发起的下载
    │   ├───Imports/                # 暂存导入
    │   └───Drop/                   # 快速传输区
    └───Archive/                    # 非活跃的保留内容
        ├───README.md
        ├───Projects/
        ├───Documents/
        ├───Software/
        └───Exports/
```

仅预创建了稳定的语义分类。在产品、源码、项目或收藏实际需要时才添加子目录。
传统安装器和包管理器可以在对应的 `Software` 边界下保留自己的命名和内部结构。
