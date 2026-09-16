# 流水线处理器性能优化

**CS 349，2015 年夏季**  
**布置日期：6 月 6 日；截止日期：6 月 21 日 23:59**  
**本次作业负责人：Harry Bovik（`bovik@cs.cmu.edu`）**

## 1 引言

在本实验中，你将学习流水线化 Y86-64 处理器的设计与实现，并通过优化处理器和基准程序来最大限度地提高性能。你可以对基准程序进行任何保持语义不变的变换，也可以增强流水线处理器，或者二者同时进行。完成本实验后，你将深入理解代码与硬件之间的相互作用，以及这种相互作用如何影响程序性能。

实验分为三个部分，每个部分都需要单独提交。在 Part A 中，你将编写几个简单的 Y86-64 程序，并熟悉 Y86-64 工具。在 Part B 中，你将为 SEQ 模拟器扩展一条新指令。这两个部分将为 Part C 做准备。Part C 是本实验的核心，你将在其中优化 Y86-64 基准程序和处理器设计。

## 2 实验安排

本实验要求独立完成。

有关作业的任何说明和修订都会发布在课程网页上。

## 3 实验材料说明

> **特定站点内容：** 请在此处插入一段文字，说明学生应如何下载 `archlab-handout.tar` 文件。

1. 首先，将文件 `archlab-handout.tar` 复制到一个准备开展实验的（受保护）目录中。
2. 然后执行命令 `tar xvf archlab-handout.tar`。这会在该目录中解包出以下文件：`README`、`Makefile`、`sim.tar`、`archlab.pdf` 和 `simguide.pdf`。
3. 接着执行命令 `tar xvf sim.tar`。这会创建目录 `sim`，其中包含你的个人 Y86-64 工具副本。你的全部实验工作都将在该目录内完成。
4. 最后，进入 `sim` 目录并构建 Y86-64 工具：

```console
unix> cd sim
unix> make clean; make
```

## 4 Part A

本部分的工作目录是 `sim/misc`。

你的任务是编写并模拟下面三个 Y86-64 程序。这些程序所需的行为由 `examples.c` 中的示例 C 函数定义。务必在每个程序开头的注释中写上你的姓名和 ID。测试程序时，可以先用 YAS 汇编程序，再用指令集模拟器 YIS 运行。

在所有 Y86-64 函数中，都应遵循 x86-64 的函数参数传递、寄存器使用和栈使用约定。这包括保存并恢复所使用的所有被调用者保存寄存器。

### `sum.ys`：迭代求链表元素之和

编写一个 Y86-64 程序 `sum.ys`，以迭代方式求链表元素之和。程序应包含设置栈结构、调用函数并最终停止的代码。在这里，该函数应当是 Y86-64 代码形式的 `sum_list`，其功能与图 1 中的 C 函数 `sum_list` 等价。请使用下面这个含三个元素的链表测试程序：

```asm
# 链表示例
.align 8
ele1:
    .quad 0x00a
    .quad ele2
ele2:
    .quad 0x0b0
    .quad ele3
ele3:
    .quad 0xc00
    .quad 0
```

```c
/* 链表元素 */
typedef struct ELE {
    long val;
    struct ELE *next;
} *list_ptr;

/* sum_list - 求链表元素之和 */
long sum_list(list_ptr ls)
{
    long val = 0;
    while (ls) {
        val += ls->val;
        ls = ls->next;
    }
    return val;
}

/* rsum_list - sum_list 的递归版本 */
long rsum_list(list_ptr ls)
{
    if (!ls)
        return 0;
    else {
        long val = ls->val;
        long rest = rsum_list(ls->next);
        return val + rest;
    }
}

/* copy_block - 将 src 复制到 dest，并返回 src 的异或校验和 */
long copy_block(long *src, long *dest, long len)
{
    long result = 0;
    while (len > 0) {
        long val = *src++;
        *dest++ = val;
        result ^= val;
        len--;
    }
    return result;
}
```

**图 1：Y86-64 解答函数的 C 语言版本。** 参见 `sim/misc/examples.c`。

### `rsum.ys`：递归求链表元素之和

编写一个 Y86-64 程序 `rsum.ys`，以递归方式求链表元素之和。该程序应与 `sum.ys` 类似，但应使用递归求链表元素之和的函数 `rsum_list`，如图 1 中的 C 函数 `rsum_list` 所示。请使用测试 `sum.ys` 时使用的同一个三元素链表进行测试。

