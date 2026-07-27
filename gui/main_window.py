from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QVBoxLayout,
)

from typing import Any

import clicker
import config


def build_main_window() -> QWidget:
    window: QWidget = QWidget()
    layout = QVBoxLayout(window)

    settings: dict[str, Any] = config.load_settings()

    # ----------------------------------------- Interval Field -----------------------------------------

    interval_field: QLineEdit = QLineEdit()
    interval_field.setPlaceholderText("Click interval (ms)")
    interval_field.setText(str(settings.get("click_interval", 400)))

    # ----------------------------------------- Start Button -----------------------------------------
    toggle_key = settings.get("toggle_key", "f6")
    start_button: QPushButton = QPushButton(f"Start ({toggle_key})")

    def on_start_clicked():
        try:
            interval_value = int(interval_field.text())
        except ValueError:
            interval_value = 400

        clicker.set_click_interval(interval_value)
        config.update_settings(click_interval=interval_value)

    start_button.clicked.connect(on_start_clicked)

    # ----------------------------------------- Dark Mode Checkbox -----------------------------------------
    dark_mode_box: QCheckBox = QCheckBox("Dark Mode")
    dark_mode_box.setChecked(bool(settings.get("dark_mode", True)))

    def on_dark_mode_update():
        config.update_settings(dark_mode=dark_mode_box.isChecked())

    dark_mode_box.stateChanged.connect(on_dark_mode_update)

    # ----------------------------------------- Build Layout -----------------------------------------------
    layout.addWidget(interval_field)
    layout.addWidget(start_button)
    layout.addWidget(dark_mode_box)
    window.setWindowTitle("AutoClicker")
    return window