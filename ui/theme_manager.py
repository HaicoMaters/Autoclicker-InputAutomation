from PySide6.QtWidgets import QApplication
from ui.styles import DARK_THEME, LIGHT_THEME

def apply_theme(theme : str):
    """
    Applies the relevant theme to the application

    Args:
        theme: a string containing the name of the theme to apply
    """
    app = QApplication.instance()
    
    if theme == "dark_mode":
        app.setStyleSheet(DARK_THEME)
    else:
        app.setStyleSheet(LIGHT_THEME)