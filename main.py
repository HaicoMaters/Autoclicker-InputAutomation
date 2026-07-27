import sys
from PySide6.QtWidgets import QApplication
import clicker
import config
from gui.main_window import build_main_window


def main():
    """
    Start the clicker services and launch the application window.
    """
    settings = config.load_settings()
    clicker.set_click_interval(settings.get("click_interval", 400))
    clicker.set_toggle_key(config.deserialise_key(settings.get("toggle_key", "f6")))
    clicker.start_clicker_services()

    app = QApplication(sys.argv)
    window = build_main_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())    

