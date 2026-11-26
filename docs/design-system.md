# 设计系统

[`code/themes/theme.py`](../code/themes/theme.py) 中的 `DEFAULT` 是共享设计基线，沿用已有的科学编辑风格：暖白页面、深绿标题、克制的绿色强调和舒展留白。项目通过 `DEFAULT.override(colors=..., layout=..., type_scale=...)` 覆盖品牌色及必要参数；未指定的参数沿用基线，不复制一整套 Theme。

通用文字层级、页面边距、Card 间距、Footer、Table 和 Icon 的基础值由 Theme 管理。基础 Card 使用白底、细边框、统一内边距，以及编号／图标、标题、正文的清晰顺序；背景色和强调色可随项目 Theme 变化。Footer 使用相同的细分隔线、标签和页码规则。表格沿用深色表头、交替浅色行及可编辑文字。视觉细节以组件代码和[组件示例](../slides/example/build.py)的渲染结果为准。

根据内容选择卡片、表格或结构图，不机械套用一种布局。保持对齐、间距、对比度和留白；文字、表格及结构图优先使用 PowerPoint 原生可编辑元素。单页特殊处理不应改变其他页面的默认样式。

图标优先选用 Lucide，先查本地，再将 SVG 原件和嵌入用 PNG 放在 `assets/icons/`；来源与许可见[图标说明](../assets/icons/README.md)。公共示意图片放在 `assets/shared/`，业务图片放在本地 `assets/images/`。图片与 Logo 应区分真实资料和设计示意，示意内容须明确标注。生成 PPT 不依赖运行时网络。
