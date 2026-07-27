import sys
from PySide6.QtWidgets import QApplication

import clicker
import config
from gui.main_window import build_main_window


def main():
    settings = config.load_settings()
    clicker.set_click_interval(settings.get("click_interval", 400))
    clicker.start_clicker_services()

    app = QApplication(sys.argv)
    window = build_main_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())    