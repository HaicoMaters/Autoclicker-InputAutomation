from pynput import keyboard

import config


def test_serialise_and_deserialise_special_key():
    key = keyboard.Key.f6
    assert config.serialise_key(key) == "f6"
    assert config.deserialise_key("f6") == keyboard.Key.f6


def test_deserialise_character_key():
    key = config.deserialise_key("a")
    assert isinstance(key, keyboard.KeyCode)
    assert key.char == "a"
