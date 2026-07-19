# Control

`chroot` 的环境控制层（v1 `Settings/` 语义）。它控制这个 chroot 环境本身--
环境变量、脚本、配置文件、命令日志。**它不负责装软件配置**（各软件的 config 进 `../Software/Configs/`）。

- `Environment`：必须注入系统级环境变量的配置。放的是"不塞进系统级就容易出故障的"配置；
  树内项目级环境变量用 direnv，不在这里。
- `Inventory`：已安装软件/受管资源记录。人写的记录或工具生成的快照都说清楚用途即可。
- `Profiles`：shell/编辑器/终端/工具设置的备份。
- `Scripts`：启动、设置、验证、维护脚本。
- `Templates`：可复用的配置和项目模板。
- `Logs`：ctl-log（命令执行记录）及其他运维日志。

凭证放 `../UserSpace/Vault`（KeePass/1Password 管），不放这里。
v1 `Settings/configfile/` 中环境控制相关的配置文件留 Control；
各软件自己的配置不进 Control，进 `../Software/Configs/`。
尽量使用文本格式，并通过 `%CHROOT_ROOT%` 而非盘符引用根目录。
