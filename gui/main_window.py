from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QSpinBox, QLabel, QHBoxLayout

import clicker
import config
from gui.settings_window import SettingsWindow, build_settings_window

"""Main application window for controlling the clicker."""
class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.interval_field_layout: QHBoxLayout | None = None
        self.settings_window: SettingsWindow | None = None
        self.interval_field_ms : QSpinBox | None = None
        self.interval_field_secs : QSpinBox | None = None
        self.interval_field_mins : QSpinBox | None = None
        self.interval_label_ms: QLabel = QLabel("Miliseconds")
        self.interval_label_secs: QLabel = QLabel("Seconds")
        self.interval_label_mins: QLabel = QLabel("Minutes")
        self.start_button: QPushButton | None = None
        self._build_ui()

    def _build_ui(self):
        """
        Create the main window widgets
        """
        container = QWidget(self)
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)

        settings: dict[str, Any] = config.load_settings()

        # Layouts
        self.interval_field_layout = QHBoxLayout()

        # interval fields (and labels)
        self.interval_field_mins = QSpinBox()
        self.interval_field_mins.setRange(0, 99999999) # randomly chose number that should be excessive (around 190 years)
        self.interval_field_mins.setValue(int(settings.get("click_interval_mins", 0)))
        self.interval_field_mins.valueChanged.connect(self._on_interval_update)

        self.interval_field_secs = QSpinBox()
        self.interval_field_secs.setRange(0, 59)
        self.interval_field_secs.setValue(int(settings.get("click_interval_secs", 0)))
        self.interval_field_secs.valueChanged.connect(self._on_interval_update)

        self.interval_field_ms = QSpinBox()
        self.interval_field_ms.setRange(0, 999)
        self.interval_field_ms.setValue(int(settings.get("click_interval_ms", 400)))
        self.interval_field_ms.valueChanged.connect(self._on_interval_update)

        # start button
        toggle_key = settings.get("toggle_key", "f6")
        self.start_button = QPushButton(f"Start ({toggle_key})")
        self.start_button.clicked.connect(self._on_start_clicked)

        # settings button
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self._toggle_settings_window)
        
        self.interval_field_layout.addWidget(self.interval_field_mins)
        self.interval_field_layout.addWidget(self.interval_field_secs)
        self.interval_field_layout.addWidget(self.interval_field_ms)
        layout.addWidget(self.start_button)
        layout.addWidget(settings_button)
        self.setWindowTitle("AutoClicker")

    def _on_interval_update(self):
        """
        Update the click interval when changed
        """
        if self.interval_field_mins or self.interval_field_secs or self.interval_field_ms is None:
            return

        mins = self.interval_field_mins.value()
        secs = self.interval_field_secs.value()
        ms = self.interval_field_ms.value()

        clicker.set_click_interval(ms, secs, mins)

    def _on_start_clicked(self):
        """
        Start the clicker or stop the clicker
        """
        clicker.set_clicking(not clicker.is_clicking())

    def _on_clicker_start(self): # not implemented logic on either clicker side or here
        """
        Minimize the window and update the start button text when window is reopened (unless always on top)
        """
        if clicker.is_clicking():
            return
        return
            
    def _toggle_settings_window(self):
        """
        Show or hide the settings window for the main window
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

