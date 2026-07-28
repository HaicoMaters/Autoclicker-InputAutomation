from pathlib import Path
import json
from typing import Any
from pynput import keyboard

CONFIG_FILE = Path("settings.json")


def serialise_key(key: Any) -> str:
    """
    Convert a pynput key object or string into a serialisable string.

    Args:
        key: The key object or string to convert.

    Returns:
        str: A string value suitable for saving in settings.
    """
    if isinstance(key, keyboard.KeyCode):
        return key.char or ""
    if isinstance(key, keyboard.Key):
        return key.name or str(key)
    if isinstance(key, str):
        return key
    return str(key)


def deserialise_key(key_string: str) -> Any:
    """
    Convert a stored key string back into a pynput key object.

    Args:
        key_string: The saved key representation.

    Returns:
        Any: A pynput key object, or the default key when parsing fails.
    """
    if not key_string:
        return keyboard.Key.f6

    candidate = key_string.strip().lower()
    if candidate in keyboard.Key.__members__:
        return getattr(keyboard.Key, candidate)

    if candidate.startswith("key."):
        candidate = candidate[4:]
        if candidate in keyboard.Key.__members__:
            return getattr(keyboard.Key, candidate)

    return keyboard.KeyCode.from_char(candidate) if len(candidate) == 1 else keyboard.Key.f6 # f6 is the default


DEFAULT_SETTINGS = {
    "toggle_key": serialise_key(keyboard.Key.f6),
    "click_interval_mins": 0,
    "click_interval_secs": 0,
    "click_interval_ms": 400,
    "always_on_top": False,
    "dark_mode": True,
    "auto_minimize": True
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
        merged: The full settings dictionary that was written to disk.
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