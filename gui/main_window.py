from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QVBoxLayout,
)

import clicker
import config


def build_main_window():
    window = QWidget()
    layout = QVBoxLayout(window)

    interval_field = QLineEdit()
    interval_field.setPlaceholderText("Click interval (ms)")
    interval_field.setText(str(config.load_settings().get("click_interval", 400)))

    toggle_checkbox = QCheckBox("Enable clicking")

    start_button = QPushButton("Start")

    def on_start_clicked():
        try:
            interval_value = int(interval_field.text())
        except ValueError:
            interval_value = 400

        clicker.set_click_interval(interval_value)
        clicker.set_clicking(toggle_checkbox.isChecked())
        config.save_settings({
            "toggle_key": config.load_settings().get("toggle_key", "f6"),
            "click_interval": interval_value,
            "always_on_top": False,
            "dark_mode": True,
        })

    start_button.clicked.connect(on_start_clicked)

    layout.addWidget(interval_field)
    layout.addWidget(toggle_checkbox)
    layout.addWidget(start_button)
    window.setWindowTitle("AutoClicker")
    return window