""" @file hotkeys.py
    @author Sean Duffie
    @brief Allows the user to toggle program state asynchronously with the keyboard.

    This was originally developed for the [Auto-Player](https://github.com/SeanDuffie/Auto-Player)
    program, however it can probably be easily recycled into other programs.

    TODO: In the future, This could be expanded by adding a dictionary of hotkeys and their
        associated flags. This would allow for more hotkeys, as well as more customization by the
        user.
"""
import logging
import threading
import time

from pynput import keyboard

# Initial Logger Settings
logger = logging.getLogger("Auto")


class Hotkey:
    """ The Hotkey object allows the user to toggle states with customized hotkeys asynchronously

        The benefit of this over using "input()" or other methods is that this can be run on a
        separate thread to allow maximum responsiveness. Additionaly, this works no matter what
        window is in focus.

        After initializing an object and calling Hotkey.run(), the user should be able to check
        the current state by calling the boolean class variables Hotkey.active and Hotkey.alive.
        These (respectively) indicate whether the activity has been paused or killed entirely.
    """
    def __init__(self,
                 toggle_key: str | keyboard.Key = keyboard.Key.alt_gr,
                 kill_key: str | keyboard.Key = keyboard.Key.ctrl_r):
        """ Initializer function for Hotkey()

        Args:
            toggle_key (str | keyboard.Key, optional): Key designated to toggle functionality.
                                                        Defaults to keyboard.Key.alt_gr.
            kill_key (str | keyboard.Key, optional): Key designated to kill the process.
                                                        Defaults to keyboard.Key.ctrl_r.
        """
        # Set key to be monitored
        if isinstance(toggle_key, str):
            # TODO: Add error handling here
            self.toggle_key = keyboard.KeyCode.from_char(toggle_key)
        else:
            self.toggle_key = toggle_key
        if isinstance(kill_key, str):
            # TODO: Add error handling here
            self.kill_key = keyboard.KeyCode.from_char(kill_key)
        else:
            self.kill_key = kill_key

        logger.info("toggle_key = %s", self.toggle_key)
        logger.info("kill_key = %s", self.kill_key)

        # Variables to contain state
        self.active = False
        self.alive = True
        # NOTE: This fixed the lag/latency issue from too many keys flooding the queue
        self.keys_pressed = set()

    def on_press(self, key: keyboard.Key):
        """ Event Handler for when a keydown event is observed by the key listener.

        Args:
            key (keyboard.Key): the key that was pressed.

        Returns:
            bool: whether the listener thread should continue or not.
        """
        # Only handle keypresses if the program is alive
        if self.alive:
            # If the key is not already being pressed, don't flood the event queue
            if key not in self.keys_pressed:
                # Add the key to the dictionary of keys that are currently being held
                self.keys_pressed.add(key)

                # If the observed key is toggle_key, toggle the active state
                if key == self.toggle_key:
                    self.active = not self.active
        else:
            logger.info("Killed Press Listener")
            return False
        return True

    def on_release(self, key):
        """ Event Handler for when a keyup event is observed by the key listener.

        Args:
            key (keyboard.Key): the key that was released.

        Returns:
            bool: whether the listener thread should continue or not.
        """
        try:
            # Remove the key from the held dictionary to allow further detection
            self.keys_pressed.remove(key)
        except KeyError:
            # logger.error("Keyup event detected without a keydown?")
            pass  # started with key pressed?

        # If the observed key is the kill_key, kill the key listener
        if key == self.kill_key:
            # Stop keyboard.Listener
            self.alive = False
            logger.info("Killed Release Listener")
            return False
        return True

    def run(self):
        """ Launches the Hotkey Listener after initialization.

            This is separated from __init__() so that the user has the option to place it on the
            main thread or a background thread to enhance responsiveness.

            Returns:
                None
        """
        # Collect events until released
        logger.info("Initializing listener...")
        start = time.time()

        # Don't suppress, that disables keyboard output
        listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release,)

        logger.info("Listening...")
        listener.start()

        stop = time.time()
        logger.info("Took %f seconds", stop-start)

        listener.join()
        logger.info("Hotkey Finished")


if __name__ == "__main__":
    # Example use case
    htky = Hotkey()
    t1= threading.Thread(target=htky.run)
    logger.info("Starting hotkey thread")
    t1.start()

    logger.info("Starting state machine")
    while htky.alive:
        if htky.active:
            pass
        else:
            logger.info("Inactive")
            while not htky.active:
                if htky.alive:
                    time.sleep(1)
                else:
                    break
            logger.info("Active")
    logger.info("State Machine Finished")

    t1.join()
    logger.info("End main")
