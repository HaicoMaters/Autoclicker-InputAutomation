# Autoclicker-InputAutomation

A lightweight autoclicker with a small GUI for controlling timing, click type, and click location. The project is still in progress, but the core automation flow is already usable.

## License
This project is licensed under the MIT License. You are free to use, modify, and redistribute it, including for commercial purposes, as long as the license notice is preserved.

## Features
- Toggle autoclicking with a configurable hotkey
- Choose click interval in minutes, seconds, and milliseconds
- Optionally add a random timing offset between clicks
- Select left, right, or middle mouse button
- Use single or double clicks
- Choose between following the current mouse position or using a fixed screen location
- Persist settings such as toggle key, interval, dark mode, and auto-minimize.

## Requirements
Install the Python dependencies from the repository root:

```bash
pip install -r requirements.txt
```

## How to run
From the project root, launch the application with:

```bash
python main.py
```

You can alternatively, run the clicker as a more basic non-visual application which clicks at max speed, following the mouse with f6 as a toggle key with:

```bash
python clicker.py
```

## Usage
- Start the app and adjust the interval and click options in the main window.
- Press the configured toggle hotkey (default: F6) to start and stop clicking.
- Use the Settings window to change the hotkey, appearance, auto-minimize behavior..
- For fixed-location clicks, select Fixed Location and either choose a monitor or use the Change Location button to record a target point.

## Configuration
Settings are stored in the project-level settings.json file. Common keys include:
- toggle_key
- click_interval_mins / click_interval_secs / click_interval_ms
- dark_mode
- auto_minimize

## Project structure
- clicker.py: Core autoclicking loop and click target handling
- main.py: Application entry point
- config.py: Main configuration handling
- gui/: Main window and settings window UI
- ui/: Styles and handling for GUI
- screen/: Monitor and mouse recording helpers
- tests/: Automated regression tests

## ToDo
- add more planned features (e.g. designating areas of the screen to make so can only autoclick within or excluding designated area, or a random jitter/- offset in location between click)
- add icon if feel like doing so
- add unit testing
- consider proper exe releases