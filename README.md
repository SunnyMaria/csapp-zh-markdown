# CSAPP 中文 Markdown 学习资料

面向正在学习《深入理解计算机系统》（CSAPP，第三版）的读者，提供按章节拆分的中文正文、习题与原书答案，以及八个实验的中文说明和官方自学实验包，方便阅读、做题和记录自己的笔记。

**[阅读正文](docs/book/README.md) · [开始实验](docs/labs/README.md) · [全部资料](docs/README.md)**

## 为什么建立这个仓库

虽然 AI 正在迅速发展，获取知识、解释概念和解决问题变得越来越方便，但我仍然相信，想要深入学习计算机、在心中建立完整的底层知识框架，系统地读完一部扎实的书籍仍然是一条不可替代的学习路径。对我而言，CSAPP 就是这样一本值得从头读下去、反复思考和实践的书。

在自己的学习过程中，我希望找到覆盖 CSAPP 全部章节、方便在线阅读的中文 Markdown 资料，却没有找到符合这一需求的完整整理。因此，我建立了这个仓库，希望把正文、图表、习题和配套实验整理到一起，让阅读和学习能够更方便地衔接。

我本人也是这本书的读者之一。希望这份整理能帮助同样喜爱 CSAPP 的读者减少学习中的阻碍，不必受实体书的携带和阅读场景限制，可以在电脑或其他设备上阅读、查找内容和记录笔记，把更多精力留给理解、做题和实验。

## 这里有什么

| 资料 | 内容与位置 |
| --- | --- |
| 章节正文 | [序章及第 1—12 章](docs/book/README.md)，按小节拆分，包含三部分的独立导语、图表、代码和旁注 |
| 练习题与家庭作业 | 练习题放在对应正文小节中；有家庭作业的章节可从章目录进入，填空表格保留空位 |
| 原书练习题答案 | 共 238 道，各章目录末尾有独立的“练习题答案”入口，便于做完后核对 |
| 实验中文说明 | [八个实验](docs/labs/README.md)的 Markdown 译文，另附 Y86-64 处理器模拟器指南 |
| 实验程序包 | 每个实验目录均附官方自学 `.tar` 包，文档顶部可直接找到 |

答案部分是原书提供的**练习题答案**，不包含自行编写的家庭作业解答或实验解答。已核实的原书排印疑点见[答案编校说明](docs/book/answers-editorial.md)。

## 正文怎么找

从[正文目录](docs/book/README.md)选择章节，再选择小节即可。初次学习可以从第 1 章开始，序章中也有“如何阅读此书”等介绍。

| 阅读范围 | 章节入口 |
| --- | --- |
| 计算机系统入门 | [第 1 章：计算机系统漫游](docs/book/chapter1/README.md) |
| 第一部分：程序结构和执行 | [第 2 章：信息的表示和处理](docs/book/chapter2/README.md)、[第 3 章：程序的机器级表示](docs/book/chapter3/README.md)、[第 4 章：处理器体系结构](docs/book/chapter4/README.md)、[第 5 章：优化程序性能](docs/book/chapter5/README.md)、[第 6 章：存储器层次结构](docs/book/chapter6/README.md) |
| 第二部分：在系统上运行程序 | [第 7 章：链接](docs/book/chapter7/README.md)、[第 8 章：异常控制流](docs/book/chapter8/README.md)、[第 9 章：虚拟内存](docs/book/chapter9/README.md) |
| 第三部分：程序间的交互和通信 | [第 10 章：系统级 I/O](docs/book/chapter10/README.md)、[第 11 章：网络编程](docs/book/chapter11/README.md)、[第 12 章：并发编程](docs/book/chapter12/README.md) |

例如，学习补码时，进入第 2 章目录找到 2.2.3；随正文完成练习后，再通过章目录末尾的答案入口核对。需要记录思路时，可以在本地 Markdown 文件中添加笔记，或单独建立自己的笔记文件。

## 实验怎么用

