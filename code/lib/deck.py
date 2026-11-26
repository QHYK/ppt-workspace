"""Shared editable PowerPoint drawing and page layout primitives."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

from code.themes import Theme


class Deck:
    """Theme-aware drawing API; all coordinates are inches."""

    def __init__(self, theme: Theme, *, icon_dir: Path, footer_label: str = "", chapters=None):
        self.theme = theme
        self.icon_dir = Path(icon_dir)
        self.footer_label = footer_label
        self.chapters = chapters or {}
        self.ppt = Presentation()
        self.ppt.slide_width = Inches(theme.width)
        self.ppt.slide_height = Inches(theme.height)

    def rgb(self, key: str) -> RGBColor:
        return RGBColor.from_string(self.theme.color(key))

    def rect(self, slide, x, y, width, height, fill, *, radius=False, line=None, shape=None):
        """Add a native filled shape using theme colors or an explicit hex color."""
        kind = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE)
        item = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(width), Inches(height))
        item.fill.solid()
        item.fill.fore_color.rgb = self.rgb(fill)
        if line:
            item.line.color.rgb = self.rgb(line)
            item.line.width = Pt(0.5)
        else:
            item.line.fill.background()
        for effect in item._element.xpath("./p:style/a:effectRef"):
            effect.set("idx", "0")
        return item

    def connector(self, slide, x1, y1, x2, y2, color="sage", width=1.1):
        """Connect two positions with an editable straight PowerPoint line."""
        item = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
        )
        item.line.color.rgb = self.rgb(color)
        item.line.width = Pt(width)
        return item

    def text_box(
        self, slide, x, y, width, height, text, size=None, color="ink", bold=False,
        *, align=PP_ALIGN.LEFT, margin=0.02,
    ):
        """Add editable text; newlines become separate styled paragraphs."""
        size = size if size is not None else self.theme.type_scale["body"]
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(width), Inches(height))
        frame = box.text_frame
        frame.word_wrap = True
        frame.margin_left = frame.margin_right = Inches(margin)
        frame.margin_top = Inches(0.02)
        frame.margin_bottom = 0
        for index, line in enumerate(str(text).split("\n")):
            para = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
            para.text = line
            para.alignment = align
            para.space_after = Pt(0)
            para.line_spacing = 1.08
            for run in para.runs:
                run.font.name = self.theme.font
                run.font.size = Pt(size)
                run.font.bold = bold
                run.font.color.rgb = self.rgb(color)
        return box

    def bullet_list(
        self, slide, x, y, width, height, items, *, size=None,
        color="muted", after=5, line_spacing=1.1,
    ):
        """Create native PowerPoint bullets from a sequence of strings."""
        size = size if size is not None else self.theme.type_scale["bullet"]
        if isinstance(items, str):
            return self.text_box(slide, x, y, width, height, items, size, color)
        box = self.text_box(slide, x, y, width, height, "", size, color)
        frame = box.text_frame
        frame.clear()
        for index, item in enumerate(items):
            para = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
            para.text = item
            para.level = 0
            para.space_after = Pt(after)
            para.line_spacing = line_spacing
            props = para._p.get_or_add_pPr()
            props.set("marL", str(Pt(15)))
            props.set("indent", str(Pt(-10)))
            bullet = OxmlElement("a:buChar")
            bullet.set("char", "•")
            props.append(bullet)
            for run in para.runs:
                run.font.name = self.theme.font
                run.font.size = Pt(size)
                run.font.color.rgb = self.rgb(color)
        return box

    def icon(self, slide, name, x, y, size=None):
        """Embed a cached Lucide PNG from the shared icon directory."""
        size = self.theme.layout.get("icon_size", 0.38) if size is None else size
        path = self.icon_dir / f"{name}.png"
        if not path.is_file():
            raise FileNotFoundError(path)
        return slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(size), Inches(size))

    def add_image_fit(self, slide, path, x, y, width, height):
        """Fit a local image inside a box without changing its aspect ratio."""
        path = Path(path)
        if not path.is_file():
            raise FileNotFoundError(path)
        with Image.open(path) as image:
            iw, ih = image.size
        scale = min(width / iw, height / ih)
        fw, fh = iw * scale, ih * scale
        return slide.shapes.add_picture(
            str(path), Inches(x + (width - fw) / 2), Inches(y + (height - fh) / 2),
            Inches(fw), Inches(fh),
        )

    def add_image_top_focus(self, slide, path, x, y, width, height):
        """Fill a wide box with the top section of a tall source image."""
        path = Path(path)
        if not path.is_file():
            raise FileNotFoundError(path)
        with Image.open(path) as image:
            iw, ih = image.size
        picture = slide.shapes.add_picture(str(path), Inches(x), Inches(y), width=Inches(width))
        picture.height = Inches(height)
        picture.crop_bottom = max(0, 1 - (height / width * iw) / ih)
        return picture

    def footer(self, slide, dark=False):
        """Add the standard page rule, footer label and current page number."""
        layout = self.theme.layout
        fg = "sage" if dark else "muted"
        self.rect(slide, layout["left"], layout["footer_line_y"], self.theme.width - layout["left"] - layout["right"], 0.012, "sage")
        self.text_box(slide, layout["left"], layout["footer_line_y"] + 0.06, 10.8, 0.25, self.footer_label, self.theme.type_scale["footer"], fg)
        self.text_box(slide, self.theme.width - 1.33, layout["footer_line_y"] + 0.04, 0.7, 0.28, f"{len(self.ppt.slides):02}", 10, fg)

    def base_slide(self, chapter, topic, title, subtitle="", *, dark=False):
        """Create a slide with the theme background and shared editorial hierarchy."""
        layout = self.theme.layout
        slide = self.ppt.slides.add_slide(self.ppt.slide_layouts[6])
        self.rect(slide, 0, 0, self.theme.width, self.theme.height, "dark" if dark else "background")
        if chapter in self.chapters:
            label = f"{chapter} {self.chapters[chapter]}"
            first_color = "sage" if dark else "green"
            caption = self.text_box(slide, layout["left"], layout["caption_y"], 12, 0.35, label + " / ", self.theme.type_scale["caption"], first_color, True)
            run = caption.text_frame.paragraphs[0].add_run()
            run.text = topic
            run.font.name = self.theme.font
            run.font.size = Pt(self.theme.type_scale["caption"])
            run.font.bold = True
            run.font.color.rgb = self.rgb("white" if dark else "dark")
        else:
            self.text_box(slide, layout["left"], layout["caption_y"], 12, 0.35, topic, self.theme.type_scale["caption"], "sage" if dark else "green", True)
        self.text_box(slide, layout["left"], layout["title_y"], 12.2, 0.69, title, self.theme.type_scale["title"], "white" if dark else "dark", True)
        if subtitle:
            self.text_box(slide, layout["left"] + 0.02, layout["subtitle_y"], 12.1, 0.48, subtitle, self.theme.type_scale["subtitle"], "sage" if dark else "muted")
        self.footer(slide, dark)
        return slide

    def _cell_border(self, cell):
        props = cell._tc.get_or_add_tcPr()
        for edge in ("lnL", "lnR", "lnT", "lnB"):
            line = OxmlElement("a:" + edge)
            line.set("w", "6350")
            fill = OxmlElement("a:solidFill")
            color = OxmlElement("a:srgbClr")
            color.set("val", self.theme.colors["border"])
            fill.append(color)
            line.append(fill)
            props.append(line)

    def native_table(
        self, *, chapter, topic, title, subtitle, headers, rows, widths,
        dense=False, row_colors=None,
    ):
        """Create an editable table with alternating body rows and optional first-column colors."""
        slide = self.base_slide(chapter, topic, title, subtitle)
        top = self.theme.layout["content_y"]
        height = self.theme.layout["content_h"]
        table = slide.shapes.add_table(
            len(rows) + 1, len(headers), Inches(self.theme.layout.get("table_left", 0.56)), Inches(top),
            Inches(sum(widths)), Inches(height),
        ).table
        for index, width in enumerate(widths):
            table.columns[index].width = Inches(width)
        row_height = height / (len(rows) + 1)
        for row_index, row in enumerate([headers] + list(rows)):
            table.rows[row_index].height = Inches(row_height)
            for col_index, value in enumerate(row):
                cell = table.cell(row_index, col_index)
                cell.text = str(value)
                fill = "dark" if row_index == 0 else ("white" if row_index % 2 else "pale")
                cell.fill.solid()
                cell.fill.fore_color.rgb = self.rgb(fill)
                cell.margin_left = cell.margin_right = Inches(0.10)
                cell.margin_top = cell.margin_bottom = Pt(3 if dense else 5)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                self._cell_border(cell)
                for para in cell.text_frame.paragraphs:
                    para.alignment = PP_ALIGN.LEFT
                    para.space_after = Pt(0)
                    para.line_spacing = 1.03
                    for run in para.runs:
                        run.font.name = self.theme.font
                        scale = self.theme.type_scale
                        run.font.size = Pt(scale["table_header"] if row_index == 0 else (scale["table_dense"] if dense else scale["table_body"]))
                        run.font.bold = row_index == 0
                        run.font.color.rgb = self.rgb("white" if row_index == 0 else "ink")
                        if row_index and col_index == 0 and row_colors:
                            run.font.color.rgb = self.rgb(row_colors.get(str(value), "ink"))
                            run.font.bold = True
        return slide

    def motif(self, slide, x, y, width, height, mode):
        """Draw a repeatable abstract cluster of native ovals for a cover accent."""
        rng = random.Random(7 + mode)
        palette = self.theme.motif_palette
        if not palette:
            raise ValueError("Theme must provide motif_palette for motif()")
        for index in range(48):
            angle = rng.random() * 6.28
            radius = math.sqrt(rng.random())
            xx = x + width / 2 + math.cos(angle) * radius * width * 0.43
            yy = y + height / 2 + math.sin(angle) * radius * height * 0.43
            size = rng.uniform(0.08, 0.35)
            self.rect(slide, xx, yy, size * 1.6, size, palette[index % 4], shape=MSO_SHAPE.OVAL)

    def list_panel(self, slide, x, y, width, height, *, title, items, icon_name=None, body_size=16):
        """Place a titled list in a bordered panel with optional icon."""
        self.rect(slide, x, y, width, height, "white", line="border")
        self.rect(slide, x, y, 0.055, height, "green")
        title_x = x + 0.25
        if icon_name:
            self.icon(slide, icon_name, x + 0.26, y + 0.20, 0.39)
            title_x = x + 0.77
        self.text_box(slide, title_x, y + 0.20, width - (title_x - x) - 0.2, 0.45, title, 21, "dark", True)
        self.bullet_list(slide, x + 0.26, y + 0.78, width - 0.5, height - 0.9, items, size=body_size, after=7)

    def statement_card(self, slide, x, y, width, height, *, icon_name, title, description):
        """Place a short icon, title and explanation in a bordered card."""
        self.rect(slide, x, y, width, height, "white", line="border")
        self.icon(slide, icon_name, x + 0.25, y + 0.24, 0.42)
        self.text_box(slide, x + 0.8, y + 0.25, width - 1.05, 0.46, title, 20, "dark", True)
        self.text_box(slide, x + 0.26, y + 0.81, width - 0.50, height - 0.9, description, 18, "muted")

    def feature_card(self, slide, x, y, width, height, data):
        """Place a compact feature summary and bullet list in a bordered card."""
        self.rect(slide, x, y, width, height, "white", line="border")
        self.text_box(slide, x + 0.23, y + 0.10, width - 0.45, 0.22, data["caption"], 10, "green", True)
        self.icon(slide, data["icon"], x + 0.23, y + 0.34, 0.32)
        self.text_box(slide, x + 0.69, y + 0.31, width - 0.91, 0.39, data["title"], 20, "dark", True)
        self.text_box(slide, x + 0.25, y + 0.72, width - 0.5, 0.32, data["description"], 13.5, "muted")
        self.rect(slide, x + 0.25, y + 1.07, width - 0.5, 0.012, "border")
        self.bullet_list(slide, x + 0.26, y + 1.12, width - 0.52, height - 1.17, data["bullets"], size=13.5, after=0.5, line_spacing=1.0)

    def simple_card(self, slide, x, y, width, height, title, body, *, icon_name=None, size=16):
        """Place a title and list or body text in a simple bordered card."""
        self.rect(slide, x, y, width, height, "white", line="border")
        title_x = x + 0.22
        if icon_name:
            self.icon(slide, icon_name, x + 0.21, y + 0.17, 0.36)
            title_x = x + 0.67
        self.text_box(slide, title_x, y + 0.15, width - (title_x - x) - 0.2, 0.43, title, 20, "dark", True)
        self.bullet_list(slide, x + 0.22, y + 0.72, width - 0.44, height - 0.8, body, size=size)

    def card(
        self, slide, x, y, width, height, *, title, body,
        number=None, icon_name=None, fill="white", title_size=None, body_size=None,
    ):
        """Draw the shared white, lightly bordered card with a clear text hierarchy."""
        title_size = title_size if title_size is not None else self.theme.type_scale["card_title"]
        body_size = body_size if body_size is not None else self.theme.type_scale["card_body"]
        pad = self.theme.layout.get("card_pad", 0.22)
        self.rect(slide, x, y, width, height, fill, line="border")
        if number is not None:
            self.text_box(slide, x + pad, y + 0.20, width - 2 * pad, 0.32, number, 13, "green", True)
        if icon_name:
            self.icon(slide, icon_name, x + width - pad - 0.30, y + 0.18, 0.30)
        title_y = y + (0.75 if number is not None else 0.26)
        self.text_box(slide, x + pad, title_y, width - 2 * pad, 0.48, title, title_size, "dark", True)
        if body:
            self.text_box(slide, x + pad, title_y + 0.73, width - 2 * pad, height - (title_y - y) - 0.83, body, body_size, "ink")

    def note_strip(self, slide, text, *, y=6.35):
        """Draw a full-width dark note without changing the page content grid."""
        left = self.theme.layout["left"]
        self.rect(slide, left, y, self.theme.width - left - self.theme.layout["right"], 0.48, "dark")
        self.text_box(slide, left + 0.19, y + 0.11, self.theme.width - left - self.theme.layout["right"] - 0.38, 0.30, text, 11.5, "white")

    def open_link(self, box, address):
        """Attach a click target to an existing one-run text box."""
        run = box.text_frame.paragraphs[0].runs[0]
        run.hyperlink.address = address
        run.font.color.rgb = self.rgb("muted")
        run.font.underline = False

    def save(self, path: Path):
        """Write the current deck to an output path, creating its directory."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.ppt.save(str(path))
        return path
