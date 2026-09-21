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

## 开发分支部署

`.github/workflows/website-preview.yml` 是 GitHub 要求放置在固定位置的工作流入口。网站的其余文件集中在本目录。

推送到 `feature/quarto-reader` 后，工作流会校验原始文档与实验包、生成页面、运行 Quarto、检查网页链接与资源，再将 `build/_site` 发布到 GitHub Pages。流程不提交生成文件，不修改 `main` 或 `v1.1` 标签。

仓库设置要求：

- Settings → Pages → Source 选择 GitHub Actions。
- Settings → Environments → github-pages 中，只允许 `feature/quarto-reader` 分支部署。

在仓库 Actions 页面查看 `Website preview` 运行结果。部署成功后的网址为 `https://sunnymaria.github.io/csapp-zh-markdown/`。这是公开的开发预览，目前不在主分支 README 中添加入口。

工作流目前仅通过该开发分支的 push 触发；失败后可在对应运行页面重新执行。将来正式合并前，需要一起调整触发分支和部署环境规则，不能仅合并后就假定主分支会自动发布。
