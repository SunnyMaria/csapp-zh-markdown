# 自学实验包与说明模板的差异

本页是整理者根据随仓库提供的官方压缩包所作的文件核对说明，不属于原实验文档译文。保留原包不作修改；下列信息来自包内 README、Makefile、代码和测试脚本的静态检查，未在本机编译或运行实验。

## Data Lab

- 实际文件名为 `datalab-handout.tar`。原 PDF 解压命令末尾多了一个句点，运行时应使用 `tar xvf datalab-handout.tar`，不要包含末尾句点。
- 随附 `bits.c` 的 13 道题与说明版本对应。原说明题目表中的几处笔误可由包内文件核对：`bitXor` 计算 `x^y`；`negate` 的合法运算符不含减号；函数名为 `isAsciiDigit`，范围是 `0x30 <= x <= 0x39`。
- `Makefile` 使用 `-m32`，编译环境需要具备 32 位编译和链接支持。

## Bomb Lab

- 随附的是公开自学包 `bomb.tar`，解压后的目录为 `bomb/`，包含 `README`、`bomb` 和 `bomb.c`。
- 原说明以课程定制包 `bombk.tar` 和目录 `bombk/` 为例；其中提到的 `writeup.pdf`、`writeup.ps` 未包含在这个自学包中，请阅读本仓库的中文 Markdown 说明。
- 官方实验页面说明，自学版已关闭向评分服务器报告的功能。课程文档中的提交与扣分流程是课程配置，不是本仓库的评分服务。

## Attack Lab

- `target1.tar` 对应说明中 `targetk.tar` 的 `k=1` 实例，包含两个目标程序、cookie 和辅助工具。
- 运行自学目标程序时使用 `-q`，避免联系不存在的评分服务器。不同实验实例的 cookie 和地址可能不同。

## Architecture Lab

- `archlab-handout.tar` 内还包含模拟器压缩包 `sim.tar`。
- 模拟器指南介绍默认 GUI 构建，但随附 `sim/Makefile` 注释了 `GUIMODE=-DHAS_GUI`。其 Tcl/Tk 配置仍保留，`TKINC` 指向 `/usr/include/tcl8.5`。
- 按包内 `sim/README` 和当前环境配置 GUI 或 TTY 模式，不要仅根据指南就假定构建结果支持 GUI 的 `-g` 选项。

## Cache Lab

- 包内测试与说明一致：矩阵大小为 32×32、64×64 和 61×67。
- `driver.py` 的解释器行是 `/usr//bin/python`，并使用 Python 2 的 `print "..."` 语法。它不是可直接交给 Python 3 执行的脚本。
- README 中的 `make`、`./test-csim`、`./test-trans -M ... -N ...` 是包内提供的构建与分项测试入口。总评脚本还需要匹配的解释器环境。

## Shell Lab

- 包内实际有 `trace01.txt` 至 `trace16.txt` 共 16 份测试；Makefile 也包含 `test16` 和 `rtest16`。README 中“15 份”的描述没有同步更新，应以实际文件和中文实验说明中的 16 份为准。
- 原说明提交路径使用 `15213-f01`，包内 Makefile 使用 `15213-f02`。两者都是历史 CMU 课程路径，自学者不应将其当作可以使用的提交服务。

## Malloc Lab

- 包内只附带 `short1-bal.rep` 和 `short2-bal.rep` 两份短测试。README 提供的短测试入口为：

```sh
./mdriver -V -f short1-bal.rep
./mdriver -V -f short2-bal.rep
```

- `config.h` 的默认测试目录是：

  ```text
  /afs/cs/project/ics2/im/labs/malloclab/traces/
  ```

  其中列出的 11 份正式跟踪文件没有包含在这个自学包中。因此，仅靠本包运行默认完整测试 `./mdriver -V`，无法获得说明所述的整套测试。使用完整测试需另有相应跟踪文件并配置路径。
- `Makefile` 使用 `-m32`，编译环境需要具备 32 位编译和链接支持。
- 包内要求的 8 字节对齐、性能评分权重 0.6 和参考吞吐量 600 Kops/s 与原说明一致。

## Proxy Lab

- 原说明写提交文件为 `../proxylab-handin.tar`，随附 Makefile 实际生成 `../$(USER)-proxylab-handin.tar`，文件名带用户名前缀。
- 并发测试会启动 `nop-server.py`，其解释器行固定为 `/usr/bin/python`。缺少这个解释器路径时，需要先解决运行环境问题，不能直接把脚本无法启动判断为代理并发逻辑失败。
- 包内评分仍是基本正确性 40 分、并发 15 分、缓存 15 分，与说明一致。
