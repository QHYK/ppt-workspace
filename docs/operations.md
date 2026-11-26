# 安装、验证与共享

依赖版本以根目录 [`pyproject.toml`](../pyproject.toml) 为准。需要 Python 3.11 或更新版本；先用 `python3 --version` 确认版本，必要时将下面的 `python3` 替换为较新版本的命令。在项目根目录安装并验证公共部分：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python slides/example/build.py
.venv/bin/python -m unittest discover -s code/tests -v
```

公共测试只使用公共 Library、Theme、图标、示意素材和 `slides/example/`。示例 PPTX 输出到示例目录，生成结果默认不进入 Git。业务项目在本地按相同方式运行自己的 `build.py`，不作为公共测试的依赖。

修改组件或 Theme 后，重新生成示例并逐页渲染检查；如果本地业务项目受到影响，也重建并检查其页面。检查文字截断、字体、重叠、越界、对齐、间距、图片、图标和结构图表达。中文预览应使用 PowerPoint 或支持中文字体的渲染器；缺少 `Noto Sans CJK SC` 的 LibreOffice 环境不能用于中文文字验收。

正式交付业务 PPT 时提供可编辑 PPTX、实际生成源码、必要依赖和素材，以及逐页预览。交付版本应能对应源码和依赖。

## Git 共享检查

新复制的工作目录如尚无 Git 仓库，可先运行 `git init`。**初始化不会自动选择可共享文件**。首次提交或后续提交前，先检查：

```bash
git status --short --untracked-files=all
git status --short --ignored
git ls-files
git log --all --name-only
```

其中 `git log` 在空仓库中没有历史记录，报错可忽略；已有仓库则应检查历史是否包含业务 PPT、素材、文档、原型或交付物。确认当前文件范围后，仅暂存需要共享的路径，例如：

```bash
git add .gitignore AGENTS.md README.md pyproject.toml code/ assets/icons/ assets/shared/ docs/ slides/example/build.py
git diff --cached --name-only
git diff --cached --check
```

逐项审阅暂存清单和 diff，再执行提交。确认 `docs/projects/`、业务项目和业务素材没有进入索引；`.gitignore` 不会移除已跟踪内容，也不会清理历史。发现业务资料时先停止共享并评估处理方式，不擅自删除本地资料或改写 Git 历史。推送和创建远程仓库另行决定。
