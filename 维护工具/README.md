# 维护工具

读者请从[阅读目录](../README.md)开始。

- `tools/check_release.py`：检查成品中的本地链接、路径大小写、目录内依赖和文档入口。
- `tools/check_supplements.py`：检查 12 章答案题号、八份实验说明，以及实验包完整性和 SHA-256。
- `tools/check_reading_views.py`：逐节核对整章正文和独立小节的文字、顺序及图片哈希。

在仓库根目录运行，使用 Python 3.9 或以上版本，仅依赖标准库：

```sh
python 维护工具/tools/check_release.py .
python 维护工具/tools/check_supplements.py
python 维护工具/tools/check_reading_views.py
```

各章 `README.md` 只负责导航，`chapter.md` 是整章正文，小节目录保留独立正文及图片。修改正文时须同步整章和小节两个版本；图片由两个版本共用。答案在 `练习题答案.md` 中独立维护。这里不保存历史成品、源 PDF、临时页图或一次性转换脚本。
