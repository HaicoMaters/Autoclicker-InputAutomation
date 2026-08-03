from pynput import mouse

class MouseRecorder():
    """ Class for recording data related to mouse inputs i.e. location on the screen """

    def __init__(self):
        self.mouse_listener : mouse.Listener | None = None
        self.single_location_x : int | None = None
        self.single_location_y : int | None = None

    def listen_for_mouse(self, func) -> mouse.Listener:
        """
        Start the mouse listener if it is not already running and binds it to a function.
        
        Args:
            func: The function to bind the on_click of the mouse listener to.

        Returns:
            mouse_listener: The active mouse listener instance, bouund to it's relevant function.
        """
        if self.mouse_listener is not None:
            return self.mouse_listener
        
        self.mouse_listener = mouse.Listener(on_click=func)
        self.mouse_listener.start()
        return self.mouse_listener

    def stop_listener(self) -> None:
        """
        Stop the mouse listener instance and set it to None
        """
        self.mouse_listener.stop()
        self.mouse_listener = None

    def is_listening(self) -> bool:
        """
        Return the current state of if the recorder is listening for a mouse input.

        Returns:
            mouse_listener.is_alive(): is the listener currently active
        """
        if self.mouse_listener is None:
            return False
        return self.mouse_listener.is_alive()

    def record_single_click_location(self, x, y) -> None:
        """
        Records a single mouse click location based on user's screen, and stops the mouse listener after a single input.

        Args:
            x,y: The x and y coords where of the click recieved from the mouse listener.
        """
        self.single_x = x
        self.single_y = y
        self.stop_listener()

    def get_single_click_location(self) -> tuple[int, int]:
        """
        Gets the recorded location from the single click location

        Returns:
            (x,y): The x and y coordinate of the single click location recording
        """
        return (self.single_location_x, self.single_location_y)