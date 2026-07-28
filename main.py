import sys

from PySide6.QtWidgets import QApplication

import clicker
import config
from gui.main_window import build_main_window


def main() -> int:
    settings = config.load_settings()

    # Clicker setup
    clicker.set_click_interval(settings.get("click_interval_ms", 400), settings.get("click_interval_secs", 0), settings.get("click_interval_mins", 0))
    clicker.set_toggle_key(config.deserialise_key(settings.get("toggle_key", "f6")))
    clicker.start_clicker_services()

    # Gui
    app = QApplication(sys.argv)
    window = build_main_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

