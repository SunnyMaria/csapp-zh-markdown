# 第 4 章 处理器体系结构

[返回总目录](../README.md) · [上一章](../第03章-程序的机器级表示/README.md) · [下一章](../第05章-优化程序性能/README.md) · [整章阅读](chapter.md) · [练习题答案](练习题答案.md)

## 阅读方式

- [整章连续阅读](chapter.md)
- 本章也保留了所有按小节拆分的 Markdown 文件，适合精确查找、引用和单独阅读。

## 小节目录

- [第 4 章 处理器体系结构](4.1/4.0-chapter-opening.md)
- [4.1 Y86-64 指令集体系结构](4.1/4.1-y86-64-instruction-set-architecture.md)
- [4.1.1 程序员可见的状态](4.1/4.1.1-programmer-visible-state.md)
- [4.1.2 Y86-64 指令](4.1/4.1.2-y86-64-instructions.md)
- [4.1.3 指令编码](4.1/4.1.3-instruction-encoding.md)
- [4.1.4 Y86-64 异常](4.1/4.1.4-y86-64-exceptions.md)
- [4.1.5 Y86-64 程序](4.1/4.1.5-y86-64-programs.md)
- [4.1.6 一些 Y86-64 指令的详情](4.1/4.1.6-some-y86-64-instruction-details.md)
- [4.2 逻辑设计和硬件控制语言 HCL](4.2/4.2-logic-design-and-hcl.md)
- [4.2.1 逻辑门](4.2/4.2.1-logic-gates.md)
- [4.2.2 组合电路和 HCL 布尔表达式](4.2/4.2.2-combinational-circuits-and-hcl-boolean-expressions.md)
- [4.2.3 字级的组合电路和 HCL 整数表达式](4.2/4.2.3-word-level-combinational-circuits-and-hcl-integer-expressions.md)
- [4.2.4 集合关系](4.2/4.2.4-set-membership.md)
- [4.2.5 存储器和时钟](4.2/4.2.5-memory-and-clocking.md)
- [4.3 Y86-64 的顺序实现](4.3/4.3-y86-64-sequential-implementation.md)
- [4.3.1 将处理组织成阶段](4.3/4.3.1-organizing-processing-into-stages.md)
- [4.3.2 SEQ 硬件结构](4.3/4.3.2-seq-hardware-structure.md)
- [4.3.3 SEQ 的时序](4.3/4.3.3-seq-timing.md)
- [4.3.4 SEQ 阶段的实现](4.3/4.3.4-seq-stage-implementation.md)
- [4.4 流水线的通用原理](4.4/4.4-general-principles-of-pipelining.md)
- [4.4.1 计算流水线](4.4/4.4.1-computational-pipelines.md)
- [4.4.2 流水线操作的详细说明](4.4/4.4.2-detailed-look-at-pipeline-operation.md)
- [4.4.3 流水线的局限性](4.4/4.4.3-limitations-of-pipelining.md)
- [4.4.4 带反馈的流水线系统](4.4/4.4.4-pipelining-a-system-with-feedback.md)
- [4.5 Y86-64 的流水线实现](4.5/4.5-y86-64-pipeline-implementation.md)
- [4.5.1 SEQ+：重新安排计算阶段](4.5/4.5.1-seq-plus-rearranging-computation-stages.md)
- [4.5.2 插入流水线寄存器](4.5/4.5.2-inserting-pipeline-registers.md)
- [4.5.3 对信号进行重新排列和标号](4.5/4.5.3-rearranging-and-labeling-signals.md)
- [4.5.4 预测下一个 PC](4.5/4.5.4-predicting-next-pc.md)
- [4.5.5 流水线冒险](4.5/4.5.5-pipeline-hazards.md)
- [4.5.6 异常处理](4.5/4.5.6-exception-handling.md)
- [4.5.7 PIPE 各阶段的实现](4.5/4.5.7-pipe-stage-implementations.md)
- [4.5.8 流水线控制逻辑](4.5/4.5.8-pipeline-control-logic.md)
- [4.5.9 性能分析](4.5/4.5.9-performance-analysis.md)
- [4.5.10 未完成的工作](4.5/4.5.10-unfinished-business.md)
- [4.6 小结](4.6/4.6-summary.md)
- [参考文献说明](4.6/references.md)
- [第 4 章家庭作业：4.45～4.50](homework/4.45-4.50-y86-programming.md)
- [第 4 章家庭作业：4.51～4.57](homework/4.51-4.57-processor-control.md)
- [第 4 章家庭作业：4.58～4.59](homework/4.58-4.59-write-back-and-performance.md)

## 其他资料

- [练习题答案](练习题答案.md)
