import threading
import time
from typing import Any

from pynput import keyboard, mouse

TOGGLE_KEY = keyboard.Key.f6

mouse_controller = mouse.Controller()
clicking = False
click_interval_ms = 400
last_click_time = 0.0
key_listener = None
clicker_thread = None

"""
Can work as a standalone autoclicker when ran but is restricted in use run the main for the full loadof features
"""

def on_press(key: Any):
    """
    Toggle the click loop when the configured hotkey is pressed.

    Args:
        key: The keyboard key that triggered the event.

    """
    global clicking
    try:
        if key == TOGGLE_KEY:
            set_clicking(not clicking)
    except Exception:
        pass


def set_clicking(enabled: bool):
    """
    Enable or disable the click loop.

    Args:
        enabled: Whether clicking should be turned on.
    """
    global clicking
    clicking = bool(enabled)


def toggle_clicking() -> bool:
    """Toggle the click loop and return its new state."""
    set_clicking(not clicking)
    return clicking


def is_clicking() -> bool:
    """
    Returns the state of the clicker

    Returns:
        True or False
    """
    return clicking

def set_click_interval(interval_ms : int, interval_secs : int = 0, interval_mins : int = 0):
    """
    Set the delay between simulated clicks in milliseconds.

    Args:
        interval_ms: The interval between clicks in milliseconds
        interval_secs: The interval between clicks in seconds default as 0
        interval_mins: The interval between clicks in minutes default as 0
    """
    global click_interval_ms
    interval_ms = interval_mins * 60000 + interval_secs * 1000 + interval_ms
    click_interval_ms = max(1, int(interval_ms))


def set_toggle_key(key: Any):
    """
    Store the hotkey used to toggle the clicker.

    Args:
        key: The new hotkey to use.
    """
    global TOGGLE_KEY
    TOGGLE_KEY = key

def get_toggle_key():
    """
    Returns:
        TOGGLE_KEY: The current hotkey.
    """
    return TOGGLE_KEY

def auto_clicker():
    """
    Run the click loop continuously until the process exits.
    """
    global last_click_time
    while True:
        if clicking:
            now = time.time()
            if now - last_click_time >= click_interval_ms / 1000:
                mouse_controller.click(mouse.Button.left, 1)
                last_click_time = now
        time.sleep(0.00001)


def listen_for_keys(): # only for when running via clicker.py and not using main/gui
    """
    Start the keyboard listener if it is not already running.

    Returns:
        key_listener: The active keyboard listener instance.
    """
    global key_listener
    if key_listener is not None:
        return key_listener

    key_listener = keyboard.Listener(on_press=on_press)
    key_listener.start()
    return key_listener


def start_clicker():
    """
    Start the clicker thread if it is not already running.

    Returns:
        clicker_thread: The clicker thread instance.
    """
    global clicker_thread
    if clicker_thread is None or not clicker_thread.is_alive():
        clicker_thread = threading.Thread(target=auto_clicker, daemon=True)
        clicker_thread.start()
    return clicker_thread


def start_clicker_services(clickerOnly : bool = False):
    """
    Start both the keyboard listener (if ran on own) and the clicker loop.
    """
    if clickerOnly: # if ran with main and not solo then handle the keys on the main app side
        listen_for_keys()
    start_clicker()


if __name__ == "__main__":
    print("Basic clicker started. Press F6 to toggle clicking.")
    start_clicker_services(True)
    while True:
        time.sleep(1)