from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QSpinBox, QVBoxLayout, QWidget
from pynput import keyboard
import clicker
import config
from gui.settings_window import SettingsWindow, build_settings_window


class MainWindow(QMainWindow):
    """
    Main application window for controlling the clicker.
    """

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.settings_window: SettingsWindow | None = None
        self.interval_field_ms: QSpinBox | None = None
        self.interval_field_secs: QSpinBox | None = None
        self.interval_field_mins: QSpinBox | None = None
        self.start_button: QPushButton | None = None
        self.stop_button: QPushButton | None = None
        self.key_listener = None
        self._listen_for_keys()
        self._build_ui()

    def _listen_for_keys(self):
        """
        Start the keyboard listener if it is not already running.

        Returns:
            key_listener: The active keyboard listener instance.
        """
        if self.key_listener is not None:
            return self.key_listener

        self.key_listener = keyboard.Listener(on_press=self._on_key_press)
        self.key_listener.start()
        return self.key_listener

    def _on_key_press(self, Key: Any):
        """
        Toggle the click loop when the hotkey is press simulate start/stop behaviour depending.
        
         Args:
            key: The keyboard key that triggered the event.
        """
        try:
            if Key == clicker.get_toggle_key(): # get toggle key in unserialised form
                if clicker.is_clicking():
                    self._on_stop_clicked()
                else:
                    self._on_start_clicked() # clicker runs without minimizing window
        except Exception:
            pass
                

    def _build_ui(self) -> None:
        """
        Create the main window widgets.
        """
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        self.setCentralWidget(container)

        settings: dict[str, Any] = config.load_settings()

        title = QLabel("Auto Clicker")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        # interval 
        interval_group = QWidget(self)
        interval_group_layout = QVBoxLayout(interval_group)
        interval_group_layout.setContentsMargins(0, 0, 0, 0)
        interval_group_layout.setSpacing(8)

        interval_row = self._build_interval_row("Minutes", settings.get("click_interval_mins", 0), 0, 99999999)
        interval_group_layout.addLayout(interval_row)

        interval_row = self._build_interval_row("Seconds", settings.get("click_interval_secs", 0), 0, 59)
        interval_group_layout.addLayout(interval_row)

        interval_row = self._build_interval_row("Milliseconds", settings.get("click_interval_ms", 400), 0, 999)
        interval_group_layout.addLayout(interval_row)

        layout.addWidget(interval_group)

        # buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(8)
        toggle_key = settings.get("toggle_key", "f6") # gets the toggle key in a serialised form
        self.start_button = QPushButton(f"Start ({toggle_key})")
        self.start_button.clicked.connect(self._on_start_clicked)
        self.start_button.setMinimumHeight(40)

        self.stop_button = QPushButton(f"Stop ({toggle_key})")
        self.stop_button.clicked.connect(self._on_stop_clicked)
        self.stop_button.setMinimumHeight(40)
        self.stop_button.setEnabled(False)

        button_row.addWidget(self.start_button, 1)
        button_row.addWidget(self.stop_button, 1)
        layout.addLayout(button_row)

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self._toggle_settings_window)
        settings_button.setMinimumHeight(38)
        layout.addWidget(settings_button)

        self.setWindowTitle("AutoClicker")
        self.resize(360, 220)

    def _build_interval_row(self, label_text: str, value: int, minimum: int, maximum: int) -> QHBoxLayout:
        """
        Create a labeled interval field row.
        """
        row = QHBoxLayout()
        row.setSpacing(8)

        label = QLabel(label_text)
        label.setMinimumWidth(90)
        row.addWidget(label)

        spinbox = QSpinBox()
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(int(value))
        spinbox.setMinimumWidth(90)
        row.addWidget(spinbox, 1)

        if label_text == "Minutes":
            self.interval_field_mins = spinbox
            self.interval_field_mins.valueChanged.connect(self._on_interval_update)
        elif label_text == "Seconds":
            self.interval_field_secs = spinbox
            self.interval_field_secs.valueChanged.connect(self._on_interval_update)
        else:
            self.interval_field_ms = spinbox
            self.interval_field_ms.valueChanged.connect(self._on_interval_update)

        return row

    def _on_interval_update(self) -> None:
        """
        Update the click interval when changed.
        """
        if self.interval_field_mins is None or self.interval_field_secs is None or self.interval_field_ms is None:
            return

        mins = self.interval_field_mins.value()
        secs = self.interval_field_secs.value()
        ms = self.interval_field_ms.value()
        clicker.set_click_interval(ms, secs, mins)

    def _on_start_clicked(self):
        """
        Start the clicker enable stop button, disable stop button and minimize window if current setting.
        """
        clicker.set_clicking(True)
        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)

        if config.load_settings().get("auto_minimize") == True:
            self.showMinimized()

    def _on_stop_clicked(self):
        """
        Stop the clicker enable start button, disable stop button.
        """
        clicker.set_clicking(False)
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        # maybe bring window back up if pressing hotkey when minimized

    def _toggle_settings_window(self):
        """
        Show or hide the settings window for the main window.
        """
        if self.settings_window is None:
            self.settings_window = build_settings_window(self)
            self.settings_window.setAttribute(Qt.WA_ShowWithoutActivating, False)
            self.settings_window.show()
        elif self.settings_window.isVisible():
            self.settings_window.hide()
        else:
            self.settings_window.show()


def build_main_window(parent: QWidget | None = None) -> MainWindow:
    """Build and return the main application window."""
    return MainWindow(parent)

