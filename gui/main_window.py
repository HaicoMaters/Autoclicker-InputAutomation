from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QSpinBox, QVBoxLayout, QWidget, QCheckBox, QGroupBox, QComboBox, QRadioButton, QButtonGroup
from PySide6.QtWidgets import QAbstractSpinBox
from pynput import keyboard, mouse
import clicker
import config
from gui.settings_window import SettingsWindow, build_settings_window
from screen.mouse_recorder import MouseRecorder
import time
from screen.monitor import Monitor, get_loaded_mointors, load_monitors
from gui.recording_overlay import RecordingOverlay


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
        
        self.random_offset_checkbox: QCheckBox | None = None
        self.random_offset_field: QSpinBox | None = None

        self.follow_mouse_radio: QRadioButton | None = None
        self.fixed_location_radio: QRadioButton | None = None
        self.monitor_select_combo: QComboBox | None = None
        self.fixed_location_button: QPushButton | None = None
        self.fixed_location_x_spinbox: QSpinBox | None = None
        self.fixed_location_y_spinbox: QSpinBox | None = None

        self.mouse_button_combo: QComboBox | None = None
        self.click_type_combo: QComboBox | None = None

        self.start_button: QPushButton | None = None
        self.stop_button: QPushButton | None = None

        self.key_listener = None
        self._listen_for_keys()
        self.mouse_recorder = MouseRecorder()
        self.monitors: list[Monitor] = load_monitors()

        self._build_ui()

    def _listen_for_keys(self) -> keyboard.Listener:
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
        layout.setContentsMargins(16, 6, 16, 12)
        layout.setSpacing(8)
        self.setCentralWidget(container)

        settings: dict[str, Any] = config.load_settings()

        title = QLabel("Autoclicker")
        title.setStyleSheet("font-size: 18px; font-weight: 800")
        layout.addWidget(title)

        # interval 
        interval_group = QGroupBox()
        interval_group.setContentsMargins(1,1,1,1)
        interval_group_layout = QVBoxLayout(interval_group)
        interval_group_layout.setSpacing(8)

        interval_group_label = QLabel("Time between click")
        interval_group_label.setStyleSheet("font-size: 12px; font-weight: 400")
        interval_group_layout.addWidget(interval_group_label)

        interval_row = self._build_interval_row("Minutes", settings.get("click_interval_mins", 0), 0, 99999999) # minutes
        interval_group_layout.addLayout(interval_row)

        interval_row = self._build_interval_row("Seconds", settings.get("click_interval_secs", 0), 0, 59) # seconds
        interval_group_layout.addLayout(interval_row)

        interval_row = self._build_interval_row("Milliseconds", settings.get("click_interval_ms", 400), 0, 999) # miliseconds
        interval_group_layout.addLayout(interval_row)

        # random interval offset
        random_offset_row = QHBoxLayout()
        random_offset_row.setSpacing(5)
        
        self.random_offset_checkbox = QCheckBox("Enable ± offset?")
        self.random_offset_checkbox.setToolTip("Your current interval + or - a random number from 0 to your offset")
        self.random_offset_checkbox.checkStateChanged.connect(self._on_offset_checkbox)
        random_offset_row.addWidget(self.random_offset_checkbox)

        random_offset_label = QLabel("Random offset (ms)")
        random_offset_label.setFixedWidth(110)
        random_offset_row.addWidget(random_offset_label)

        self.random_offset_field = QSpinBox()
        self.random_offset_field.setRange(0, 99999999)
        self.random_offset_field.setValue(50)
        self.random_offset_field.setMinimumWidth(60)
        self.random_offset_field.valueChanged.connect(self._on_offset_update)
        random_offset_row.addWidget(self.random_offset_field)
        
        interval_group_layout.addLayout(random_offset_row)

        layout.addWidget(interval_group)

        # type an location row
        click_type_location_row = QHBoxLayout()

        # click type and mouse button
        click_type_box = QGroupBox()
        click_type_box.setContentsMargins(1,1,1,1)
        click_type_box_layout = QVBoxLayout(click_type_box)
        click_type_box_layout.setSpacing(8)

        mouse_button_row = QHBoxLayout()
        mouse_button_row.setSpacing(5)

        mouse_button_label = QLabel("Mouse button:")
        mouse_button_label.setFixedWidth(75)
        mouse_button_row.addWidget(mouse_button_label)

        self.mouse_button_combo = QComboBox()
        self.mouse_button_combo.addItems(["Left", "Right", "Middle"])
        mouse_button_row.addWidget(self.mouse_button_combo)
        click_type_box_layout.addLayout(mouse_button_row)

        click_type_row = QHBoxLayout()
        click_type_row.setSpacing(5)

        click_type_label = QLabel("Click type:")
        click_type_label.setFixedWidth(75)
        click_type_row.addWidget(click_type_label)

        self.click_type_combo = QComboBox()
        self.click_type_combo.addItems(["Single", "Double"])
        click_type_row.addWidget(self.click_type_combo)
        click_type_box_layout.addLayout(click_type_row)

        click_type_location_row.addWidget(click_type_box)

        # mouse click location
        mouse_click_location_box = QGroupBox()
        mouse_click_location_box.setContentsMargins(1, 1, 1, 1)
        mouse_click_location_layout = QVBoxLayout(mouse_click_location_box)
        mouse_click_location_layout.setSpacing(8)

        mouse_click_location_btn_group = QButtonGroup()
        
        self.follow_mouse_radio = QRadioButton("Follow Mouse")
        self.follow_mouse_radio.setChecked(True)
        mouse_click_location_btn_group.addButton(self.follow_mouse_radio)

        fixed_location_row = QHBoxLayout()
        fixed_location_row.setSpacing(5)

        self.fixed_location_radio = QRadioButton("Fixed Location")
        mouse_click_location_btn_group.addButton(self.fixed_location_radio)
        fixed_location_row.addWidget(self.fixed_location_radio)

        self.monitor_select_combo = self._build_monitor_select_combo()
        self.monitor_select_combo.currentTextChanged.connect(self._on_combo_monitor_changed)
        fixed_location_row.addWidget(self.monitor_select_combo)
        
        fixed_location_row2 = QHBoxLayout()
        fixed_location_row2.setSpacing(5)

        self.fixed_location_button = QPushButton("Change Location")
        self.fixed_location_button.clicked.connect(self._on_fixed_location_button_clicked)
        self.fixed_location_button.setMinimumHeight(25)
        fixed_location_row2.addWidget(self.fixed_location_button)

        monitor_id = self.monitor_select_combo.currentData()
        selected_monitor = next(monitor for monitor in self.monitors if monitor.id == monitor_id)

        fixed_x_label = QLabel("x:")
        fixed_x_label.setFixedWidth(10)
        fixed_location_row2.addWidget(fixed_x_label)
        
        self.fixed_location_x_spinbox = QSpinBox()
        self.fixed_location_x_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.fixed_location_x_spinbox.setMinimumWidth(60)
        self.fixed_location_x_spinbox.setRange(0, selected_monitor.scaled_width)
        fixed_location_row2.addWidget(self.fixed_location_x_spinbox)

        fixed_y_label = QLabel("y:")
        fixed_y_label.setFixedWidth(10)
        fixed_location_row2.addWidget(fixed_y_label)

        self.fixed_location_y_spinbox = QSpinBox()
        self.fixed_location_y_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.fixed_location_y_spinbox.setMinimumWidth(60)
        self.fixed_location_y_spinbox.setRange(0, selected_monitor.scaled_height)
        fixed_location_row2.addWidget(self.fixed_location_y_spinbox)

        mouse_click_location_layout.addWidget(self.follow_mouse_radio)
        mouse_click_location_layout.addLayout(fixed_location_row)
        mouse_click_location_layout.addLayout(fixed_location_row2)

        click_type_location_row.addWidget(mouse_click_location_box)

        layout.addLayout(click_type_location_row)

        # add other options here

        layout.addStretch() # add stretch just before the buttons

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
        row.setSpacing(5)

        label = QLabel(label_text)
        label.setFixedWidth(90)
        row.addWidget(label)

        spinbox = QSpinBox()
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(int(value))
        spinbox.setMinimumWidth(60)
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

    def _build_monitor_select_combo(self) -> QComboBox:
        """
        Builds the combo box for selecting monitor.

        Returns:
            combo: The combo box object.
        """
        combo = QComboBox()

        for monitor in self.monitors:
            combo.addItem(f"{monitor.name} ({monitor.scaled_width}x{monitor.scaled_height})", monitor.id)

        return combo

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

    def _on_offset_update(self) -> None:
        """
        Update random offset when changed and random offset is enabled
        """
        if self.random_offset_field is None or not self.random_offset_checkbox.isChecked():
            return
        
        offset = self.random_offset_field.value()
        clicker.set_random_offset(offset)

    def _on_offset_checkbox(self) -> None:
        """
        When offset is checked change offset in clicker to offset spinbox value
        When offset is unchecked change offset in clicker to 0
        """
        if self.random_offset_checkbox is None or self.random_offset_field is None:
            return

        if (self.random_offset_checkbox.isChecked()):
            clicker.set_random_offset(self.random_offset_field.value())
        else:
            clicker.set_random_offset(0)

    def _on_combo_monitor_changed(self) -> None:
        """
        Updates the ranges for the spinboxes based on the sizes of the monitors
        """
        monitor_id = self.monitor_select_combo.currentData()

        selected_monitor = next(monitor for monitor in self.monitors if monitor.id == monitor_id)

        self.fixed_location_x_spinbox.setRange(0, selected_monitor.scaled_width)
        self.fixed_location_y_spinbox.setRange(0, selected_monitor.scaled_height)


    def _on_fixed_location_button_clicked(self) -> None:
        # show recording overlay and get input from the overlay
       self.recording_overlay = RecordingOverlay(self.mouse_recorder)
       self.recording_overlay.location_selected.connect(self._on_location_selected)
       self.recording_overlay.showFullScreen()
       self.recording_overlay.start_recording()


    def _on_location_selected(self, x: int, y: int) -> None:
        self.fixed_location_x_spinbox.setValue(x)
        self.fixed_location_y_spinbox.setValue(y)

    def _on_follow_mouse_radio(self) -> None:
        """
        Updates the clicker to remove target 
        """
        clicker.clear_click_target()

    def _on_fixed_location_radio(self) -> None:
        """
        Updates the clicker to have settings set to fixed location
        """
        clicker.set_click_target(self.fixed_location_x_spinbox.Value(), self.fixed_location_y_spinbox().Value)

    def _on_start_clicked(self) -> None:
        """
        Start the clicker enable stop button, disable stop button and minimize window if current setting update the clicktype settings.
        """
        # handle follow mouse
        if self.follow_mouse_radio.isChecked():
            clicker.clear_click_target()
        elif self.fixed_location_radio.isChecked():
            clicker.set_click_target((self.fixed_location_x_spinbox.value(), self.fixed_location_y_spinbox.value()))

        clicker.set_clicking(True)
        self._update_click_type()
        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)

        if config.load_settings().get("auto_minimize") == True:
            self.showMinimized()
    
    def _on_stop_clicked(self) -> None:
        """
        Stop the clicker enable start button, disable stop button.
        """
        clicker.set_clicking(False)
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        # maybe bring window back up if pressing hotkey when minimized

    def _update_click_type(self) -> None:
        mouse_button = mouse.Button.left

        match (self.mouse_button_combo.currentText()):
            case "Right":
                mouse_button = mouse.Button.right
            case "Middle":
                mouse_button = mouse.Button.middle
            case _:
                mouse_button = mouse.Button.left

        click_count = 1

        if (self.click_type_combo.currentText() == "Double"):
            click_count = 2

        clicker.set_number_of_clicks(click_count)
        clicker.set_mouse_button(mouse_button)

    def _toggle_settings_window(self) -> None:
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

