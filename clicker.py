import threading
import time
from pynput import keyboard, mouse

TOGGLE_KEY = keyboard.Key.f6

mouse_controller = mouse.Controller()
clicking = False
click_interval_ms = 400
last_click_time = 0.0
key_listener = None
clicker_thread = None


def on_press(key):
    global clicking
    try:
        if key == TOGGLE_KEY:
            clicking = not clicking
    except Exception:
        pass


def set_clicking(enabled):
    global clicking
    clicking = bool(enabled)


def set_click_interval(interval_ms):
    global click_interval_ms
    click_interval_ms = max(1, int(interval_ms))


def auto_clicker():
    global last_click_time
    while True:
        if clicking:
            now = time.time()
            if now - last_click_time >= click_interval_ms / 1000:
                mouse_controller.click(mouse.Button.left, 1)
                last_click_time = now
        time.sleep(0.001)


def listen_for_keys():
    global key_listener
    if key_listener is not None:
        return key_listener

    key_listener = keyboard.Listener(on_press=on_press)
    key_listener.start()
    return key_listener


def start_clicker():
    global clicker_thread
    if clicker_thread is None or not clicker_thread.is_alive():
        clicker_thread = threading.Thread(target=auto_clicker, daemon=True)
        clicker_thread.start()
    return clicker_thread


def start_clicker_services():
    listen_for_keys()
    start_clicker()


if __name__ == "__main__":
    print("Basic clicker started. Press F6 to toggle clicking.")
    start_clicker_services()
    while True:
        time.sleep(1)