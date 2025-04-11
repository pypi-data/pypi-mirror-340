from pathlib import Path
from instaui import ui

_STATIC_DIR = Path(__file__).parent / "static"
_DAISYUI_CSS = _STATIC_DIR / "daisyui.css"
_THEME_CSS = _STATIC_DIR / "themes.css"


def use_daisyui(value=True):
    if value:
        ui.add_css_link(_DAISYUI_CSS)
        ui.add_css_link(_THEME_CSS)
    else:
        ui.remove_css_link(_DAISYUI_CSS)
        ui.remove_css_link(_THEME_CSS)