### `copy.ys`：将源数据块复制到目标数据块

编写一个程序 `copy.ys`，把一块内存中的字复制到另一块不重叠的内存区域，同时计算所有被复制字的异或（Xor）校验和。

程序应包含建立栈帧、调用函数 `copy_block` 并最终停止的代码。该函数应与图 1 中的 C 函数 `copy_block` 在功能上等价。请使用下面这个三元素源数据块和目标数据块测试程序：

```asm
.align 8
# 源数据块
src:
    .quad 0x00a
    .quad 0x0b0
    .quad 0xc00

# 目标数据块
dest:
    .quad 0x111
    .quad 0x222
    .quad 0x333
```

## 5 Part B

本部分的工作目录是 `sim/seq`。

Part B 的任务是扩展 SEQ 处理器，使其支持家庭作业题 4.51 和 4.52 中介绍的 `iaddq`。为加入这条指令，需要修改文件 `seq-full.hcl`。该文件实现了 CS:APP3e 教材中描述的 SEQ 版本，并声明了解答中需要使用的一些常量。

HCL 文件开头必须包含一个头部注释，其中应有以下信息：

- 你的姓名和 ID。
- 对 `iaddq` 指令所需计算的描述。可以参考 CS:APP3e 图 4-18 中对 `irmovq` 和 `OPq` 的描述。

### 构建并测试解答

修改完 `seq-full.hcl` 后，需要根据该 HCL 文件构建一个新的 SEQ 模拟器实例（`ssim`），然后进行测试。

#### 构建新的模拟器

可以使用 `make` 构建新的 SEQ 模拟器：

```console
unix> make VERSION=full
```

该命令构建的 `ssim` 版本会使用你在 `seq-full.hcl` 中指定的控制逻辑。为了减少输入，可以在 `Makefile` 中把 `VERSION` 设为 `full`。

#### 使用简单的 Y86-64 程序测试解答

初步测试时，建议在 TTY 模式下运行 `asumi.yo`（用于测试 `iaddq`）等简单程序，并将结果与 ISA 模拟结果比较：

```console
unix> ./ssim -t ../y86-code/asumi.yo
```

如果 ISA 测试失败，应在 GUI 模式下让模拟器单步执行，以调试实现：

```console
unix> ./ssim -g ../y86-code/asumi.yo
```

#### 使用基准程序重新测试解答

当模拟器能够正确执行小程序后，可以使用 `../y86-code` 中的 Y86-64 基准程序自动测试：

```console
unix> (cd ../y86-code; make testssim)
```

该命令会在基准程序上运行 `ssim`，并把最终处理器状态与高层 ISA 模拟得到的状态进行比较，以检查正确性。请注意，这些程序都不会测试新增的指令；这里仅仅是确认你的解答没有给原有指令引入错误。更多细节参见 `../y86-code/README`。

#### 执行回归测试

当基准程序能够正确执行后，应运行 `../ptest` 中覆盖范围很广的回归测试。要测试除 `iaddq` 和 `leave` 之外的所有内容，请执行：

```console
unix> (cd ../ptest; make SIM=../seq/ssim)
```

要测试 `iaddq` 的实现，请执行：

```console
unix> (cd ../ptest; make SIM=../seq/ssim TFLAGS=-i)
```

有关 SEQ 模拟器的更多信息，请参阅配套文档《CS:APP3e Y86-64 处理器模拟器指南》（`simguide.pdf`）。

```c
/*
 * ncopy - 将 src 复制到 dst，并返回 src 数组中
 *         正整数的个数。
 */
word_t ncopy(word_t *src, word_t *dst, word_t len)
{
    word_t count = 0;
    word_t val;

    while (len > 0) {
        val = *src++;
        *dst++ = val;
        if (val > 0)
            count++;
        len--;
    }
    return count;
}
```

**图 2：`ncopy` 函数的 C 语言版本。** 参见 `sim/pipe/ncopy.c`。

## 6 Part C

本部分的工作目录是 `sim/pipe`。

图 2 中的 `ncopy` 函数把含 `len` 个元素的整数数组 `src` 复制到不重叠的 `dst`，并返回 `src` 中正整数的个数。图 3 给出了 `ncopy` 的基准 Y86-64 版本。文件 `pipe-full.hcl` 包含 PIPE 的 HCL 代码副本，以及常量值 `IIADDQ` 的声明。

