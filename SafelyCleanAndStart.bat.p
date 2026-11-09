创建一个cmd脚本

当且仅当
- 当前工作目录不以 example 结尾
- 工作目录中有 SafetyProtect.Tag 文件
    - 其中含有与本脚本中硬编码一致的字符串
- 工作目录中没有以.p结尾的文件或目录
时工作

检查工作目录有没有.git：
有则检查当前git状态，如果有stash、暂存内容或脏工作区，拒绝并提醒用户
有 .git 而 git 命令不可用也立即报错

询问用户是否开始
- 首先移除SafetyProtect.Tag，若失败则立即停止
- 其次移除 .github ，.ci .vscode 目录
- 再递归移除所有含有
```gitignore
# Git Keeper
*
!.gitignore
```
的.gitignore文件

移除文件的行为均不做备份，没有就不管，不视为报错
如果文件存在但移除失败，若存在.git，在移除.git前停下，列出所有失败项和已移除项，并建议用户回滚
若不存在.git或已经在移除.git，视为出错，应当立即停下并报告出错位置


然后递归移除所有.gitkeeper文件，注意不是gitkeep，没打错字

最后移除.git，然后移除自身

如果因为报错退出，必须pause

- 使用纯英文注释和提示，不含 ASCII 字符之外的字符