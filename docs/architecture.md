# PPT 开发架构

Python 源码是演示稿的 Source of Truth，使用 `python-pptx` 输出可编辑 PPTX。公共项目可以仅凭下表中的公共文件安装、运行测试并生成组件示例，不读取本地业务资产或历史 PPTX。

| 路径 | 职责与共享边界 |
| --- | --- |
| `code/lib/` | 公共绘制、布局和结构图组件；共享。 |
| `code/themes/` | 默认 Theme 与轻量覆盖机制；共享。 |
| `code/tests/` | 只验证公共能力和组件示例；共享。 |
| `slides/example/` | 非业务组件示例源码与视觉回归样本；共享源码。 |
| `assets/icons/`、`assets/shared/` | 公共图标和示意素材；共享。 |
| `docs/` | 公共技术文档和公共库变更记录；共享。 |
| `slides/<项目名>/`、`assets/images/`、`docs/projects/` | 本地业务源码、图片和文档；默认忽略。 |
| `references/`、`prototype/` | 本地参考资料与独立原型；默认忽略。 |

`code/scripts/` 仅在出现可复用的素材转换、渲染或检查需求时增加脚本。根目录的 `AGENTS.md`、`README.md`、`pyproject.toml` 和 `.gitignore` 属于公共项目。

依赖方向为 `slides/example → code/lib + code/themes + assets`；业务项目遵循同样方向，并在自己的目录定义内容与必要的 Theme 覆盖。公共 Library 和 Theme 不依赖业务项目、业务页码、业务素材或历史输出。每个业务项目维护独立的主要 `build.py`；项目专属布局留在项目内，不复制公共绘制逻辑。

正常迭代不读取上一版 PPTX、修改 DrawingML XML 或复制特定页面图形。不硬编码本机绝对路径，不静默忽略生成错误和缺失素材。确需底层 XML 时，将通用能力封装在公共方法中。`.gitignore` 只限制新的 Git 跟踪；已有跟踪文件及历史提交须另行审计，见[操作文档](operations.md)。
