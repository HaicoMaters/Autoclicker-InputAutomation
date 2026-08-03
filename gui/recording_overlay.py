from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class RecordingOverlay(QWidget):
    """
    Fullscreen overlay used to record a single mouse click location.

    Uses MouseRecorder to listen for mouse input and emits the selected
    coordinates once a click has been recorded.
    """

    location_selected = Signal(int, int)

    def __init__(self, mouse_recorder):
        """
        Initialise the recording overlay.

        Args:
            mouse_recorder: MouseRecorder instance used to capture mouse input.
        """
        super().__init__()

        self.mouse_recorder = mouse_recorder

        self.setWindowFlags( Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel("Recording mouse location...\n\nClick the location for autoclicker")

        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                font-size: 24px;
                padding: 20px;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._check_location)

    def start_recording(self) -> None:
        """
        Start listening for a single mouse click.

        The MouseRecorder listener uses pynput internally. This function
        starts the listener and begins checking for the recorded location.
        """
        self.mouse_recorder.listen_for_mouse(self._record_single_click)

        self.timer.start(100)

    def _record_single_click(self, x: int, y: int, pressed: bool) -> None:
        """
        Records a single mouse click location.

        Args:
            x,y: coords of the mouse click.
            pressed: Whether the button was pressed or released.
        """
        if pressed:
            self.mouse_recorder.record_single_click_location(x, y)

    def _check_location(self) -> None:
        """
        Check whether the mouse listener has finished recording, capture location and emit coordinates and close overlay.
        """
        if not self.mouse_recorder.is_listening():
            x = self.mouse_recorder.single_x
            y = self.mouse_recorder.single_y

            self.timer.stop()

            self.location_selected.emit(x, y)

            self.close()