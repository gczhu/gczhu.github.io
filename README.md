# Guangcheng Zhu · 祝广程

面向 GitHub Pages 的学术个人主页。参考王皓波老师主页的白底蓝色链接、衬线标题和左侧头像布局，自行实现 HTML、CSS 和少量 JavaScript。网站不依赖第三方统计、字体 CDN 或前端框架。

页面包含 About、Selected publications 和 Education，研究方向在个人简介中加粗展示。暂不包含 Experience、Selected honors、University–industry collaboration 或 Academic service。论文保持纯文字列表，不展示配图或摘要。

## 本地预览

在项目目录运行：

```sh
python3 build.py
python3 -m http.server 8000
```

打开 http://localhost:8000/ 。直接双击 `index.html` 也能浏览；本地文件模式可能不支持剪贴板按钮，BibTeX 展开和文件下载仍可使用。

## 发布到 gczhu.github.io

1. 使用 **gczhu** 账号新建公开仓库 **gczhu.github.io**。如果同名仓库已经存在，请先检查其中的文件，不要直接覆盖。
2. 将本目录的内容（包含 `.github` 隐藏目录）放入仓库根目录，提交到 `main` 分支。
3. 进入仓库 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。
4. 在 **Actions → Deploy academic homepage → Run workflow** 运行工作流。工作流成功后，网站地址为 https://gczhu.github.io/ 。

工作流使用 Python 标准库生成静态文件，无需安装依赖。GitHub Pages 的官方流程见 https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages 。

如需直接上传静态文件，也可以将 `python3 build.py --output _site` 生成的目录内容作为 Pages 发布目录。

## 更新内容

- `content/profile.json`：姓名、邮箱、学校、导师、研究简介、教育经历和页脚更新时间。`research_highlights` 指定简介中需要加粗的短语，`updated` 设置页脚的更新时间。
- `content/publications.json`：论文题目、按原文排序的作者、会议、链接、BibTeX。`selected: true` 表示默认展示。`sort_date` 控制时间倒序：有 arXiv 的论文使用首次公开时间，其余使用所提供的会议发表月份；同日记录保持原顺序。会议接收年份单独保留在 `year` 中。
- `assets/style.css`：颜色、间距和手机布局。
- `build.py`：页面结构。每次修改内容后运行 `python3 build.py`；GitHub Actions 也会自动生成页面。

### 替换头像

当前头像使用本人提供的插画，保存在 `assets/portrait.jpg`。替换该文件后运行构建即可；`content/profile.json` 的 `portrait_alt` 设置图片描述。页面通过 CSS 的 `object-fit: cover` 和 `object-position: 50% 35%` 控制显示范围，保留原始图片，优先展示猫和人物的脸部。

### 添加 Google Scholar

`content/profile.json` 中的 `scholar` 已设置为本人提供的公开主页 URL。需要更换时修改该地址并重新构建；顶部入口依次为 Email、Google Scholar、GitHub。

### 添加论文

复制已有记录，设置唯一 `id`，填写作者名单和准确链接。论文采用纯文字列表，无需准备配图。链接按 paper、pdf、code 排序，仅显示已有资源，BibTeX 入口由构建自动生成，不再添加单独的 arXiv 入口。运行构建会同步更新首页、总 BibTeX 和每篇论文的独立引用文件。

## 内容核对

- 原始文件包含 14 条 BibTeX；合并 TraPO 与 RealHiTBench 的会议版 / arXiv 版，再加入 CoCA，共 13 篇。
- TraPO、RealHiTBench 以所提供的会议记录作为主要引用，PDF 链接使用 arXiv 版本。
- MARAL 的代码链接根据论文首页核实为 https://github.com/gczhu/MARAL 。
- PivotTrace 的 arXiv 页面明确标注接收于 NeurIPS 2026，页面已更新会议标注；BibTeX 保留 arXiv 记录并添加接收说明。
- GeoMin 由本人确认接收于 KDD 2026，页面已更新；BibTeX 保留 arXiv 记录并添加接收说明。
- CriPO 采用 arXiv v4 的最新题目和作者名单（末位作者为 Chenglong Wang）。
- CoCA 的共同一作标记来自论文正文；TraPO 的 Shenzhi Yang 与 Guangcheng Zhu 标注共同一作，由本人确认。
- 其他未从论文来源核实会议接收状态的工作保留 arXiv 标注。
- 个人简介和教育经历根据本人提供的信息整理；没有添加未经提供的实习经历、奖项、CV 或 Scholar 主页。

网页布局灵感：https://hbzju.github.io/ 。站点实现为原创，未复制该网站的照片或个人文案。

## 自动部署

网站地址：https://gczhu.github.io/ 。提交到 `main` 分支后，GitHub Actions 会运行 `build.py` 并发布生成的静态页面。部署结果可在仓库的 Actions 页面查看；也可以手动运行 `Deploy academic homepage` 工作流重新发布。
