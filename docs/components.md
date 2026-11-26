# 公共组件

接口以 [`code/lib/deck.py`](../code/lib/deck.py) 和 [`code/lib/diagrams.py`](../code/lib/diagrams.py) 为准；重要函数的用途与关键行为见代码注释。坐标使用英寸，颜色可使用 Theme 键或十六进制值。

| 能力 | 主要接口 | 用途 |
| --- | --- | --- |
| Typography / Shape | `text_box`、`bullet_list`、`rect`、`connector` | 原生文字与图形。 |
| Card / Layout | `card`、`list_panel`、`statement_card`、`feature_card`、`simple_card`、`base_slide`、`footer` | 信息单元与页面骨架。 |
| Table | `native_table` | 可编辑表格。 |
| Image / Icon | `add_image_fit`、`add_image_top_focus`、`icon` | 本地素材嵌入；缺失素材报错。 |
| Structure diagrams | `framework`、`flowchart`、`timeline`、`gantt`、`relationship` | 原生可编辑结构图。 |

开发新页面前先检查已有组件。能满足需求时直接复用；需要扩展时增加合理参数或兼容行为，不重复实现相同绘制逻辑。只有具备明确复用价值的能力才进入公共库，项目特殊布局留在业务脚本中。公共组件接收必要的位置、尺寸、内容和样式参数，不包含业务事实或页码。

可运行的调用方式见[组件示例源码](../slides/example/build.py)。默认 Card 的样式约定见[设计系统](design-system.md)。