Part C 的任务是修改 `ncopy.ys` 和 `pipe-full.hcl`，目标是让 `ncopy.ys` 尽可能快地运行。

需要提交两个文件：`pipe-full.hcl` 和 `ncopy.ys`。每个文件开头都应有一个头部注释，其中包含以下信息：

- 你的姓名和 ID。
- 对代码的高层描述。对于每个文件，都要说明如何修改了代码，以及为什么这样修改。

### 编码规则

在满足以下限制的前提下，可以自由进行任何修改：

- `ncopy.ys` 函数必须适用于任意数组大小。你可能会想针对 64 元素数组直接写死 64 条复制指令，但这并不可取，因为评分会依据解答在任意数组上的性能。

```asm
##################################################################
# ncopy.ys - 将含 len 个字的 src 数据块复制到 dst。
# 返回 src 中正数（>0）字的个数。
#
# 在这里写上你的姓名和 ID。
#
# 描述你如何以及为什么修改基准代码。
#
##################################################################
# 不要修改这一部分
# 函数序言。
# %rdi = src, %rsi = dst, %rdx = len
ncopy:

##################################################################
# 可以修改这一部分
            # 循环头
    xorq %rax,%rax        # count = 0;
    andq %rdx,%rdx        # len <= 0?
    jle Done              # 若是，转到 Done

Loop:   mrmovq (%rdi), %r10  # 从 src 读取 val...
        rmmovq %r10, (%rsi)  # ...并存入 dst
        andq %r10, %r10       # val <= 0?
        jle Npos              # 若是，转到 Npos
        irmovq $1, %r10
        addq %r10, %rax       # count++
Npos:   irmovq $1, %r10
        subq %r10, %rdx       # len--
        irmovq $8, %r10
        addq %r10, %rdi       # src++
        addq %r10, %rsi       # dst++
        andq %rdx,%rdx        # len > 0?
        jg Loop               # 若是，转到 Loop
##################################################################
# 不要修改下面这一段代码
# 函数尾声。
Done:
    ret
##################################################################
# 将下面的标号保留在函数末尾
End:
```

**图 3：`ncopy` 函数的基准 Y86-64 版本。** 参见 `sim/pipe/ncopy.ys`。

- `ncopy.ys` 函数必须能够在 YIS 上正确运行。所谓正确，是指它必须正确复制 `src` 数据块，并在 `%rax` 中返回正确的正整数个数。
- 汇编后的 `ncopy` 文件不得超过 1000 字节。可以使用提供的脚本 `check-len.pl` 检查任何嵌入了 `ncopy` 函数的程序长度：

  ```console
  unix> ./check-len.pl < ncopy.yo
  ```

- `pipe-full.hcl` 的实现必须通过 `../y86-code` 和 `../ptest` 中的回归测试（不使用测试 `iaddq` 的 `-i` 标志）。

除此之外，如果认为有帮助，可以实现 `iaddq` 指令。可以对 `ncopy.ys` 函数进行任何保持语义不变的变换，例如重新排列指令、用一条指令替换一组指令、删除某些指令或加入其他指令。阅读 CS:APP3e 第 5.8 节有关循环展开的内容可能会有所帮助。

### 构建并运行解答

为了测试解答，需要构建一个调用 `ncopy` 函数的驱动程序。实验材料提供了 `gen-driver.pl`，它可以为任意大小的输入数组生成驱动程序。例如，输入：

```console
unix> make drivers
```

会构建以下两个实用驱动程序：

- **`sdriver.yo`**：使用含 4 个元素的小数组测试 `ncopy` 函数。如果解答正确，该程序复制 `src` 数组后会停止，此时寄存器 `%rax` 的值为 2。
- **`ldriver.yo`**：使用含 63 个元素的大数组测试 `ncopy` 函数。如果解答正确，该程序复制 `src` 数组后会停止，此时寄存器 `%rax` 的值为 31（`0x1f`）。

每次修改 `ncopy.ys` 后，可以用下面的命令重新构建驱动程序：

```console
unix> make drivers
```

每次修改 `pipe-full.hcl` 后，可以用下面的命令重新构建模拟器：

```console
unix> make psim VERSION=full
```

如果要同时重新构建模拟器和驱动程序，请执行：

```console
unix> make VERSION=full
```

