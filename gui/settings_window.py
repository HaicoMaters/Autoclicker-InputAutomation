from typing import Any

from pynput import keyboard
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QSpinBox, QPushButton, QVBoxLayout, QWidget

import clicker
import config


class SettingsWindow(QWidget):
    """
    Settings dialog for editing clicker preferences
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.Window)
        self.capture_listener: keyboard.Listener | None = None
        self.selected_toggle_key_name: str = "f6"
        self.toggle_key_button: QPushButton | None = None
        self.interval_field_mins: QSpinBox | None = None
        self.interval_field_secs: QSpinBox | None = None
        self.interval_field_ms: QSpinBox | None = None
        self.always_on_top_box: QCheckBox | None = None
        self.dark_mode_box: QCheckBox | None = None
        self._build_ui()

    def _build_ui(self):
        """Create the settings form and bind its actions."""
        layout = QVBoxLayout(self)
        settings: dict[str, Any] = config.load_settings()
        self.selected_toggle_key_name = str(settings.get("toggle_key", "f6"))

        # toggle key
        toggle_key_label = QLabel("Toggle key")
        self.toggle_key_button = QPushButton(self.selected_toggle_key_name)
        self.toggle_key_button.clicked.connect(self._capture_toggle_key)

        # interval fields
        self.interval_field_mins = QSpinBox()
        self.interval_field_mins.setRange(0, 99999999) # randomly chose number that should be excessive (around 190 years)
        self.interval_field_mins.setValue(int(settings.get("click_interval_mins", 0)))

        self.interval_field_secs = QSpinBox()
        self.interval_field_secs.setRange(0, 59)
        self.interval_field_secs.setValue(int(settings.get("click_interval_secs", 0)))

        self.interval_field_ms = QSpinBox()
        self.interval_field_ms.setRange(0, 999)
        self.interval_field_ms.setValue(int(settings.get("click_interval_ms", 400)))

        # checkboxes
        self.always_on_top_box = QCheckBox("Always on top")
        self.always_on_top_box.setChecked(bool(settings.get("always_on_top", False)))

        self.dark_mode_box = QCheckBox("Dark mode")
        self.dark_mode_box.setChecked(bool(settings.get("dark_mode", True)))

        button_row = QHBoxLayout()
        save_button = QPushButton("Save")
        reset_button = QPushButton("Reset")
        save_button.clicked.connect(self._save_changes)
        reset_button.clicked.connect(self._reset_changes)

        button_row.addWidget(save_button)
        button_row.addWidget(reset_button)

        layout.addWidget(toggle_key_label)
        layout.addWidget(self.toggle_key_button)
        layout.addWidget(self.interval_field_mins)
        layout.addWidget(self.interval_field_secs)
        layout.addWidget(self.interval_field_ms)
        layout.addWidget(self.always_on_top_box)
        layout.addWidget(self.dark_mode_box)
        layout.addLayout(button_row)

        self.setWindowTitle("AutoClicker Settings")
        self.setWindowModality(Qt.NonModal)

    def _update_toggle_key_button(self):
        """Refresh the visible label shown for the selected toggle key."""
        if self.toggle_key_button is not None:
            self.toggle_key_button.setText(self.selected_toggle_key_name)

    def _capture_toggle_key(self):
        """Wait for the user to press a key and use it as the toggle hotkey."""
        if self.capture_listener is not None:
            return

        if self.toggle_key_button is not None:
            self.toggle_key_button.setText("Press any key...")

        def on_key_press(key: Any) -> bool:
            self.selected_toggle_key_name = config.serialise_key(key)
            clicker.set_toggle_key(config.deserialise_key(self.selected_toggle_key_name))
            self._update_toggle_key_button()
            if self.capture_listener is not None:
                self.capture_listener.stop()
            self.capture_listener = None
            return False

        self.capture_listener = keyboard.Listener(on_press=on_key_press)
        self.capture_listener.start()

    def _save_changes(self):
        """
          the edited settings and close the settings window
        """
        if self.interval_field_ms is None or self.interval_field_mins is None or self.interval_field_secs is None or self.always_on_top_box is None or self.dark_mode_box is None:
            return

        settings : dict[str, Any] = config.load_settings()

        # intervals 
        try:
            interval_value_ms = int(self.interval_field_ms.value())
        except ValueError:
            interval_value_ms = settings.get("click_interval_ms", 400)

        try:
             interval_value_secs = int(self.interval_field_secs.value())
        except ValueError:
            interval_value_secs  = settings.get("click_interval_secs", 0)

        try:
            interval_value_mins = int(self.interval_field_mins.value())
        except ValueError:
                interval_value_mins = settings.get("click_interval_mins", 0)
        

        # update
        config.update_settings(
            toggle_key=self.selected_toggle_key_name,
            click_interval_ms=interval_value_ms,
            click_interval_secs=interval_value_secs,
            click_interval_mins=interval_value_mins,
            always_on_top=self.always_on_top_box.isChecked(),
            dark_mode=self.dark_mode_box.isChecked(),
        )
        clicker.set_toggle_key(config.deserialise_key(self.selected_toggle_key_name))
        self.close()

    def _reset_changes(self):
        """
        Restore the default settings and refresh the form controls
        """
        config.reset_settings()
        settings : dict[str, Any] = config.load_settings()

        # hotkey
        self.selected_toggle_key_name = settings.get("toggle_key", "f6")
        clicker.set_toggle_key(config.deserialise_key(self.selected_toggle_key_name))
        self._update_toggle_key_button()

        # intervals
        if self.interval_field_ms is not None:
            self.interval_field_ms.setValue(settings.get("click_interval_ms", 400))
            
        if self.interval_field_secs is not None:
            self.interval_field_secs.setValue(settings.get("click_interval_secs", 400))
            
        if self.interval_field_mins is not None:
            self.interval_field_mins.setValue(settings.get("click_interval_mins", 400))

        # checkboxes
        if self.always_on_top_box is not None:
            self.always_on_top_box.setChecked(False)
        if self.dark_mode_box is not None:
            self.dark_mode_box.setChecked(True)


def build_settings_window(parent: QWidget | None = None) -> SettingsWindow:
    """
    Build and return the settings window for editing clicker preferences
    """
    return SettingsWindow(parent)

