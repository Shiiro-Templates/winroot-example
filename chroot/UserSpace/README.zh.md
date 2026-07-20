---
//把现在所有的READEME改名为README_Agent.md，它们适合AI读而不是人类读
//人类读的文档不需要傻逼限制和澄清，因为你丫的管不了，限制人类的方法，排除惩罚，只有一个就是本身语义鲜明舒适，否则你是在脱裤子放屁让用户削足适履
//README_Agent_zh.md
// 我会修改Agent输出的文档，以真正适配人类阅读，不过那是当前目录语义已经完善的情况做的收尾工作
//真正的README后面再写
Author: Agent
Target: Agent
---

# UserSpace

用户的操作空间。"孩子那里不是家"--UserSpace 不是归宿意义上的"家"，
是用户操作和资产的所在。前六个子目录是 Windows Shell Folder 重定向目标，
后两个是自主内容，最后是凭证库。
// 没有用树状目录，你找死吗，所有目录语义用制表符画出的树，不得用列表，不得用表格
- `Desktop`：Shell Folder 重定向。//这个先不需要，我们不讨论，删掉即可，无需记录此变更，没有理由
- `Documents`：Shell Folder 重定向。
- `Downloads`：Shell Folder 重定向（用户发起下载的入口）。
---这三个恢复我v1版本的Storage/ 语义 原因：大，重，胖，不能用文本编辑器打开，为什么不用media?你可以考虑一下安卓的media语义都被滥用成啥样了，storage就是storage，有拓展性
- `Music`：Shell Folder 重定向。
- `Pictures`：Shell Folder 重定向。
- `Videos`：Shell Folder 重定向。
---
- `Knowledge`：自主内容--笔记、wiki、Obsidian vault。
- `Collections`：自主内容--书签、Github Stars 等。
- `Vault`：凭证库--KeePass/1Password 等的库文件。//见我对tree的修改注释，改Secrets

Shell Folders 直接沿用 Windows 原始默认命名，不套 `Storage/` 层，也不改名。
它们是 Windows 资源管理器左侧栏认识的名字，通过注册表/属性页映射。
凭证是用户资产，由专门软件管，不单独顶层、不进 Control、不混软件配置；
独立加密/备份策略由对应软件负责。

`Downloads` 是唯一下载入口（用户发起）。机器管理的可重下载工件不存在独立目录--
它们跟着各自的软件/管理器走（如 `../Software/Scoop/cache/`）。
