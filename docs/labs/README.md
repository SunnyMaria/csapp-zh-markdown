# 实验资料

八个实验的中文说明统一采用 Markdown，按学习顺序排列。Architecture Lab 另附处理器模拟器指南；文档中的必要配图随仓库提供。

| 实验 | 中文说明 | 随仓库提供的官方自学实验包 |
| --- | --- | --- |
| Data Lab | [数据的位级表示与运算](datalab-zh/datalab-zh.md) | [datalab-handout.tar](datalab-zh/datalab-handout.tar) |
| Bomb Lab | [拆解二进制炸弹](bomblab-zh/bomblab-zh.md) | [bomb.tar](bomblab-zh/bomb.tar) |
| Attack Lab | [理解缓冲区溢出漏洞](attacklab-zh/attacklab-zh.md) | [target1.tar](attacklab-zh/target1.tar) |
| Architecture Lab | [流水线处理器性能优化](archlab-zh/archlab-zh.md) | [archlab-handout.tar](archlab-zh/archlab-handout.tar) |
| Cache Lab | [理解高速缓存存储器](cachelab-zh/cachelab-zh.md) | [cachelab-handout.tar](cachelab-zh/cachelab-handout.tar) |
| Shell Lab | [编写带作业控制的 Unix shell](shlab-zh/shlab-zh.md) | [shlab-handout.tar](shlab-zh/shlab-handout.tar) |
| Malloc Lab | [编写动态存储分配器](malloclab-zh/malloclab-zh.md) | [malloclab-handout.tar](malloclab-zh/malloclab-handout.tar) |
| Proxy Lab | [编写带缓存的 Web 代理](proxylab-zh/proxylab-zh.md) | [proxylab-handout.tar](proxylab-zh/proxylab-handout.tar) |

## 配套指南

- [Y86-64 处理器模拟器指南](archlab-zh/simguide-zh.md)
- [实验包来源与校验值](PACKAGES.md)
- [自学实验包与说明模板的差异](COMPATIBILITY.md)

## 版本与使用说明

资料来源：[CS:APP3e 官方实验页面](https://csapp.cs.cmu.edu/3e/labs.html)。本目录选用 64 位 Attack Lab 与 Y86-64 Architecture Lab；Cache Lab 对应官方课程中替代 Performance Lab 的实验。

这里提供实验说明的中文翻译，不包含实验解答。原说明中的课程日期、教师信息、提交地址及 `SITE-SPECIFIC` 等占位内容保留原意；自学者应以实际使用的实验包及课程安排为准。运行实验所需的官方自学压缩包已原样放入各实验目录，可以通过上表本地链接获取。

官方自学 Bomb Lab 已关闭向评分服务器报告的功能；自学 Attack Lab 运行目标程序时需使用 `-q`，避免连接不存在的评分服务器。