要在 GUI 模式下使用一个含 4 个元素的小数组测试解答，请执行：

```console
unix> ./psim -g sdriver.yo
```

要使用含 63 个元素的大数组测试解答，请执行：

```console
unix> ./psim -g ldriver.yo
```

当模拟器能够在这两种数据块长度下正确运行你的 `ncopy.ys` 版本后，还应执行以下测试。

#### 在 ISA 模拟器上测试驱动文件

确认 `ncopy.ys` 函数能够在 YIS 上正确运行：

```console
unix> make drivers
unix> ../misc/yis sdriver.yo
```

#### 使用 ISA 模拟器测试一系列数据块长度

Perl 脚本 `correctness.pl` 会生成数据块长度从 0 到某个上限（默认为 65）以及若干更大尺寸的驱动文件，使用模拟器运行它们（默认使用 YIS），并检查结果。该脚本会生成报告，显示每个数据块长度的状态：

```console
unix> ./correctness.pl
```

该脚本生成的测试程序，其结果计数会在每次运行时随机变化，因此它比标准驱动程序执行的测试更严格。

如果某个长度 `K` 得到错误结果，可以为该长度生成一个包含检查代码且结果随机变化的驱动文件：

```console
unix> ./gen-driver.pl -f ncopy.ys -n K -rc > driver.ys
unix> make driver.yo
unix> ../misc/yis driver.yo
```

程序结束时，寄存器 `%rax` 将具有以下值之一：

| `%rax` | 含义 |
|---|---|
| `0xaaaa` | 所有测试均通过。 |
| `0xbbbb` | 计数不正确。 |
| `0xcccc` | 函数 `ncopy` 超过 1000 字节。 |
| `0xdddd` | 某些源数据没有复制到目标位置。 |
| `0xeeee` | 目标区域之前或之后紧邻的某个字被破坏。 |

#### 在基准程序上测试流水线模拟器

当模拟器能够正确执行 `sdriver.ys` 和 `ldriver.ys` 后，应使用 `../y86-code` 中的 Y86-64 基准程序进行测试：

```console
unix> (cd ../y86-code; make testpsim)
```

该命令会在基准程序上运行 `psim`，并将结果与 YIS 比较。

#### 使用大量回归测试测试流水线模拟器

当基准程序能够正确执行后，应使用 `../ptest` 中的回归测试检查模拟器。例如，如果解答实现了 `iaddq` 指令，请执行：

```console
unix> (cd ../ptest; make SIM=../pipe/psim TFLAGS=-i)
```

#### 使用流水线模拟器测试一系列数据块长度

最后，可以在流水线模拟器上运行此前在 ISA 模拟器上运行过的同一组代码测试：

```console
unix> ./correctness.pl -p
```

## 7 评分

本实验共 190 分：Part A 30 分，Part B 60 分，Part C 100 分。

### Part A

Part A 共 30 分，每个 Y86-64 解答程序 10 分。每个程序都将根据正确性进行评估，包括是否正确处理栈和寄存器，以及是否与 `examples.c` 中的示例 C 函数在功能上等价。

如果评分者没有发现错误，并且各自的 `sum_list` 和 `rsum_list` 函数都在寄存器 `%rax` 中返回和 `0xcba`，则程序 `sum.ys` 和 `rsum.ys` 被视为正确。

如果评分者没有发现错误，`copy_block` 函数在寄存器 `%rax` 中返回值 `0xcba`，把三个 64 位值 `0x00a`、`0x0b` 和 `0xc` 复制到从地址 `dest` 开始的 24 个字节中，并且没有破坏其他内存位置，则程序 `copy.ys` 被视为正确。

> **译注：** 本段数值按原文保留；它与前面测试数据块中写出的 `0x00a`、`0x0b0`、`0xc00` 存在表示上的差异。

### Part B

原文在本小节中写道，本部分共 35 分：

- 10 分：描述 `iaddq` 指令所需的计算。
- 10 分：通过 `y86-code` 中的基准回归测试，以验证模拟器仍能正确执行基准程序集合。
- 15 分：通过 `ptest` 中针对 `iaddq` 的回归测试。

> **译注：** 本节列出的 35 分与本章开头“Part B 60 分”的总分说明不一致；两处均按原文保留。

### Part C

Part C 共 100 分。如果 `ncopy.ys` 代码或修改后的模拟器未通过前文所述的任何一项测试，本部分将不得分。

