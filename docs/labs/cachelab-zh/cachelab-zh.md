# Cache Lab：理解高速缓存存储器

原文：[官方实验说明](https://csapp.cs.cmu.edu/3e/cachelab.pdf)  
实验包：[cachelab-handout.tar](cachelab-handout.tar)

自学包说明：[运行配置与原说明的差异](../COMPATIBILITY.md)

**15-213/18-213，2012 年秋季**  
**布置时间：2012 年 10 月 2 日，星期二**  
**截止时间：2012 年 10 月 11 日，星期四，23:59**  
**最晚提交时间：2012 年 10 月 14 日，星期日，23:59**

> 译注：课程日期及下文的课程专用地址或占位符来自官方说明模板，不是本仓库的截止日期或提交要求。

## 1 实验安排

这是一个个人项目。你必须在一台 64 位 x86-64 机器上运行本实验。

> **特定站点内容：** 在此处插入其他实验安排，例如如何寻求帮助。

## 2 概述

本实验将帮助你理解高速缓存存储器会对 C 程序的性能产生怎样的影响。

实验由两个部分组成。在第一部分中，你将编写一个小型 C 程序（约 200-300 行），模拟高速缓存存储器的行为。在第二部分中，你将优化一个小型矩阵转置函数，目标是尽可能减少缓存不命中的次数。

## 3 下载实验材料

> **特定站点内容：** 在此处插入一段文字，说明教师将如何向学生发放 `cachelab-handout.tar` 文件。

首先，将 `cachelab-handout.tar` 复制到一个受保护的 Linux 目录中，你将在该目录中完成实验。然后执行：

```console
linux> tar xvf cachelab-handout.tar
```

这会创建一个名为 `cachelab-handout` 的目录，其中包含若干文件。你需要修改两个文件：`csim.c` 和 `trans.c`。要编译这些文件，请输入：

```console
linux> make clean
linux> make
```

> **警告：** 不要让 Windows WinZip 程序打开 `.tar` 文件（许多 Web 浏览器被设置为自动执行此操作）。应当把文件保存到 Linux 目录中，再使用 Linux 的 `tar` 程序解压。一般来说，在本课程中，绝不要使用 Linux 以外的平台修改文件。这样做可能导致数据以及重要实验成果丢失。

## 4 实验说明

本实验包含两个部分。在 Part A 中，你将实现一个缓存模拟器。在 Part B 中，你将编写一个针对缓存性能优化的矩阵转置函数。

### 4.1 参考跟踪文件

实验材料目录的 `traces` 子目录中包含一组参考跟踪文件。我们将使用这些文件评估你在 Part A 中编写的缓存模拟器是否正确。这些跟踪文件由一个名为 `valgrind` 的 Linux 程序生成。例如，在命令行中输入：

```console
linux> valgrind --log-fd=1 --tool=lackey -v --trace-mem=yes ls -l
```

该命令会运行可执行程序 `ls -l`，按照各次内存访问发生的顺序捕获跟踪记录，并将它们打印到标准输出 `stdout`。

Valgrind 内存跟踪记录采用如下形式：

```text
I 0400d7d4,8
 M 0421c7f0,4
 L 04f6b868,8
 S 7ff0005c8,8
```

每一行表示一次或两次内存访问。每一行的格式为：

```text
[space]operation address,size
```

`operation` 字段表示内存访问类型：`I` 表示指令加载，`L` 表示数据加载，`S` 表示数据存储，`M` 表示数据修改（即先执行一次数据加载，再执行一次数据存储）。`I` 前面绝不会有空格；`M`、`L` 和 `S` 前面始终有一个空格。`address` 字段指定一个 64 位十六进制内存地址，`size` 字段指定该操作访问的字节数。

### 4.2 Part A：编写缓存模拟器

在 Part A 中，你将在 `csim.c` 中编写一个缓存模拟器。它以 Valgrind 内存跟踪记录作为输入，模拟高速缓存对该跟踪记录的命中/不命中行为，并输出命中、不命中和驱逐的总次数。

实验材料提供了一个参考缓存模拟器的二进制可执行文件 `csim-ref`。它能够针对 Valgrind 跟踪文件模拟任意大小和任意相联度的高速缓存。在选择要驱逐的缓存行时，它采用 LRU（least-recently used，最近最少使用）替换策略。

参考模拟器接受以下命令行参数：

```text
Usage: ./csim-ref [-hv] -s <s> -E <E> -b <b> -t <tracefile>
```

- **`-h`**：可选的帮助标志，用于打印用法信息。
- **`-v`**：可选的详细输出标志，用于显示跟踪信息。
- **`-s <s>`**：组索引位数（组数 S = 2<sup>s</sup>）。
- **`-E <E>`**：相联度，即每组的行数。
- **`-b <b>`**：块位数（块大小 B = 2<sup>b</sup>）。
- **`-t <tracefile>`**：要重放的 Valgrind 跟踪文件名。

这些命令行参数采用 CS:APP2e 教材第 597 页中的记号 `s`、`E` 和 `b`。例如：

```console
linux> ./csim-ref -s 4 -E 1 -b 4 -t traces/yi.trace
hits:4 misses:5 evictions:3
```

同一个示例在详细输出模式下的结果为：

```console
linux> ./csim-ref -v -s 4 -E 1 -b 4 -t traces/yi.trace
L 10,1 miss
M 20,1 miss hit
L 22,1 hit
S 18,1 hit
L 110,1 miss eviction
L 210,1 miss eviction
M 12,1 miss eviction hit
hits:4 misses:5 evictions:3
```

Part A 的任务是补全 `csim.c`，使其接受与参考模拟器相同的命令行参数，并产生完全相同的输出。请注意，该文件几乎完全是空的，你需要从头编写它。

#### Part A 编程规则

- 在 `csim.c` 的头部注释中写上你的姓名和登录 ID。
- `csim.c` 必须在编译时不产生任何警告，否则不能得分。
- 模拟器必须对任意 `s`、`E` 和 `b` 都能正确工作。这意味着你需要使用 `malloc` 函数为模拟器的数据结构分配存储空间。输入 `man malloc` 可以查看该函数的信息。
- 本实验只关注数据缓存性能，因此模拟器应忽略所有指令缓存访问，即以 `I` 开头的行。请记住，Valgrind 始终把 `I` 放在第一列（前面没有空格），把 `M`、`L` 和 `S` 放在第二列（前面有一个空格）。这一点可能有助于解析跟踪记录。
- 要获得 Part A 的分数，必须在 `main` 函数末尾调用 `printSummary`，并传入命中、不命中和驱逐的总次数：

  ```c
  printSummary(hit_count, miss_count, eviction_count);
  ```

- 在本实验中，可以假定内存访问都正确对齐，因此一次内存访问绝不会跨越块边界。有了这一假设，就可以忽略 Valgrind 跟踪记录中的访问大小。

### 4.3 Part B：优化矩阵转置

在 Part B 中，你将在 `trans.c` 中编写一个转置函数，使其引发的缓存不命中尽可能少。

令 A 表示一个矩阵，A<sub>ij</sub> 表示第 i 行第 j 列的元素。A 的转置记作 A<sup>T</sup>；它是一个满足 A<sub>ij</sub> = A<sup>T</sup><sub>ji</sub> 的矩阵。

为了帮助你入门，`trans.c` 中提供了一个示例转置函数。它计算 `N x M` 矩阵 `A` 的转置，并把结果存入 `M x N` 矩阵 `B`：

```c
char trans_desc[] = "Simple row-wise scan transpose";
void trans(int M, int N, int A[N][M], int B[M][N])
```

该示例转置函数是正确的，但效率不高，因为它的访问模式会造成较多缓存不命中。

Part B 的任务是编写一个类似的函数 `transpose_submit`，尽量减少处理不同大小矩阵时的缓存不命中次数：

```c
char transpose_submit_desc[] = "Transpose submission";
void transpose_submit(int M, int N, int A[N][M], int B[M][N]);
```

不要修改 `transpose_submit` 函数的描述字符串 `"Transpose submission"`。自动评分器会搜索这个字符串，以确定应当评估哪个转置函数并据此评分。

#### Part B 编程规则

- 在 `trans.c` 的头部注释中写上你的姓名和登录 ID。
- `trans.c` 中的代码必须在编译时不产生任何警告，否则不能得分。
- 每个转置函数最多只能定义 12 个 `int` 类型的局部变量。[^1]
- 不得使用 `long` 类型变量或位操作技巧在一个变量中存储多个值，以规避上一条规则。
- 转置函数不得使用递归。
- 如果使用辅助函数，那么辅助函数和顶层转置函数在任一时刻位于栈上的局部变量总数不得超过 12。例如，转置函数声明了 8 个变量，随后调用一个使用 4 个变量的函数，而该函数又调用另一个使用 2 个变量的函数，此时栈上共有 14 个变量，违反了规则。
- 转置函数不得修改数组 `A`，但可以任意处理数组 `B` 的内容。
- 不得在代码中定义任何数组，也不得使用任何形式的 `malloc`。

[^1]: 设置这项限制的原因是，测试代码无法统计对栈的引用。实验希望你限制对栈的引用，把重点放在源数组和目标数组的访问模式上。

## 5 评分

本节说明如何评估你的实验成果。本实验满分为 60 分：

- Part A：27 分
- Part B：26 分
- 代码风格：7 分

### 5.1 Part A 的评分

对于 Part A，我们将使用不同的缓存参数和跟踪文件运行你的缓存模拟器。共有 8 个测试用例；除最后一个用例为 6 分外，其余每个用例均为 3 分：

```console
linux> ./csim -s 1 -E 1 -b 1 -t traces/yi2.trace
linux> ./csim -s 4 -E 2 -b 4 -t traces/yi.trace
linux> ./csim -s 2 -E 1 -b 4 -t traces/dave.trace
linux> ./csim -s 2 -E 1 -b 3 -t traces/trans.trace
linux> ./csim -s 2 -E 2 -b 3 -t traces/trans.trace
linux> ./csim -s 2 -E 4 -b 3 -t traces/trans.trace
linux> ./csim -s 5 -E 1 -b 5 -t traces/trans.trace
linux> ./csim -s 5 -E 1 -b 5 -t traces/long.trace
```

可以使用参考模拟器 `csim-ref` 获得每个测试用例的正确答案。调试时，使用 `-v` 选项可以得到每次命中和不命中的详细记录。

对于每个测试用例，如果输出了正确的缓存命中、不命中和驱逐次数，就会得到该用例的全部分数。报告的命中、不命中和驱逐次数分别占该用例分数的 1/3。也就是说，如果某个测试用例值 3 分，而模拟器输出的命中和不命中次数正确，但驱逐次数错误，那么可以得到 2 分。

### 5.2 Part B 的评分

对于 Part B，我们会在三种不同大小的输出矩阵上评估 `transpose_submit` 函数的正确性和性能：

- 32 x 32（`M = 32, N = 32`）
- 64 x 64（`M = 64, N = 64`）
- 61 x 67（`M = 61, N = 67`）

#### 5.2.1 性能（26 分）

对于每种矩阵大小，首先使用 Valgrind 提取 `transpose_submit` 函数的地址跟踪记录，然后用参考模拟器在参数为 `s = 5, E = 1, b = 5` 的高速缓存上重放该跟踪记录，以评估函数性能。

每种矩阵大小的性能得分会随不命中次数 `m` 线性变化，直至达到相应阈值：

- **32 x 32**：`m < 300` 时得 8 分，`m > 600` 时得 0 分。
- **64 x 64**：`m < 1,300` 时得 8 分，`m > 2,000` 时得 0 分。
- **61 x 67**：`m < 2,000` 时得 10 分，`m > 3,000` 时得 0 分。

代码在某一矩阵大小上必须正确，才能获得该大小对应的任何性能分数。代码只需要对这三种情况正确，因此可以专门针对这三种情况进行优化。特别地，函数可以显式检查输入大小，并为每种情况分别实现优化代码，这完全符合要求。

### 5.3 代码风格评分

代码风格共 7 分，由课程工作人员人工评定。代码风格指南可在课程网站上找到。

课程工作人员还会检查 Part B 代码中是否存在违规数组和过多的局部变量。

## 6 开展实验

### 6.1 开展 Part A

实验材料提供了一个名为 `test-csim` 的自动评分程序，它使用参考跟踪记录测试缓存模拟器的正确性。运行测试前务必先编译模拟器：

```console
linux> make
linux> ./test-csim
```

该程序的输出形式如下：

| 分值 | `(s,E,b)` | 你的模拟器：命中 | 你的模拟器：不命中 | 你的模拟器：驱逐 | 参考模拟器：命中 | 参考模拟器：不命中 | 参考模拟器：驱逐 | 跟踪文件 |
|---:|:---:|---:|---:|---:|---:|---:|---:|---|
| 3 | `(1,1,1)` | 9 | 8 | 6 | 9 | 8 | 6 | `traces/yi2.trace` |
| 3 | `(4,2,4)` | 4 | 5 | 2 | 4 | 5 | 2 | `traces/yi.trace` |
| 3 | `(2,1,4)` | 2 | 3 | 1 | 2 | 3 | 1 | `traces/dave.trace` |
| 3 | `(2,1,3)` | 167 | 71 | 67 | 167 | 71 | 67 | `traces/trans.trace` |
| 3 | `(2,2,3)` | 201 | 37 | 29 | 201 | 37 | 29 | `traces/trans.trace` |
| 3 | `(2,4,3)` | 212 | 26 | 10 | 212 | 26 | 10 | `traces/trans.trace` |
| 3 | `(5,1,5)` | 231 | 7 | 0 | 231 | 7 | 0 | `traces/trans.trace` |
| 6 | `(5,1,5)` | 265189 | 21775 | 21743 | 265189 | 21775 | 21743 | `traces/long.trace` |
| **27** |  |  |  |  |  |  |  |  |

对于每项测试，程序都会显示你得到的分数、缓存参数、输入跟踪文件，以及你的模拟器与参考模拟器结果的对比。

下面是完成 Part A 的一些提示和建议：

- 初步调试应使用较小的跟踪文件，例如 `traces/dave.trace`。
- 参考模拟器接受可选参数 `-v`，用于启用详细输出，显示每次内存访问造成的命中、不命中和驱逐。你不必在 `csim.c` 中实现该功能，但强烈建议这样做。这样就能直接比较你的模拟器与参考模拟器在参考跟踪文件上的行为，有助于调试。
- 建议使用 `getopt` 函数解析命令行参数。需要包含以下头文件：

  ```c
  #include <getopt.h>
  #include <stdlib.h>
  #include <unistd.h>
  ```

  详细信息参见 `man 3 getopt`。
- 每次数据加载（`L`）或存储（`S`）操作最多造成一次缓存不命中。数据修改操作（`M`）被视为先加载、再向同一地址存储。因此，一次 `M` 操作可能产生两次缓存命中，也可能产生一次不命中和一次命中，并可能伴随一次驱逐。
- 如果希望使用 15-122 课程中的 C0 风格契约，可以包含实验材料目录中为方便使用而提供的 `contracts.h`。

### 6.2 开展 Part B

实验材料提供了一个名为 `test-trans.c` 的自动评分程序，用于测试你向自动评分器注册的每个转置函数的正确性和性能。

可以在 `trans.c` 文件中注册最多 100 个版本的转置函数。每个转置版本采用如下形式：

```c
/* 头部注释 */
char trans_simple_desc[] = "A simple transpose";
void trans_simple(int M, int N, int A[N][M], int B[M][N])
{
    /* 在此处编写转置代码 */
}
```

要向自动评分器注册某个转置函数，请在 `trans.c` 的 `registerFunctions` 例程中进行如下形式的调用：

```c
registerTransFunction(trans_simple, trans_simple_desc);
```

运行时，自动评分器会评估每个已注册的转置函数并打印结果。当然，注册的函数中必须包含要提交评分的 `transpose_submit`：

```c
registerTransFunction(transpose_submit, transpose_submit_desc);
```

有关其工作方式的示例，请参阅默认的 `trans.c` 函数。

自动评分器以矩阵大小作为输入。它使用 Valgrind 为每个已注册的转置函数生成跟踪记录，然后在参数为 `s = 5, E = 1, b = 5` 的高速缓存上运行参考模拟器，以评估每份跟踪记录。

例如，要在 32 x 32 矩阵上测试已注册的转置函数，请重新构建 `test-trans`，然后用适当的 `M` 和 `N` 值运行它：

```console
linux> make
linux> ./test-trans -M 32 -N 32
Step 1: Evaluating registered transpose funcs for correctness:
func 0 (Transpose submission): correctness: 1
func 1 (Simple row-wise scan transpose): correctness: 1
func 2 (column-wise scan transpose): correctness: 1
func 3 (using a zig-zag access pattern): correctness: 1

Step 2: Generating memory traces for registered transpose funcs.

Step 3: Evaluating performance of registered transpose funcs (s=5, E=1, b=5)
func 0 (Transpose submission): hits:1766, misses:287, evictions:255
func 1 (Simple row-wise scan transpose): hits:870, misses:1183, evictions:1151
func 2 (column-wise scan transpose): hits:870, misses:1183, evictions:1151
func 3 (using a zig-zag access pattern): hits:1076, misses:977, evictions:945

Summary for official submission (func 0): correctness=1 misses=287
```

在这个示例中，`trans.c` 中注册了 4 个不同的转置函数。`test-trans` 程序会测试每个已注册的函数、显示各自的结果，并提取正式提交函数的结果。

下面是完成 Part B 的一些提示和建议：

- `test-trans` 程序把函数 `i` 的跟踪记录保存在文件 `trace.fi` 中。[^2] 这些跟踪文件是非常有价值的调试工具，可以帮助你准确理解每个转置函数的命中和不命中来自何处。要调试某个函数，只需使用详细输出选项，让参考模拟器重放其跟踪记录：

  ```console
  linux> ./csim-ref -v -s 5 -E 1 -b 5 -t trace.f0
  S 68312c,1 miss
  L 683140,8 miss
  L 683124,4 hit
  L 683120,4 hit
  L 603124,4 miss eviction
  S 6431a0,4 miss
  ...
  ```

- 转置函数是在直接映射高速缓存上进行评估的，因此冲突不命中是一个潜在问题。请考虑代码中可能发生的冲突不命中，尤其是沿矩阵对角线的位置，并设法设计能够减少这些冲突不命中的访问模式。
- 分块是一种减少缓存不命中的实用技术。更多信息请参阅：`http://csapp.cs.cmu.edu/public/waside/waside-blocking.pdf`。

[^2]: 由于 Valgrind 会引入许多与你的代码无关的栈访问，实验已经从跟踪记录中滤除了所有栈访问。这正是禁止使用局部数组并限制局部变量个数的原因。

### 6.3 综合测试

实验材料提供了一个驱动程序 `./driver.py`，用于完整评估缓存模拟器和转置代码。这与教师评估提交内容时使用的程序相同。驱动程序使用 `test-csim` 评估模拟器，使用 `test-trans` 在三种矩阵大小上评估提交的转置函数，然后打印结果摘要以及所得分数。

要运行驱动程序，请输入：

```console
linux> ./driver.py
```

## 7 提交实验

每次在 `cachelab-handout` 目录中输入 `make` 时，`Makefile` 都会创建一个名为 `userid-handin.tar` 的 tar 包，其中包含当前的 `csim.c` 和 `trans.c` 文件。

> **特定站点内容：** 在此处插入文字，说明每位学生应如何在所在学校提交 `userid-handin.tar` 文件。

> **重要：** 不要在 Windows 或 Mac 机器上创建提交用 tar 包，也不要以任何其他归档格式提交文件，例如 `.zip`、`.gzip` 或 `.tgz`。
