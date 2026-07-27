from pathlib import Path
import json

CONFIG_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "toggle_key": "f6",
    "click_interval": 400,
    "always_on_top": False,
    "dark_mode": True,
}


def load_settings():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    merged = DEFAULT_SETTINGS.copy()
                    merged.update(data)
                    return merged
        except (json.JSONDecodeError, OSError):
            pass

    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def reset_settings():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_SETTINGS, f, indent=4)