"""Reusable native-shape diagrams; inputs are content, coordinates and style keys."""

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN


def framework(deck, slide, *, tiers, branches, x, y, width, tier_height=0.47, gap=0.16):
    """Stack centered strategy tiers above an equally spaced branch row."""
    if not tiers or not branches:
        raise ValueError("framework requires tiers and branches")
    for index, label in enumerate(tiers):
        yy = y + index * (tier_height + gap)
        deck.rect(slide, x + width * 0.17, yy, width * 0.66, tier_height, "dark" if index == 0 else "green")
        deck.text_box(slide, x + width * 0.18, yy + 0.06, width * 0.64, 0.33, label, 17, "white", True, align=PP_ALIGN.CENTER)
    start = y + len(tiers) * (tier_height + gap) + 0.15
    cell_width = (width - gap * (len(branches) - 1)) / len(branches)
    for index, (heading, detail) in enumerate(branches):
        xx = x + index * (cell_width + gap)
        deck.rect(slide, xx, start, cell_width, 1.00, "pale")
        deck.text_box(slide, xx + 0.08, start + 0.16, cell_width - 0.16, 0.31, heading, 15, "dark", True, align=PP_ALIGN.CENTER)
        deck.text_box(slide, xx + 0.08, start + 0.59, cell_width - 0.16, 0.27, detail, 12, "muted", align=PP_ALIGN.CENTER)


def flowchart(deck, slide, *, steps, x, y, width, height, fill="pale"):
    """Horizontal cards with editable arrow connectors."""
    if not steps:
        raise ValueError("flowchart requires at least one step")
    gap = 0.21
    card_width = (width - gap * (len(steps) - 1)) / len(steps)
    for index, (heading, detail) in enumerate(steps):
        xx = x + index * (card_width + gap)
        deck.rect(slide, xx, y, card_width, height, fill)
        deck.text_box(slide, xx + 0.22, y + 0.20, card_width - 0.44, 0.35, f"{index + 1:02}", 14, "green", True)
        deck.text_box(slide, xx + 0.22, y + 0.78, card_width - 0.44, 0.50, heading, 19, "dark", True)
        deck.text_box(slide, xx + 0.22, y + 1.48, card_width - 0.44, height - 1.65, detail, 14, "ink")
        if index < len(steps) - 1:
            deck.text_box(slide, xx + card_width - 0.02, y + height * 0.45, gap + 0.04, 0.40, "›", 21, "green", True, align=PP_ALIGN.CENTER)


def timeline(deck, slide, *, milestones, x, y, width, height, highlight=None, cards=True):
    """Equal milestones on a line; optionally place each one on a pale card."""
    if not milestones:
        raise ValueError("timeline requires at least one milestone")
    if highlight is not None and not 0 <= highlight < len(milestones):
        raise ValueError("highlight must identify a milestone")
    gap = 0.20
    card_width = (width - gap * (len(milestones) - 1)) / len(milestones)
    line_y = y + 1.05
    if cards:
        for index in range(len(milestones)):
            xx = x + index * (card_width + gap)
            deck.rect(slide, xx, y, card_width, height, "pale")
    deck.connector(slide, x + card_width / 2, line_y, x + width - card_width / 2, line_y, "green", 1.2)
    for index, (when, heading, detail) in enumerate(milestones):
        xx = x + index * (card_width + gap)
        color = "gold" if index == highlight else "green"
        deck.text_box(slide, xx + 0.15, y + 0.18, card_width - 0.30, 0.40, when, 16, color, True, align=PP_ALIGN.CENTER)
        center = xx + card_width / 2
        deck.rect(slide, center - 0.12, line_y - 0.12, 0.24, 0.24, color, shape=MSO_SHAPE.OVAL)
        deck.text_box(slide, xx + 0.12, y + 1.42, card_width - 0.24, 0.48, heading, 19, "dark", True, align=PP_ALIGN.CENTER)
        deck.text_box(slide, xx + 0.12, y + 2.10, card_width - 0.24, height - 2.23, detail, 14, "muted", align=PP_ALIGN.CENTER)


def gantt(deck, slide, *, periods, rows, x, y, label_width, width, row_height=0.44):
    """Lightweight native Gantt. Rows: (label, start, end, color, annotation)."""
    if not periods:
        raise ValueError("gantt requires at least one period")
    for _, start, end, _, _ in rows:
        if not 0 <= start <= end < len(periods):
            raise ValueError("gantt row range is outside periods")
    grid_x = x + label_width
    step = width / len(periods)
    for index, period in enumerate(periods):
        xx = grid_x + index * step
        deck.text_box(slide, xx, y, step, 0.29, period, 13, "dark", True, align=PP_ALIGN.CENTER)
        deck.connector(slide, xx, y + 0.40, xx, y + 0.50 + len(rows) * row_height, "border", 0.6)
    for index, (label, start, end, color, annotation) in enumerate(rows):
        yy = y + 0.52 + index * row_height
        deck.text_box(slide, x + 0.03, yy, label_width - 0.10, 0.30, label, 13, "dark", True)
        bar_x = grid_x + start * step + 0.03
        bar_w = (end - start + 1) * step - 0.06
        deck.rect(slide, bar_x, yy, bar_w, 0.25, color)
        if annotation:
            deck.text_box(slide, bar_x + 0.05, yy + 0.015, max(bar_w - 0.1, 0.3), 0.22, annotation, 10, "white", True)


def relationship(deck, slide, *, center, satellites, x, y, width, height):
    """A central editable node connected to four or more surrounding nodes."""
    cx = x + width * 0.5
    cy = y + height * 0.5
    center_w, center_h = width * 0.28, 0.85
    spots = [(0.08, 0.08), (0.72, 0.08), (0.08, 0.72), (0.72, 0.72)]
    if len(satellites) > len(spots):
        raise ValueError("relationship supports at most four satellites")
    # Draw lines before nodes so the connections do not cross their text.
    for (heading, detail), (rx, ry) in zip(satellites, spots):
        xx, yy = x + width * rx, y + height * ry
        box_w, box_h = width * 0.20, 0.72
        deck.connector(slide, cx, cy, xx + box_w / 2, yy + box_h / 2, "green", 0.9)
    deck.rect(slide, cx - center_w / 2, cy - center_h / 2, center_w, center_h, "dark")
    deck.text_box(slide, cx - center_w / 2 + 0.10, cy - 0.28, center_w - 0.20, 0.60, center, 16, "white", True, align=PP_ALIGN.CENTER)
    for (heading, detail), (rx, ry) in zip(satellites, spots):
        xx, yy = x + width * rx, y + height * ry
        box_w, box_h = width * 0.20, 0.72
        deck.rect(slide, xx, yy, box_w, box_h, "pale")
        deck.text_box(slide, xx + 0.05, yy + 0.10, box_w - 0.10, 0.25, heading, 14, "dark", True, align=PP_ALIGN.CENTER)
        deck.text_box(slide, xx + 0.05, yy + 0.43, box_w - 0.10, 0.18, detail, 10, "muted", align=PP_ALIGN.CENTER)
