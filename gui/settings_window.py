from typing import Any

from pynput import keyboard
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import clicker
import config

def build_settings_window(parent: QWidget | None = None) -> QWidget:
    """
    Build and return the settings window for editing clicker preferences.

    Args:
        parent: The parent widget for the settings window.

    Returns:
        QWidget: The settings window widget.
    """
    window: QWidget = QWidget(parent, Qt.Window)
    window.setWindowTitle("Settings")
    window.setWindowModality(Qt.NonModal)
    layout = QVBoxLayout(window)

    settings: dict[str, Any] = config.load_settings()

    # ----------------------------------------- Toggle Key -------------------------------------
    toggle_key_label = QLabel("Toggle key")
    selected_toggle_key_name = settings.get("toggle_key")
    toggle_key_button: QPushButton = QPushButton(str(selected_toggle_key_name))
    capture_listener = None

    def update_toggle_key_button():
        """
        Refresh the visible label shown for the selected toggle key.
        """
        toggle_key_button.setText(str(selected_toggle_key_name))

    def capture_toggle_key():
        """
        Wait for the user to press a key and use it as the toggle hotkey.
        """
        nonlocal capture_listener
        nonlocal selected_toggle_key_name
        if capture_listener is not None:
            return

        toggle_key_button.setText("Press any key...")

        def on_key_press(key: Any) -> bool:
            nonlocal capture_listener
            nonlocal selected_toggle_key_name
            selected_toggle_key_name = config.serialise_key(key)
            clicker.set_toggle_key(config.deserialise_key(selected_toggle_key_name))
            update_toggle_key_button()
            if capture_listener is not None:
                capture_listener.stop()
            capture_listener = None
            return False

        capture_listener = keyboard.Listener(on_press=on_key_press)
        capture_listener.start()

    # ----------------------------------------- Interval Field ----------------------------------
    interval_label = QLabel("Default Click interval (ms)")
    interval_field: QLineEdit = QLineEdit(str(settings.get("click_interval", 400)))

    # ----------------------------------------- Always On Top -----------------------------------
    always_on_top_box: QCheckBox = QCheckBox("Always on top")
    always_on_top_box.setChecked(bool(settings.get("always_on_top", False)))

    # ----------------------------------------- Dark Mode ---------------------------------------
    dark_mode_box: QCheckBox = QCheckBox("Dark mode")
    dark_mode_box.setChecked(bool(settings.get("dark_mode", True)))

    # ----------------------------------------- Buttons -----------------------------------------
    button_row = QHBoxLayout()
    save_button: QPushButton = QPushButton("Save")
    reset_button: QPushButton = QPushButton("Reset")

    def save_changes():
        """
        Persist the edited settings and close the settings window.
        """
        try:
            interval_value = int(interval_field.text())
        except ValueError:
            interval_value = settings.get("click_interval", 400)

        config.update_settings(
            toggle_key=selected_toggle_key_name,
            click_interval=interval_value,
            always_on_top=always_on_top_box.isChecked(),
            dark_mode=dark_mode_box.isChecked(),
        )
        clicker.set_toggle_key(config.deserialise_key(selected_toggle_key_name))
        window.close()

    def reset_changes():
        """
        Restore the default settings and refresh the form controls.
        """
        nonlocal selected_toggle_key_name
        config.reset_settings()
        selected_toggle_key_name = "f6"
        clicker.set_toggle_key(config.deserialise_key(selected_toggle_key_name))
        update_toggle_key_button()
        interval_field.setText("400")
        always_on_top_box.setChecked(False)
        dark_mode_box.setChecked(True)

    save_button.clicked.connect(save_changes)
    reset_button.clicked.connect(reset_changes)
    toggle_key_button.clicked.connect(capture_toggle_key)

    button_row.addWidget(save_button)
    button_row.addWidget(reset_button)

    # ----------------------------------------- Build Layout -----------------------------------------
    layout.addWidget(toggle_key_label)
    layout.addWidget(toggle_key_button)
    layout.addWidget(interval_label)
    layout.addWidget(interval_field)
    layout.addWidget(always_on_top_box)
    layout.addWidget(dark_mode_box)
    layout.addLayout(button_row)
    window.setWindowTitle("AutoClicker Settings")

    return window
