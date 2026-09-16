# 维护工具

读者请从 [成品目录](../docs/README.md) 开始。

- `tools/check_release.py`：检查成品中的本地链接、路径大小写、目录内依赖和文档入口。
- `tools/check_supplements.py`：检查 12 章答案题号、八份实验说明，以及实验包完整性和 SHA-256。

在仓库根目录运行，使用 Python 3.9 或以上版本，仅依赖标准库：

```sh
python work/tools/check_release.py docs
python work/tools/check_supplements.py
```

直接维护 `docs/` 中的文件；这里不保存历史成品、源 PDF、临时页图或一次性转换脚本。
