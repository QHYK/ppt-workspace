# 安装、验证与共享

依赖版本以根目录 [`pyproject.toml`](../pyproject.toml) 为准。需要 Python 3.11 或更新版本；在项目根目录安装并验证公共部分：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python slides/example/build.py
.venv/bin/python -m unittest discover -s code/tests -v
```

公共测试只使用公共 Library、Theme、图标、示意素材和 `slides/example/`。示例 PPTX 输出到示例目录，生成结果默认不进入 Git。业务项目在本地按相同方式运行自己的 `build.py`；不要把业务生成脚本列为公共测试的依赖。

修改组件或 Theme 后，重新生成示例并逐页渲染检查；如果本地业务项目受到影响，也重建并检查其页面。检查文字截断、字体、重叠、越界、对齐、间距、图片、图标、结构图表达，以及业务事实和数字是否变化。视觉质量以实际渲染为准；无法渲染时在报告中说明。中文预览应使用 PowerPoint 或支持中文字体的渲染器；缺少 `Noto Sans CJK SC` 的 LibreOffice 环境不能用于中文文字验收。

正式交付业务 PPT 时提供可编辑 PPTX、实际生成源码、必要的公共依赖及素材和逐页预览。源码历史应通过 Git 管理；交付版本应能明确对应源码和依赖。不把事后反向重建的代码当作交付源码。

## Git 共享审计

当前工作目录没有 `.git`，因此无法验证曾被跟踪的业务文件或历史提交。连接已有仓库或首次共享前，应检查 `git status --short`、`git ls-files` 和 `git log --all --name-only`，重点核对业务 PPT、图片、文档、原型及历史交付物。`.gitignore` 只阻止新文件默认进入索引，不会移除已跟踪内容或清除历史。如果发现业务资料已被跟踪，应先报告路径和共享风险，再确定仅从索引移除还是需要另行处理历史；不要擅自改写历史或删除本地资料。
