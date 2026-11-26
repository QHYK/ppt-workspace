"""Build a non-business visual catalog of the shared PowerPoint components."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pptx.enum.text import PP_ALIGN

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from code.lib import Deck, flowchart, framework, gantt, relationship, timeline
from code.themes import DEFAULT

OUTPUT = Path(__file__).with_name("component_showcase.pptx")
ICONS = ROOT / "assets" / "icons"
SAMPLE_IMAGE = ROOT / "assets" / "shared" / "abstract-forms.png"


def build(output: Path = OUTPUT) -> Path:
    """Generate eleven editable slides using only shared code and sample assets."""
    deck = Deck(DEFAULT, icon_dir=ICONS, footer_label="PPT COMPONENT SHOWCASE")

    cover = deck.base_slide("", "DESIGN SYSTEM / EXAMPLE", "公共组件展示", "默认 Theme · 可编辑组件 · 非业务内容", dark=True)
    deck.text_box(cover, 0.75, 3.05, 7.4, 1.4, "Clear structure\nConsistent details", 34, "white", True)
    deck.motif(cover, 8.0, 2.0, 4.4, 4.5, 1)

    slide = deck.base_slide("", "01 / TYPOGRAPHY", "文字与间距", "公共字号、颜色和页面骨架")
    deck.text_box(slide, 0.68, 2.34, 5.7, 0.45, "Section heading", 22, "dark", True)
    deck.text_box(slide, 0.68, 2.92, 5.7, 0.70, "Readable body copy uses clear contrast and a comfortable line length.", 18, "ink")
    deck.text_box(slide, 0.68, 3.80, 5.7, 0.50, "Secondary information stays quieter.", 15, "muted")
    deck.bullet_list(slide, 0.70, 4.52, 5.7, 1.40, ["Editable text", "Theme colors", "Consistent rhythm"], size=16)
    deck.rect(slide, 7.18, 2.37, 4.72, 0.84, "dark")
    deck.text_box(slide, 7.45, 2.62, 4.2, 0.3, "PRIMARY / DARK", 15, "white", True)
    deck.rect(slide, 7.18, 3.44, 4.72, 0.84, "green")
    deck.text_box(slide, 7.45, 3.69, 4.2, 0.3, "ACCENT / GREEN", 15, "white", True)
    deck.rect(slide, 7.18, 4.51, 4.72, 0.84, "pale")
    deck.text_box(slide, 7.45, 4.76, 4.2, 0.3, "SURFACE / PALE", 15, "dark", True)
    deck.connector(slide, 7.18, 5.70, 11.90, 5.70, "sage", 1.2)

    slide = deck.base_slide("", "02 / CARD", "默认信息卡", "白底、细边框、统一内边距与信息层级")
    gap = DEFAULT.layout["card_gap"]
    width = (12.23 - gap * 2) / 3
    for index, (title, body, icon_name) in enumerate([
        ("Clear title", "A short explanation remains easy to scan.", "file-text"),
        ("Useful grouping", "Related information stays within one visual unit.", "layout-dashboard"),
        ("Flexible content", "Cards accept optional icons, numbers and themes.", "palette"),
    ]):
        deck.card(slide, 0.55 + index * (width + gap), 2.26, width, 3.62,
                  title=title, body=body, number=f"{index + 1:02}", icon_name=icon_name)

    slide = deck.base_slide("", "03 / PANELS", "卡片变体与列表", "使用现有组件处理不同信息密度")
    deck.statement_card(slide, 0.55, 2.26, 5.84, 1.52, icon_name="shield-check",
                        title="Statement card", description="An icon, heading and brief explanation.")
    deck.simple_card(slide, 0.55, 4.08, 5.84, 2.38, "Simple card",
                     ["One concise point", "A second supporting point"], icon_name="list-tree", size=16)
    deck.feature_card(slide, 6.69, 2.26, 6.08, 4.20, {
        "caption": "FEATURE / 01", "icon": "code-xml", "title": "Feature card",
        "description": "A structured summary for denser material.",
        "bullets": ["Context and purpose", "Key capabilities", "Next step"],
    })

    deck.native_table(
        chapter="", topic="04 / TABLE", title="可编辑表格", subtitle="主题色、行间距和文字层级保持一致",
        headers=["Component", "Typical use", "Editable"],
        rows=[
            ("Card", "Grouped information", "Yes"),
            ("Table", "Structured comparison", "Yes"),
            ("Timeline", "Milestones", "Yes"),
            ("Image", "Visual reference", "Embedded"),
        ],
        widths=[3.15, 5.73, 3.35],
    )

    slide = deck.base_slide("", "05 / FRAMEWORK", "战略框架图", "层级与分支均由原生图形组成")
    framework(deck, slide, tiers=["Overall direction", "Shared priorities"], branches=[
        ("Plan", "Define scope"), ("Build", "Create assets"), ("Review", "Check results"),
    ], x=0.75, y=2.40, width=11.85)

    slide = deck.base_slide("", "06 / FLOWCHART", "流程图", "步骤、连接和说明均可编辑")
    flowchart(deck, slide, steps=[
        ("Discover", "Collect requirements"),
        ("Design", "Choose a layout"),
        ("Build", "Generate slides"),
        ("Review", "Render and inspect"),
    ], x=0.55, y=2.47, width=12.23, height=3.12)

    slide = deck.base_slide("", "07 / TIMELINE", "时间轴", "相同间距组织阶段与里程碑")
    timeline(deck, slide, milestones=[
        ("W1", "Outline", "Agree on content"),
        ("W2", "Draft", "Build the slides"),
        ("W3", "Review", "Check visuals"),
        ("W4", "Deliver", "Share source"),
    ], x=0.55, y=2.35, width=12.23, height=3.62, highlight=2)

    slide = deck.base_slide("", "08 / GANTT", "轻量甘特图", "适合简短排期与职责展示")
    gantt(deck, slide, periods=["Week 1", "Week 2", "Week 3", "Week 4"], rows=[
        ("Outline", 0, 0, "green", "Scope"),
        ("Content", 0, 1, "green", "Draft"),
        ("Visuals", 1, 2, "dark", "Design"),
        ("Review", 2, 3, "gold", "Check"),
        ("Delivery", 3, 3, "green", "Share"),
    ], x=0.67, y=2.57, label_width=3.05, width=8.82, row_height=0.58)

    slide = deck.base_slide("", "09 / RELATIONSHIP + IMAGE", "关系图与图片", "组合原生图形和可替换的公共示意素材")
    relationship(deck, slide, center="Shared goal", satellites=[
        ("Content", "What to say"), ("Design", "How it reads"),
        ("Build", "Editable output"), ("Review", "Quality check"),
    ], x=0.55, y=2.39, width=7.08, height=3.56)
    deck.rect(slide, 8.02, 2.39, 4.68, 3.34, "white", line="border")
    deck.add_image_fit(slide, SAMPLE_IMAGE, 8.17, 2.54, 4.38, 2.78)
    deck.text_box(slide, 8.17, 5.38, 4.38, 0.25, "Reusable sample image", 11, "muted", align=PP_ALIGN.CENTER)

    slide = deck.base_slide("", "10 / LIST + IMAGE", "列表面板与图片裁切", "补充展示密集文本和本地图片的常用处理方式")
    deck.list_panel(slide, 0.55, 2.37, 5.86, 3.40, title="List panel", icon_name="list-tree",
                    items=["State the purpose", "Group related points", "Keep enough white space"], body_size=17)
    deck.rect(slide, 6.76, 2.37, 6.01, 3.40, "white", line="border")
    deck.add_image_top_focus(slide, SAMPLE_IMAGE, 6.94, 2.55, 5.65, 2.65)
    deck.text_box(slide, 6.94, 5.34, 5.65, 0.27, "Top-focused image placement", 11, "muted", align=PP_ALIGN.CENTER)
    deck.note_strip(slide, "A shared note strip highlights one important takeaway.", y=6.28)

    return deck.save(output)


def main() -> None:
    """Parse an optional output path for local builds and isolated tests."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build(args.output)
    print(f"Saved {result}")


if __name__ == "__main__":
    main()
