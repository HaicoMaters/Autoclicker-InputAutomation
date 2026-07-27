from pathlib import Path
import json
from typing import Any

CONFIG_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "toggle_key": "f6",
    "click_interval": 400,
    "always_on_top": False,
    "dark_mode": True,
}


def load_settings() -> dict[str, Any]:
    """
    Load application settings from the JSON file.

    If the settings file does not exist, it is recreated from the default
    values. Any missing keys are filled in from the defaults.

    Returns:
        dict[str, Any]: A dictionary containing the current settings.
    """
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
    else:
        reset_settings()

    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict[str, Any]) -> dict:
    """
    Save settings to the JSON file.

    The provided values are merged with the defaults so any omitted keys are
    preserved.

    Args:
        settings: Settings values to save.

    Returns:
        dict: The full settings dictionary that was written to disk.
    """
    merged = DEFAULT_SETTINGS.copy()
    merged.update(settings)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4)
    return merged


def update_settings(**changes: Any) -> dict[str, Any]:
    """
    Update one or more settings values and persist them.

    Keyword Args:
        **changes: Setting names and their new values.

    Returns:
        dict: The updated settings dictionary written to disk.
    """
    current_settings = load_settings()
    current_settings.update(changes)
    return save_settings(current_settings)


def reset_settings() -> None:
    """
    Reset settings to the default values.

    The default settings are written back to the JSON file immediately.
    """
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_SETTINGS, f, indent=4)