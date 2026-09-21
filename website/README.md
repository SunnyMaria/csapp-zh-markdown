# 阅读网站

网站使用 Quarto 1.9.38，将仓库现有 Markdown 生成网页；正文仍在原章节目录维护。

网站相关文件集中在本目录，保留原有章节、实验和图片目录结构：

```text
website/
  README.md             网站维护说明
  scripts/
    build.py            生成页面、导航与资源映射
    check.py            检查网页链接、图片与原文一致性
  styles/
    reader.css          阅读界面样式
  build/                自动生成，不提交
    _quarto.yml         生成的 Quarto 配置
    manifest.json       来源与资源映射
    check-report.json   检查结果
    _site/              生成的 HTML 网站
```

构建缓存、预览网页和检查报告均留在 `build/`，不混入书稿或提交记录。网站源码将作为独立的网站变更提交，不移动现有正文，也不修改已发布的 `v1.1` 标签。

在仓库根目录运行：

```sh
python website/scripts/build.py
quarto render website/build
python website/scripts/check.py
quarto preview website/build --no-browser
```

生成器会清空并重建 `website/build/`，请勿在其中编辑正文。

书中的代码仅供显示，不会执行。首页为第一章开篇，侧栏提供前言、所有章节、独立答案、实验、附录和参考文献。章节导航保留整章阅读入口，整章页不重复进入搜索结果。

当前只提供本地预览，尚未启用远程自动部署。上线前需验证仓库子路径下的图片、页面链接和搜索，并配置 GitHub Pages。
