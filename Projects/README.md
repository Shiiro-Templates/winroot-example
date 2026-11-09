---
AuthorType: Human
TargetType: Human
---

# Projects

```tree
Projects/
├───Playground/        # 无 git 的草稿与随手实验区
├───Private/           # 私有仓库
│   ├───Demos/         #   概念验证与演示项目
│   ├───Tools/         #   自用小工具与脚本库
│   └───Products/      #   完整产品级项目
├───Public/            # 公开仓库
│   ├───Demos/         #   公开演示与示例
│   ├───Own-Dev/       #   自己主导、严格控制，重心在于主力开发
│   ├───Own-Community/ #   已步入正轨（Steward）、社区驱动，重心在于把控方向
│   ├───Forks/         #   fork 并长期维护的魔改分支
│   ├───Mirrors/       #   为了研读源码而同步的只读镜像
│   └───Contrib/       #   临时贡献（PR 即止，不长期跟进）
└───Orgs/              # 所属组织的协作仓库
```

## 建议

- 如果你拉取某个开源项目只是为了本地 build 出可执行文件当工具用，将它归入 `../Software/Build2Use/`。
- 当叶子目录的仓库数量膨胀时，可以在分类下按需插入一层 `<owner>/` 或 `<forge>/` 子目录做二次归拢。

<!--@Nyashiiro::Note
To-Agent:
- 每个具体的项目仓库及 `Playground/` 下的独立实验目录内部由其自身的工具接管
- **分类层 `.META` 按需出现**：若需记录某分类下各项目的标签或状态元数据，将 `.META/` 建在分类层（如 `Private/Tools/.META/`），与具体项目目录并列；仓库内部的 `.META` 为该仓库工具链所有。
- **项目文档就地维护**：具体项目的文档直接放在该项目仓库内部的 `docs/`（或其对应的文档站项目）中，不往外层的 `../UserSpace/Knowledge/` 拆分。
-->

## 设计思路

- Attention Budgeting：让目录结构直接反映你对不同代码的**心理契约与维护负担**
- 给灵光一现留一块飞地：`Playground` 作为灵感的 `inbox`，降低初次执行的阻力；无 `git` （git init作为搬迁信号）建议视为硬契约，以免游乐场成为储物箱