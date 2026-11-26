# Python PPT 开发项目

本项目用 Python 和 `python-pptx` 生成可编辑演示稿。公共 Library 负责绘制与布局，Theme 提供默认设计参数，具体 PPT 的内容与项目覆盖配置留在本地业务目录。仓库内的组件示例可用于学习接口和检查视觉变化。

## 安装与验证

需要 Python 3.11 或更新版本。在项目根目录运行：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python slides/example/build.py
.venv/bin/python -m unittest discover -s code/tests -v
```

示例源码位于 [`slides/example/build.py`](slides/example/build.py)，输出到同目录的 `component_showcase.pptx`。这里的可编辑安装只用于本地开发，不表示发布独立 Python Package。

## 新建业务 PPT

1. 先与 AI 或团队成员讨论并确认需求、核心思路、内容大纲和逐页描述。
2. 在 `slides/<项目名>/build.py` 编写页面内容和布局，调用 [公共组件](docs/components.md)；需要品牌变化时用 [Theme 覆盖](docs/design-system.md)。
3. 业务图片放在 `assets/images/`，业务文档放在 `docs/projects/`，参考资料放在 `references/`。这些目录和新增的 `slides/<项目名>/` 默认不进入公共仓库。
4. 从源码生成 PPTX，运行相关测试并逐页渲染检查，操作约定见 [Operations](docs/operations.md)。

公共项目可直接使用 `DEFAULT`：

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from code.lib import Deck
from code.themes import DEFAULT

theme = DEFAULT.override(colors={"green": "247F78", "dark": "143B40"})
deck = Deck(theme, icon_dir=ROOT / "assets" / "icons", footer_label="YOUR DECK")
slide = deck.base_slide("", "SECTION", "Slide title", "Supporting sentence")
deck.card(slide, 0.55, 2.25, 3.8, 3.5, title="Card title", body="Card content", number="01")
deck.save(Path(__file__).with_name("output.pptx"))
```

上例适用于 `slides/<项目名>/build.py`；更完整的入口见组件示例源码。已有素材中只有 `assets/icons/` 和 `assets/shared/` 是公共资源。业务项目可以保留自己的 Theme 覆盖和素材，不必复制公共 Library。

## Example Prompt

在使用前，将下面的占位符替换为已确认的需求：

> 请基于当前项目的公共 Library、默认 Theme 和组件示例，设计并生成一份可编辑 PPT。先阅读 AGENTS.md 和 docs/00-index.md，复用公共组件；将业务内容和素材留在默认忽略的本地项目目录。生成后运行相关测试，逐页渲染检查，并按 AGENTS.md 汇报。
>
> {{请将已经讨论确认的 PPT 需求、核心思路、内容大纲、逐页描述及相关要求替换到这里。也可以提供对应的本地文档路径。}}

## 共享边界

[`.gitignore`](.gitignore) 默认排除业务项目、业务图片、业务文档、参考资料、原型和生成结果。忽略规则不会移除已经被 Git 跟踪的文件，也不会清除历史提交；连接或发布仓库前，按 [共享检查步骤](docs/operations.md)核对跟踪状态与历史。
