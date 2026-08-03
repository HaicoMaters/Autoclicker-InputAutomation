import threading
import time
from typing import Any
import random

from pynput import keyboard, mouse

TOGGLE_KEY = keyboard.Key.f6 # only for running this as a solo file

mouse_controller = mouse.Controller()
clicking = False
click_interval_ms = 400
last_click_time = 0.0
key_listener = None
clicker_thread = None
number_of_clicks = 1
mouse_button = mouse.Button.left
random_offset = 0
next_offset = 0
click_target_location: tuple[int, int] | None = None 

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

def set_random_offset(offset : int):
    """
    Sets the range of the random offset between each click (-offset -> offset)

    Args:
        offset: the number of milliseconds to potentially offset each click by
    """
    global random_offset
    random_offset = offset

def set_number_of_clicks(clicks : int):
    """
    Sets the number of clicks to perform per interval

    Args:
        clicks: number of clocks to carry per interval (usually single or double 1 or 2)
    """
    global number_of_clicks
    number_of_clicks = clicks

def set_mouse_button(button : mouse.Button):
    """
    Sets the mouse button to auto click with

    Args:
        button: the mouse button object left, right or middle
    """
    global mouse_button
    mouse_button = button


def set_click_target(target: tuple[int, int] | None):
    """
    Set a fixed screen location for the next click actions.

    Args:
        target: A screen coordinate tuple of (x, y), or None to use the
            current mouse position.
    """
    global click_target_location
    click_target_location = target


def clear_click_target() -> None:
    """
    Remove any fixed click target so the cursor stays where it is.
    """
    set_click_target(None)


def get_click_target() -> tuple[int, int] | None:
    """
    Return the currently configured fixed click target, if any.
    """
    return click_target_location


def perform_click() -> None:
    """
    Move to the configured target (if present) and trigger a click.
    """
    global click_target_location
    if click_target_location is not None:
        mouse_controller.position = click_target_location
    mouse_controller.click(mouse_button, number_of_clicks)


def set_click_interval(interval_ms : int, interval_secs : int = 0, interval_mins : int = 0):
    """
    Set the delay between simulated clicks in milliseconds.

    Args:
        interval_ms: The interval between clicks in milliseconds.
        interval_secs: The interval between clicks in seconds default as 0.
        interval_mins: The interval between clicks in minutes default as 0.
    """
    global click_interval_ms
    interval_ms = interval_mins * 60000 + interval_secs * 1000 + interval_ms
    click_interval_ms = interval_ms


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
    global last_click_time, mouse_button, number_of_clicks, next_offset, random_offset
    while True:
        if clicking:
            now = time.time()
            if now - last_click_time >= (click_interval_ms + next_offset) / 1000:
                perform_click()
                last_click_time = now
                
                if random_offset:
                    next_offset = random.randint(-random_offset, random_offset)
                else:
                    next_offset = 0

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