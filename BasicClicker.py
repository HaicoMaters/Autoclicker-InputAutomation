import threading
from pynput import keyboard, mouse
import time

TOGGLE_KEY = keyboard.Key.f6

mouse_controller = mouse.Controller()
clicking = False


def on_press(key):
    global clicking
    try:
        if key == TOGGLE_KEY:
            clicking = not clicking
            print("Clicking started" if clicking else "Clicking stopped")
    except Exception:
        pass


def auto_clicker():
    while True:
        if clicking:
            mouse_controller.click(mouse.Button.left, 1)
        time.sleep(0.001) #Sleep allows for checking toggle key and exit key


def listen_for_keys():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    print("Basic clicker started. Press F6 to toggle clicking.")
    key_listener_thread = threading.Thread(target=listen_for_keys)
    key_listener_thread.daemon = True
    key_listener_thread.start()
    auto_clicker()