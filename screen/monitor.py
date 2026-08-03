from PySide6.QtWidgets import QApplication

monitors = []

"""Handles getting monitors and their information"""

class Monitor():
    """ Monitor objects for storing information about each monitor """
    def __init__(self, monitor_id: int, name: str, width: int, height: int, scaled_width : int, scaled_height : int, scale : int | float, primary: bool):
        self.id : int = monitor_id
        self.name : str = name

        # height and width used for logic
        self.width : int = width
        self.height : int = height

        #scaled height and width for ui display
        self.scaled_width : int = scaled_width
        self.scaled_height : int = scaled_height
        self.scale : int | float = scale
        
        self.primary : bool = primary

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str | None:
        return self.name

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_primary(self) -> bool:
        return self.primary


def load_monitors() -> list[Monitor]:
    """
    Gets all the monitors and stores their information.

    Returns:
        monitors: A list of all the monitors as objects.
    """
    monitors.clear

    screens = QApplication.screens()
    primary_screen = QApplication.primaryScreen()

    for index, screen in enumerate(screens):
        geometry = screen.geometry()
        scale = screen.devicePixelRatio()

        scaled_width = int(geometry.width() * scale)
        scaled_height = int(geometry.height() * scale)

        monitors.append(Monitor(monitor_id=index, 
                                name=screen.name(), 
                                width=geometry.width(), 
                                height=geometry.height(),
                                 scaled_width=scaled_width, 
                                 scaled_height=scaled_height, 
                                 scale=scale, 
                                 primary=(screen == primary_screen))
                                 )

    return monitors

def get_loaded_mointors() -> list[Monitor]:
    """
    Gets all of the loaded monitors.

    Returns:
        monitors: A list of all loaded monitors.
    """
    global monitors
    return monitors