| 实验 | 主要练习内容 | 中文说明 |
| --- | --- | --- |
| Data Lab | 位运算、整数与浮点数表示 | [打开](docs/labs/datalab-zh/datalab-zh.md) |
| Bomb Lab | 汇编阅读、反汇编与调试 | [打开](docs/labs/bomblab-zh/bomblab-zh.md) |
| Attack Lab | 栈、缓冲区溢出与返回导向编程 | [打开](docs/labs/attacklab-zh/attacklab-zh.md) |
| Architecture Lab | Y86-64、流水线与性能优化 | [打开](docs/labs/archlab-zh/archlab-zh.md) |
| Cache Lab | 高速缓存模拟与矩阵转置优化 | [打开](docs/labs/cachelab-zh/cachelab-zh.md) |
| Shell Lab | 进程、信号与作业控制 | [打开](docs/labs/shlab-zh/shlab-zh.md) |
| Malloc Lab | 动态内存分配与内存管理 | [打开](docs/labs/malloclab-zh/malloclab-zh.md) |
| Proxy Lab | 网络编程、并发与缓存 | [打开](docs/labs/proxylab-zh/proxylab-zh.md) |

1. 打开对应中文说明，了解实验目标和要求。
2. 通过文档顶部的“实验包”链接取得同目录下的 `.tar` 文件，解压到自己的实验工作目录。
3. 阅读[自学包与原说明的差异](docs/labs/COMPATIBILITY.md)，然后按实验说明和包内 README 配置环境、编译及测试。

实验包主要面向 Linux 环境，部分使用较早的工具链或解释器。原文中的课程日期、服务器地址和提交路径保留自官方模板，不是本仓库提供的课程服务。特别是 **Malloc 自学包仅附两份短测试，不含完整评分跟踪文件**；具体差异已在上述说明中列出。

Architecture Lab 的配套资料见 [Y86-64 模拟器指南](docs/labs/archlab-zh/simguide-zh.md)。实验包的官方来源和 SHA-256 见[来源与校验值](docs/labs/PACKAGES.md)。

## 在线阅读与本地使用

**在线阅读：** 直接点击本页的目录链接，在 GitHub 上查看 Markdown。

**下载阅读：** 使用仓库页面的 **Code → Download ZIP** 下载并解压，或运行：

```sh
git clone https://github.com/SunnyMaria/csapp-zh-markdown.git
```

然后用支持 Markdown 预览的编辑器或阅读器打开 `README.md` 或 `docs/README.md`。阅读资料不需要安装 Python，也不需要原始扫描 PDF。

所有学习资料都在 `docs/` 中，可以将这个目录整体复制到其他位置。**请保留内部目录结构和图片文件，不要只复制单个 Markdown 文件**，否则相对路径引用的图片可能无法显示。实验压缩包也保存在各自的实验目录中。

## 整理方式与反馈

正文尽量忠于原书的措辞和顺序。文字、代码、普通表格及简单公式使用可编辑文本；需要保留空间结构的图示使用本地图片。不同 Markdown 阅读器对上下标和脚注的显示支持可能不同。

如果发现错字、缺段、图片截断或链接失效，欢迎提交 Issue，注明章节、题号或图号，便于核对。维护者使用的校验方法见 [work/README.md](work/README.md)。

## 2.0 展望：在线阅读与学习

1.0 以完整、可下载的 Markdown 学习资料为基础。后续计划推出 **CSAPP 在线阅读与学习网站**，让大家直接在浏览器中按章节阅读正文、查阅习题答案和使用实验资料。

2.0 将围绕清晰的章节导航、内容搜索，以及电脑和手机上的阅读体验展开，减少下载和配置阅读工具的步骤。Markdown 资料仍会保留，方便离线阅读和自行记录笔记。

目前网站尚未上线，具体功能和上线时间待确定；后续进展及访问入口会在本仓库更新。

## 特别致谢

特别致敬并感谢 **[Hansimov/csapp](https://github.com/Hansimov/csapp)**。

本项目整理正文所使用的 **OCR 源文件来自该仓库**。它为后续的文字核对、章节拆分以及 Markdown 整理提供了重要基础。感谢原仓库维护者和贡献者对 CSAPP 学习资料的整理与分享，也欢迎大家访问原仓库。
