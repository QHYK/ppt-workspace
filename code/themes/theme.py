"""Design tokens. Content and page composition belong in each presentation."""

from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class Theme:
    width: float
    height: float
    colors: dict[str, str]
    font: str = "Noto Sans CJK SC"
    layout: dict[str, float] = field(default_factory=dict)
    type_scale: dict[str, float] = field(default_factory=dict)
    motif_palette: tuple[str, ...] = ()

    def color(self, key: str) -> str:
        """Resolve a semantic color key, accepting an explicit hex value too."""
        return self.colors.get(key, key)

    def override(
        self, *, colors=None, layout=None, type_scale=None, font=None,
        width=None, height=None, motif_palette=None,
    ) -> "Theme":
        """Create a project variant while retaining unspecified base tokens."""
        return replace(
            self,
            colors={**self.colors, **(colors or {})},
            layout={**self.layout, **(layout or {})},
            type_scale={**self.type_scale, **(type_scale or {})},
            font=self.font if font is None else font,
            width=self.width if width is None else width,
            height=self.height if height is None else height,
            motif_palette=self.motif_palette if motif_palette is None else motif_palette,
        )


# The established editorial palette and proportions are the shared starting point.
DEFAULT = Theme(
    width=13.333,
    height=7.5,
    colors={
        "background": "F5F5EF", "dark": "153D35", "green": "327B68",
        "muted": "61776D", "pale": "E1EBE1", "white": "FFFFFF",
        "ink": "172D28", "border": "D8E2D9", "soft": "EBF0E8",
        "sage": "87A89A", "gold": "B9A66F",
    },
    layout={
        "left": 0.55, "right": 0.55, "content_y": 2.05, "content_h": 4.76,
        "caption_y": 0.32, "title_y": 0.82, "subtitle_y": 1.52,
        "footer_line_y": 7.05, "card_gap": 0.20, "card_pad": 0.22,
        "icon_size": 0.38, "table_left": 0.56,
    },
    type_scale={
        "body": 18, "bullet": 15, "caption": 11, "title": 30, "subtitle": 14,
        "footer": 9, "card_title": 18, "card_body": 14,
        "table_header": 14, "table_body": 14.5, "table_dense": 13,
    },
    motif_palette=("A8C9B1", "77A994", "D8E6C9", "3D826E"),
)
