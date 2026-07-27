from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QVBoxLayout
)

import clicker
import config
from gui.settings_window import build_settings_window


def build_main_window() -> QWidget:
    """Build and return the main application window.

    Returns:
        QWidget: The main application window widget.
    """
    window: QWidget = QWidget()
    layout = QVBoxLayout(window)

    settings: dict[str, Any] = config.load_settings()

    # ----------------------------------------- Interval Field -----------------------------------------

    interval_field: QLineEdit = QLineEdit()
    interval_field.setPlaceholderText("Click interval (ms)")
    interval_field.setText(str(settings.get("click_interval", 400)))

    # ----------------------------------------- Start Button -----------------------------------------
    toggle_key = settings.get("toggle_key")
    start_button: QPushButton = QPushButton(f"Start ({toggle_key})")

    def on_start_clicked():
        """Apply the current interval value to the clicker and save it.

        Returns:
            None: This function does not return a value.
        """
        try:
            interval_value = int(interval_field.text())
        except ValueError:
            interval_value = 400

        clicker.set_click_interval(interval_value)
        config.update_settings(click_interval=interval_value)

    start_button.clicked.connect(on_start_clicked)

    # ----------------------------------------- Settings Button -----------------------------------------
    settings_button: QPushButton = QPushButton("Settings")
    settings_window: QWidget | None = None

    def toggle_settings_window() -> None:
        """Show or hide the settings window for the main window.

        Returns:
            None: This function does not return a value.
        """
        nonlocal settings_window
        if settings_window is None:
            settings_window = build_settings_window(window)
            settings_window.setAttribute(Qt.WA_ShowWithoutActivating, False)
            settings_window.show()
        elif settings_window.isVisible():
            settings_window.hide()
        else:
            settings_window.show()

    settings_button.clicked.connect(toggle_settings_window)

    # ----------------------------------------- Build Layout -----------------------------------------------
    layout.addWidget(interval_field)
    layout.addWidget(start_button)
    layout.addWidget(settings_button)
    window.setWindowTitle("AutoClicker")
    return window