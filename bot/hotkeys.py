"""hotkeys.py
"""
import logging
# import multiprocessing as mp
import threading
import time

from pynput import keyboard

# Initial Logger Settings
logger = logging.getLogger("Main.Hotkeys")


class Hotkey:
    """_summary_
    """
    def __init__(self, toggle_key: str | keyboard.Key = keyboard.Key.alt_gr, kill_key: str | keyboard.Key = keyboard.Key.ctrl_r):
        # Set key to be monitored
        if isinstance(toggle_key, str):
            self.toggle_key = keyboard.KeyCode.from_char(toggle_key)
        else:
            self.toggle_key = toggle_key
        if isinstance(kill_key, str):
            self.kill_key = keyboard.KeyCode.from_char(kill_key)
        else:
            self.kill_key = kill_key

        logger.info("toggle_key = %s", self.toggle_key)
        logger.info("kill_key = %s", self.kill_key)

        # Variable to contain state
        self.active = False
        self.alive = True
        self.keys_pressed = set()

        # # Multiprocessing stuff
        # self.toggle_event = mp.Event()
        # self.kill_event = mp.Event()

        # self.thread = mp.Process(target=)

    def on_press(self, key):
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        if self.alive:
            if key not in self.keys_pressed:
                self.keys_pressed.add(key)
                # print(key)
                if key == self.toggle_key:
                    self.active = not self.active
        else:
            logger.info("Killed Press Listener")
            return False
        return True

    def on_release(self, key):
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            self.keys_pressed.remove(key)
        except KeyError:
            pass  # started with key pressed?
        if key == self.kill_key:
            # Stop keyboard.Listener
            self.alive = False
            logger.info("Killed Release Listener")
            return False
        return True

    def run(self):
        """_summary_
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

    # def quit(self):
    #     self.toggle_event.clear()
    #     self.kill_event.set()
        
    #     self.thread.join()


if __name__ == "__main__":
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
