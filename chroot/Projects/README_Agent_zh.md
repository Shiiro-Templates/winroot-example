---
AuthorType: Agent
TargetType: Agent
---

# Projects

你**开发、维护**的项目。你是作者/贡献者，代码被版本控制跟踪。
独立顶层，不回 UserSpace 下--它是活跃工作的主战场，体量和 Software/Archive 对等。
只使用、不维护的源码不进这里，进 `../Software/Build2Use/`。

仓库按可见性/归属分组，加一个无 git 的 Playground：

```text
Projects/
├───Playground/        # 不用 git 的草稿实验区
├───Private/           # 私有仓库
│   ├───Demos/         #   演示项目
│   ├───Tools/         #   工具类
│   └───Products/      #   产品类
├───Public/            # 公开仓库
│   ├───Demos/         #   演示
│   ├───Own-Dev/       #   自己主导、严格控制，主要工作为开发
│   ├───Own-Community/ #   已进入 Steward、社区驱动，主要工作维持方向
│   ├───Forks/         #   fork 并维护的项目（有自己的改动、长期跟进）
│   ├───Mirrors/       #   为学习同步的只读镜像（看源码用，不贡献）
│   └───Contrib/       #   临时贡献（要 push 回 upstream，不长期维护）
└───Orgs/              # 所属组织的仓库
```

每个项目作为一个整体资产，内部由 git 管，我们不碰。
`.META` 服务于分类层（描述其下有哪些资产单元），**不进资产内部**--
`.META`（和 `.pool`）永远贴着分类层，离资产至少一个目录的距离。`.META` 按需放，不强制每个分类层都有。

项目文档在项目内的 `docs/`，或对应文档站项目的 `docs/`。
仓库规模大时，可在分组下按 forge/owner 进一步组织（如 `Orgs/<org>/<repo>/`），按需建，不预约定。