- `ncopy.ys` 和 `pipe-full.hcl` 的头部说明及其实现质量各 20 分。
- 性能 60 分。要获得这些分数，解答必须满足前文定义的正确性要求，即 `ncopy` 能在 YIS 上正确运行，且 `pipe-full.hcl` 能通过 `y86-code` 和 `ptest` 中的全部测试。

函数性能以**每元素周期数**（cycles per element，CPE）为单位表示。也就是说，如果模拟代码复制含 `N` 个元素的数据块需要 `C` 个周期，则 CPE 为 `C/N`。PIPE 模拟器会显示完成程序所需的总周期数。基准版本的 `ncopy` 函数在标准 PIPE 模拟器上处理含 63 个元素的大数组时，需要 897 个周期，因此 CPE 为 `897/63 = 14.24`。

由于调用 `ncopy` 和建立 `ncopy` 内部循环都需要消耗一些周期，不同数据块长度会得到不同的 CPE（通常 `N` 增大时 CPE 会下降）。因此，函数性能将按数据块长度从 1 到 64 时的平均 CPE 评估。可以使用 `pipe` 目录中的 Perl 脚本 `benchmark.pl`，让 `ncopy.ys` 代码在一系列数据块长度下运行模拟，并计算平均 CPE。只需执行：

```console
unix> ./benchmark.pl
```

即可查看结果。例如，基准版本 `ncopy` 的 CPE 范围是 29.00 到 14.27，平均值为 15.18。请注意，该 Perl 脚本不会检查答案的正确性；正确性应使用脚本 `correctness.pl` 检查。

平均 CPE 应当能够达到 9.00 以下。作者的最佳版本平均为 7.48。如果平均 CPE 为 `c`，则本实验这一部分的得分 `S` 为：

| 条件 | 得分 `S` |
|---|---:|
| `c > 10.5` | `0` |
| `7.50 <= c <= 10.50` | `20 * (10.5 - c)` |
| `c < 7.50` | `60` |

默认情况下，`benchmark.pl` 和 `correctness.pl` 会编译并测试 `ncopy.ys`。使用参数 `-f` 可以指定其他文件名；标志 `-h` 会给出完整的命令行参数列表。

## 8 提交说明

> **特定站点内容：** 请插入一段说明，解释学生应当如何提交实验的三个部分。下面给出 CMU 使用的说明。

- 需要提交三组文件：
  - Part A：`sum.ys`、`rsum.ys` 和 `copy.ys`。
  - Part B：`seq-full.hcl`。
  - Part C：`ncopy.ys` 和 `pipe-full.hcl`。
- 确保每个提交文件顶部的注释中都包含姓名和 ID。
- 要提交 Part X 的文件，请进入 `archlab-handout` 目录并输入：

  ```console
  unix> make handin-partX TEAM=teamname
  ```

  其中 `X` 为 `a`、`b` 或 `c`，`teamname` 是你的 ID。例如，提交 Part A 时输入：

  ```console
  unix> make handin-parta TEAM=teamname
  ```

- 如果提交后发现错误并希望提交修订版本，请输入：

  ```console
  unix> make handin-partX TEAM=teamname VERSION=2
  ```

  每次提交时继续递增版本号。
- 可以查看下面的目录来验证提交：

  ```text
  CLASSDIR/archlab/handin-partX
  ```

  你对该目录具有列出和插入权限，但没有读或写权限。

## 9 提示

- 按照设计，`sdriver.yo` 和 `ldriver.yo` 都足够小，可以在 GUI 模式下调试。作者认为 GUI 模式下调试最容易，并建议使用该模式。
- 如果在 Unix 服务器上以 GUI 模式运行，请确保已经初始化 `DISPLAY` 环境变量：

  ```console
  unix> setenv DISPLAY myhost.edu:0
  ```

- 对于某些 X 服务器，以 GUI 模式运行 `psim` 或 `ssim` 时，`Program Code`（程序代码）窗口最初会显示为一个收起的图标。只需单击图标即可展开窗口。
- 对于某些基于 Microsoft Windows 的 X 服务器，`Memory Contents`（内存内容）窗口不会自动调整大小，需要手动调整。
- 如果要求 `psim` 或 `ssim` 模拟器执行一个无效的 Y86-64 目标文件，模拟器会因段错误而终止。
