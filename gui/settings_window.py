from typing import Any

from pynput import keyboard
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QPushButton, QSpinBox, QVBoxLayout, QWidget

import clicker
import config


class SettingsWindow(QWidget):
    """
    Settings dialog for editing clicker preferences.
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
        self.auto_minimize_box: QCheckBox | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        """
        Create the settings form and bind its actions.
        """
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(300, 400)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 6, 16, 12)
        layout.setSpacing(8)

        settings: dict[str, Any] = config.load_settings()

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 30px; font-weight: 800;")
        layout.addWidget(title)

        # ------------------------------------------------ toggle key -----------------------------------------------
        self.selected_toggle_key_name = str(settings.get("toggle_key", "f6"))

        toggle_key_label = QLabel("Toggle hotkey")
        toggle_key_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        layout.addWidget(toggle_key_label)

        self.toggle_key_button = QPushButton(self.selected_toggle_key_name)
        self.toggle_key_button.clicked.connect(self._capture_toggle_key)
        self.toggle_key_button.setStyleSheet("font-size: 18px; font-weight: 800;")
        self.toggle_key_button.setMinimumHeight(38)
        layout.addWidget(self.toggle_key_button)

        # ---------------------------------------------- click interval --------------------------------------------------------
        interval_group = QWidget(self)
        interval_group_layout = QVBoxLayout(interval_group)
        interval_group_layout.setContentsMargins(0, 0, 0, 0)
        interval_group_layout.setSpacing(8)
        interval_group_label = QLabel("Time between click")
        interval_group_label.setStyleSheet("font-size: 14px; font-weight: 600")
        interval_group_layout.addWidget(interval_group_label)

        interval_group_layout.addLayout(self._build_interval_row("Minutes", settings.get("click_interval_mins", 0), 0, 99999999))
        interval_group_layout.addLayout(self._build_interval_row("Seconds", settings.get("click_interval_secs", 0), 0, 59))
        interval_group_layout.addLayout(self._build_interval_row("Milliseconds", settings.get("click_interval_ms", 400), 0, 999))
        layout.addWidget(interval_group)

        # ---------------------------------------------- checkboxes -------------------------------------------------------------
        self.always_on_top_box = QCheckBox("Always on top")
        self.always_on_top_box.setChecked(bool(settings.get("always_on_top", False)))
        layout.addWidget(self.always_on_top_box)

        self.dark_mode_box = QCheckBox("Dark mode")
        self.dark_mode_box.setChecked(bool(settings.get("dark_mode", True)))
        layout.addWidget(self.dark_mode_box)

        self.auto_minimize_box = QCheckBox("Minimize main window on autoclick start")
        self.auto_minimize_box.setChecked(bool(settings.get("auto_minimize", True)))
        layout.addWidget(self.auto_minimize_box)

        # ------------------------------------------------- buttons ---------------------------------------------
        button_row = QHBoxLayout()
        button_row.setSpacing(8)
        save_button = QPushButton("Save")
        reset_button = QPushButton("Reset")
        save_button.clicked.connect(self._save_changes)
        reset_button.clicked.connect(self._reset_changes)
        save_button.setMinimumHeight(36)
        reset_button.setMinimumHeight(36)
        button_row.addWidget(save_button, 1)
        button_row.addWidget(reset_button, 1)
        layout.addLayout(button_row)

        self.setWindowTitle("AutoClicker Settings")
        self.setWindowModality(Qt.NonModal)

    def _build_interval_row(self, label_text: str, value: int, minimum: int, maximum: int) -> QHBoxLayout:
        """
        Create a labeled interval field row.
        """
        row = QHBoxLayout()
        row.setSpacing(5)

        label = QLabel(label_text)
        label.setMinimumWidth(40)
        row.addWidget(label)

        spinbox = QSpinBox()
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(int(value))
        spinbox.setMinimumWidth(40)
        row.addWidget(spinbox, 1)

        if label_text == "Minutes":
            self.interval_field_mins = spinbox
        elif label_text == "Seconds":
            self.interval_field_secs = spinbox
        else:
            self.interval_field_ms = spinbox

        return row

    def _update_toggle_key_button(self) -> None:
        """
        Refresh the visible label shown for the selected toggle key.
        """
        if self.toggle_key_button is not None:
            self.toggle_key_button.setText(self.selected_toggle_key_name)

    def _capture_toggle_key(self) -> None:
        """
        Wait for the user to press a key and use it as the toggle hotkey.
        """
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

    def _save_changes(self) -> None:
        """
        Persist the edited settings and close the settings window.
        """
        if self.interval_field_ms is None or self.interval_field_mins is None or self.interval_field_secs is None:
            return

        settings: dict[str, Any] = config.load_settings()

        interval_value_ms = self.interval_field_ms.value()
        interval_value_secs = self.interval_field_secs.value()
        interval_value_mins = self.interval_field_mins.value()

        config.update_settings(
            toggle_key=self.selected_toggle_key_name,
            click_interval_ms=interval_value_ms,
            click_interval_secs=interval_value_secs,
            click_interval_mins=interval_value_mins,
            always_on_top=self.always_on_top_box.isChecked() if self.always_on_top_box is not None else False,
            dark_mode=self.dark_mode_box.isChecked() if self.dark_mode_box is not None else True,
            auto_minimize = self.auto_minimize_box.isChecked() if self.auto_minimize_box is not None else True,
        )
        clicker.set_toggle_key(config.deserialise_key(self.selected_toggle_key_name))
        self.close()

    def _reset_changes(self) -> None:
        """
        Restore the default settings and refresh the form controls.
        """
        config.reset_settings()
        settings: dict[str, Any] = config.load_settings()

        self.selected_toggle_key_name = settings.get("toggle_key", "f6")
        clicker.set_toggle_key(config.deserialise_key(self.selected_toggle_key_name))
        self._update_toggle_key_button()

        if self.interval_field_ms is not None:
            self.interval_field_ms.setValue(settings.get("click_interval_ms", 400))
        if self.interval_field_secs is not None:
            self.interval_field_secs.setValue(settings.get("click_interval_secs", 0))
        if self.interval_field_mins is not None:
            self.interval_field_mins.setValue(settings.get("click_interval_mins", 0))
        if self.always_on_top_box is not None:
            self.always_on_top_box.setChecked(False)
        if self.dark_mode_box is not None:
            self.dark_mode_box.setChecked(True)


def build_settings_window(parent: QWidget | None = None) -> SettingsWindow:
    """
    Build and return the settings window for editing clicker preferences.
    """
    return SettingsWindow(parent)

