"""Gradio theme and global CSS for the League Table Manager."""
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes


class LeagueTheme(Base):
    def __init__(self):
        super().__init__(
            primary_hue=colors.green,
            secondary_hue=colors.emerald,
            neutral_hue=colors.slate,
            spacing_size=sizes.spacing_md,
            radius_size=sizes.radius_lg,
            text_size=sizes.text_md,
            font=(
                fonts.GoogleFont("Inter"),
                "ui-sans-serif",
                "system-ui",
                "sans-serif",
            ),
        )
        super().set(
            body_background_fill="#0f172a",
            body_background_fill_dark="#0f172a",
            block_background_fill="#1e293b",
            block_background_fill_dark="#1e293b",
            block_border_color="#334155",
            block_border_color_dark="#334155",
            block_border_width="1px",
            block_radius="12px",
            block_shadow="0 4px 24px rgba(0,0,0,0.4)",
            body_text_color="#e2e8f0",
            body_text_color_dark="#e2e8f0",
            block_label_text_color="#94a3b8",
            block_label_text_weight="600",
            input_background_fill="#0f172a",
            input_background_fill_dark="#0f172a",
            input_border_color="#334155",
            input_border_color_dark="#334155",
            input_border_color_focus="*primary_500",
            button_primary_background_fill="*primary_600",
            button_primary_background_fill_hover="*primary_500",
            button_primary_text_color="white",
            button_primary_border_color="transparent",
            button_secondary_background_fill="#334155",
            button_secondary_background_fill_hover="#475569",
            button_secondary_text_color="#e2e8f0",
            border_color_primary="*primary_600",
        )


CSS = """
/* Tab bar */
.tab-nav button {
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #94a3b8 !important;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}
.tab-nav button.selected {
    color: #22c55e !important;
    border-bottom: 2px solid #22c55e !important;
    background: transparent !important;
}

/* Dataframe table headers */
.gr-dataframe th, table th {
    background-color: #0f172a !important;
    color: #22c55e !important;
    font-weight: 700 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    padding: 10px 8px !important;
    border-bottom: 2px solid #22c55e !important;
}
.gr-dataframe td, table td {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    padding: 8px !important;
    border-bottom: 1px solid #334155 !important;
    font-size: 0.85rem;
}
.gr-dataframe tr:hover td, table tr:hover td {
    background-color: #263548 !important;
}

/* Buttons */
button.primary, .primary {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(22,163,74,0.3) !important;
    transition: all 0.2s !important;
}
button.primary:hover {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    box-shadow: 0 6px 16px rgba(34,197,94,0.4) !important;
    transform: translateY(-1px);
}
button.stop {
    background: #7f1d1d !important;
    color: #fca5a5 !important;
    border: 1px solid #dc2626 !important;
}

/* Accordion */
.gr-accordion {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

/* Input fields */
input[type="text"], input[type="number"], textarea {
    background-color: #0f172a !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
input:focus, textarea:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.1) !important;
}

/* App heading */
h1 {
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: white !important;
}
"""
