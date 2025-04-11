import plotly.io as pio

# Supported themes (can expand later)
_SUPPORTED_THEMES = {
    "plotly": "plotly",
    "plotly_dark": "plotly_dark",
    "ggplot2": "ggplot2",
    "seaborn": "seaborn",
    "simple_white": "simple_white",
    "presentation": "presentation",
}

# Internal state
_current_theme = "plotly"

def set_theme(name: str):
    global _current_theme
    if name not in _SUPPORTED_THEMES:
        raise ValueError(f"Theme '{name}' is not supported. Choose from: {list(_SUPPORTED_THEMES)}")
    pio.templates.default = _SUPPORTED_THEMES[name]
    _current_theme = name

def get_current_theme():
    global _current_theme
    return _current_theme
