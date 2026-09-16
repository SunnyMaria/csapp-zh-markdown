# Shell Lab：编写你自己的 Unix Shell

原文：[官方实验说明](https://csapp.cs.cmu.edu/3e/shlab.pdf)  
实验包：[shlab-handout.tar](shlab-handout.tar)

自学包说明：[运行配置与原说明的差异](../COMPATIBILITY.md)

## 课程信息

CS 213，2002 年秋季

实验作业 L5：编写你自己的 Unix Shell

布置：10 月 24 日；截止：10 月 31 日（星期四）晚上 11:59

Harry Bovik（bovik@cs.cmu.edu）是本作业负责人。

## 引言

本作业的目的是让你更加熟悉进程控制和信号的概念。你将通过编写一个支持作业控制的简单 Unix shell 来完成这一目标。

## 事务安排

你最多可以与另一名同学组队完成本作业。唯一的“提交”方式是电子提交。任何澄清和作业修订都会发布在课程网页上。

## 发放说明

> **SITE-SPECIFIC：** 此处应插入说明教师如何向学生发放 `shlab-handout.tar` 文件的段落。（译注：这是课程占位符，原文未提供本课程实例内容。）以下是 CMU 使用的说明。

首先，将 `shlab-handout.tar` 复制到你计划工作的受保护目录（实验目录）中。然后执行：

- 输入命令 `tar xvf shlab-handout.tar` 展开 tar 文件。
- 输入命令 `make` 编译并链接一些测试例程。
- 在 `tsh.c` 顶部的头部注释中填写你的组员姓名和 Andrew ID。

查看 `tsh.c`（tiny shell）文件，你会看到其中包含一个简单 Unix shell 的可运行骨架。为了帮助你开始，我们已经实现了不太有趣的函数。你的任务是完成下面列出的其余空函数。作为合理性检查，我们列出了这些函数在参考实现中的大致代码行数（参考实现包含大量注释）：

- `eval`：解析并解释命令行的主例程。[70 行]
- `builtin_cmd`：识别并解释内置命令：`quit`、`fg`、`bg` 和 `jobs`。[25 行]
- `do_bgfg`：实现 `bg` 和 `fg` 内置命令。[50 行]
- `waitfg`：等待前台作业完成。[20 行]
- `sigchld_handler`：捕获 SIGCHILD 信号。[80 行]
- `sigint_handler`：捕获 SIGINT（ctrl-c）信号。[15 行]
- `sigtstp_handler`：捕获 SIGTSTP（ctrl-z）信号。[15 行]

每次修改 `tsh.c` 后，都输入 `make` 重新编译。运行 shell 时，在命令行输入 `tsh`：

```text
unix> ./tsh
tsh> [type commands to your shell here]
```

## Unix Shell 概述

shell 是代表用户运行程序的交互式命令行解释器。shell 不断打印提示符，从 `stdin` 等待命令行，然后根据命令行内容执行某些操作。

命令行是一串由空白分隔的 ASCII 文本单词。命令行的第一个单词要么是内置命令的名称，要么是可执行文件的路径名。其余单词是命令行参数。如果第一个单词是内置命令，shell 会立即在当前进程中执行它。否则，该单词被视为可执行程序的路径名；此时 shell 会创建一个子进程，然后在子进程上下文中加载并运行该程序。解释一条命令行所创建的子进程统称为一个作业。通常，一个作业可以由多个通过 Unix 管道连接的子进程组成。

如果命令行以 `&` 结尾，作业就在后台运行，也就是说 shell 不等待作业终止，就打印提示符并等待下一条命令。否则，作业就在前台运行，也就是说 shell 等待作业终止后才等待下一条命令。因此，在任意时刻最多只有一个作业可以在前台运行，但可以有任意多个作业在后台运行。

例如，输入命令行：

```text
tsh> jobs
```

会让 shell 执行内置的 `jobs` 命令。输入：

```text
tsh> /bin/ls -l -d
```

会让 `ls` 程序在前台运行。按照约定，shell 保证程序开始执行其主例程时：

```c
int main(int argc, char *argv[])
```

`argc` 和 `argv` 参数具有以下值：

```text
argc == 3,
argv[0] == ``/bin/ls'',
argv[1]== ``-l'',
argv[2]== ``-d''.
```

也可以输入：

```text
tsh> /bin/ls -l -d &
```

让 `ls` 程序在后台运行。

Unix shell 支持作业控制，使用户能够在后台和前台之间移动作业，并改变作业中进程的状态（运行、停止或终止）。输入 `ctrl-c` 会向前台作业中的每个进程发送 SIGINT 信号。SIGINT 的默认动作是终止进程。同样，输入 `ctrl-z` 会向前台作业中的每个进程发送 SIGTSTP 信号。SIGTSTP 的默认动作是将进程置于停止状态；进程会保持该状态，直到收到 SIGCONT 信号而被唤醒。Unix shell 还提供支持作业控制的各种内置命令，例如：

- `jobs`：列出正在运行和已停止的后台作业。
- `bg <job>`：将已停止的后台作业变为运行中的后台作业。
- `fg <job>`：将已停止或正在运行的后台作业变为在前台运行。
- `kill <job>`：终止一个作业。

## `tsh` 规范

你的 `tsh` shell 应具备以下功能：

- 提示符应为字符串 `tsh> `。
- 用户输入的命令行应由一个名称和零个或多个参数组成，各项由一个或多个空格分隔。如果名称是内置命令，`tsh` 应立即处理它并等待下一条命令行。否则，`tsh` 应假设名称是可执行文件的路径，并在一个初始子进程的上下文中加载和运行它（在此上下文中，术语“作业”指这个初始子进程）。
- `tsh` 不需要支持管道（`|`）或输入/输出重定向（`<` 和 `>`）。
- 输入 `ctrl-c`（`ctrl-z`）应使 SIGINT（SIGTSTP）信号发送到当前前台作业及其所有后代（例如它创建的子进程）。如果没有前台作业，信号不应产生作用。
- 如果命令行以 `&` 结尾，`tsh` 应在后台运行作业；否则应在前台运行。
- 每个作业既可用进程 ID（PID）识别，也可用作业 ID（JID）识别。JID 是由 `tsh` 分配的正整数。命令行中 JID 必须以 `%` 为前缀。例如，`%5` 表示 JID 5，而 `5` 表示 PID 5。（我们已提供操作作业列表所需的全部例程。）
- `tsh` 应支持以下内置命令：
  - `quit` 命令终止 shell。
  - `jobs` 命令列出所有后台作业。
  - `bg <job>` 命令通过发送 SIGCONT 信号重新启动 `<job>`，然后在后台运行它。`<job>` 参数可以是 PID 或 JID。
  - `fg <job>` 命令通过发送 SIGCONT 信号重新启动 `<job>`，然后在前台运行它。`<job>` 参数可以是 PID 或 JID。
- `tsh` 应回收其所有僵尸子进程。如果某个作业因收到未捕获的信号而终止，`tsh` 应识别该事件，并打印包含作业 PID 以及导致终止的信号说明的消息。

## 检查你的工作

我们提供了一些工具帮助你检查工作。

**参考实现。** Linux 可执行文件 `tshref` 是 shell 的参考实现。运行它可以解决关于 shell 行为的疑问。你的 shell 输出应与参考实现完全相同（当然，PID 除外，因为 PID 会随运行而变化）。

**Shell 驱动程序。** `sdriver.pl` 程序以子进程运行 shell，根据跟踪文件的指示向它发送命令和信号，并捕获和显示 shell 的输出。

使用 `-h` 参数查看 `sdriver.pl` 的用法：

```text
unix> ./sdriver.pl -h
Usage: sdriver.pl [-hv] -t <trace> -s <shellprog> -a <args>
Options:
  -h            Print this message
  -v            Be more verbose
  -t <trace>    Trace file
  -s <shell>    Shell program to test
  -a <args>     Shell arguments
  -g            Generate output for autograder
```

我们还提供了 16 个跟踪文件（`trace{01-16}.txt`），你将结合 shell 驱动程序使用它们测试 shell 的正确性。编号较小的跟踪文件只进行非常简单的测试，编号较大的测试更复杂。

例如，可以使用 `trace01.txt` 运行你的 shell：

```text
unix> ./sdriver.pl -t trace01.txt -s ./tsh -a "-p"
```

（`-a "-p"` 参数告诉 shell 不要输出提示符），或者：

```text
unix> make test01
```

类似地，要将结果与参考 shell 比较，可以运行：

```text
unix> ./sdriver.pl -t trace01.txt -s ./tshref -a "-p"
```

或者：

```text
unix> make rtest01
```

作为参考，`tshref.out` 给出了参考实现在所有竞态测试中的输出。与手动对所有跟踪文件运行 shell 驱动程序相比，这可能更方便。

跟踪文件的妙处在于，它们生成的输出与交互运行 shell 时得到的输出相同（开头会有一条用于标识跟踪的注释）。例如：

```text
bass> make test15
./sdriver.pl -t trace15.txt -s ./tsh -a "-p"
#
# trace15.txt - Putting it all together
#
tsh> ./bogus
./bogus: Command not found.
tsh> ./myspin 10
Job (9721) terminated by signal 2
tsh> ./myspin 3 &
[1] (9723) ./myspin 3 &
tsh> ./myspin 4 &
[2] (9725) ./myspin 4 &
tsh> jobs
[1] (9723) Running    ./myspin 3 &
[2] (9725) Running    ./myspin 4 &
tsh> fg %1
Job [1] (9723) stopped by signal 20
tsh> jobs
[1] (9723) Stopped    ./myspin 3 &
[2] (9725) Running    ./myspin 4 &
tsh> bg %3
%3: No such job
tsh> bg %1
[1] (9723) ./myspin 3 &
tsh> jobs
[1] (9723) Running    ./myspin 3 &
[2] (9725) Running    ./myspin 4 &
tsh> fg %1
tsh> quit
bass>
```

## 提示

- 阅读教材第 8 章（异常控制流）的每一个字。
- 用跟踪文件指导 shell 的开发。从 `trace01.txt` 开始，确保 shell 产生与参考 shell 完全相同的输出，然后继续处理 `trace02.txt`，依此类推。
- `waitpid`、`kill`、`fork`、`execve`、`setpgid` 和 `sigprocmask` 函数会非常有用。`waitpid` 的 `WUNTRACED` 和 `WNOHANG` 选项也很有用。
- 实现信号处理程序时，务必使用 `kill` 函数的 `-pid` 而不是 `pid`，将 SIGINT 和 SIGTSTP 信号发送到整个前台进程组。`sdriver.pl` 会测试这一错误。
- 作业中比较棘手的一点是决定 `waitfg` 和 `sigchld_handler` 函数之间的工作分配。我们建议：在 `waitfg` 中使用围绕 `sleep` 函数的忙等待循环；在 `sigchld_handler` 中恰好调用一次 `waitpid`。虽然也可以在两个函数中都调用 `waitpid`，但这会非常容易混淆；把所有回收操作放在处理程序中更简单。
- 在 `eval` 中，父进程必须在创建子进程之前使用 `sigprocmask` 阻塞 SIGCHLD 信号，并在调用 `addjob` 将子进程加入作业列表后再次使用 `sigprocmask` 解除阻塞。由于子进程会继承父进程的阻塞向量，因此子进程必须在执行新程序前解除 SIGCHLD 的阻塞。

  父进程必须这样阻塞 SIGCHLD 信号，以避免子进程在父进程调用 `addjob` 之前就被 `sigchld_handler` 回收（从而从作业列表中删除）的竞态条件。
- `more`、`less`、`vi` 和 `emacs` 等程序会对终端设置做奇怪的事情。不要从你的 shell 运行这些程序。使用 `/bin/ls`、`/bin/ps` 和 `/bin/echo` 等简单的文本程序。
- 当你从标准 Unix shell 运行自己的 shell 时，你的 shell 运行在前台进程组中。如果你的 shell 创建子进程，默认情况下子进程也会属于前台进程组。由于输入 `ctrl-c` 会向前台进程组中的每个进程发送 SIGINT，因此输入 `ctrl-c` 会同时发送给你的 shell 以及 shell 创建的每个进程，这显然不正确。

  解决办法是：`fork` 之后、`execve` 之前，子进程应调用 `setpgid(0, 0)`，这会把子进程放入一个新的进程组，其组 ID 与子进程 PID 相同。这样前台进程组中就只有一个进程，即你的 shell。输入 `ctrl-c` 时，shell 应捕获产生的 SIGINT，然后将其转发给适当的前台作业（更准确地说，是包含前台作业的进程组）。

## 评分

总分最高为 90 分，分配如下：

- **80 分，正确性：** 16 个跟踪文件，每个 5 分。
- **10 分，风格：** 我们期望你写出良好注释（5 分），并检查每一个系统调用的返回值（5 分）。

你的 shell 将在 Linux 机器上使用实验目录中包含的同一 shell 驱动程序和跟踪文件进行正确性测试。除以下两点外，你的 shell 在这些跟踪上的输出应与参考 shell 完全相同：

- PID 可以不同，而且确实会不同。
- `trace11.txt`、`trace12.txt` 和 `trace13.txt` 中 `/bin/ps` 命令的输出会因运行而不同。不过，`/bin/ps` 输出中任何 `mysplit` 进程的运行状态应相同。

## 提交说明

> **SITE-SPECIFIC：** 此处应插入说明学生如何提交 `tsh.c` 文件的段落。（译注：这是课程占位符，原文未提供本课程实例内容。）以下是 CMU 使用的说明。

- 确保在 `tsh.c` 的头部注释中填写姓名和 Andrew ID。
- 创建如下形式的组名：
  - 如果独自完成，组名为你的 Andrew ID，即 `ID`；
  - 如果两人组队，组名为 `ID1+ID2`，其中 `ID1` 是第一位组员的 Andrew ID，`ID2` 是第二位组员的 Andrew ID。

我们要求按此方式创建组名，以便自动评分作业。

- 提交 `tsh.c` 文件：

```text
make handin TEAM=teamname
```

其中 `teamname` 是上述形式的组名。

- 提交后，如果发现错误并想提交修订版本，输入：

```text
make handin TEAM=teamname VERSION=2
```

每次提交都递增版本号。

- 应通过查看以下目录验证提交：

```text
/afs/cs.cmu.edu/academic/class/15213-f01/L5/handin
```

你对该目录拥有列出和插入权限，但没有读或写权限。

祝好运！
