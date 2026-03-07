"""League Table Manager - Entry point."""
from interface import build_interface
from theme import LeagueTheme, CSS

if __name__ == "__main__":
    demo = build_interface()
    demo.launch(theme=LeagueTheme(), css=CSS)
