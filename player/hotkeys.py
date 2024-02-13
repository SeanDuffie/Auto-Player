"""hotkeys.py
"""
import logging
import multiprocessing
import threading
import time

from pynput import keyboard


class Hotkey:
    """_summary_
    """
    def __init__(self, key: str):
        # Set key to be monitored
        # self.key = key
        # self.key = keyboard.Key(key)
        self.key = keyboard.Key.alt_gr

        # Variable to contain state
        self.active = False
        self.alive = True
        self.keys_pressed = set()

    def on_press(self, key):
        """_summary_

        Args:
            key (_type_): _description_
        """
        if self.alive:
            if key not in self.keys_pressed:
                self.keys_pressed.add(key)
                # print(key)
                if key == self.key:
                    self.active = not self.active
        else:
            logging.info("Killed Press Listener")
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
        if key == keyboard.Key.ctrl_r:
            # Stop keyboard.Listener
            self.alive = False
            logging.info("Killed Release Listener")
            return False

    def run(self):
        """_summary_
        """
        # Collect events until released
        logging.info("Initializing listener...")
        start = time.time()

        # Don't suppress, that disables keyboard output
        listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release,)

        logging.info("Listening...")
        listener.start()

        stop = time.time()
        logging.info("Took %f seconds", stop-start)

        listener.join()
        logging.info("Hotkey Finished")

    def quit(self):
        pass


if __name__ == "__main__":
    # Initial Logger Settings
    fmt_main = "%(asctime)s\t| %(levelname)s\t| %(message)s"
    logging.basicConfig(format=fmt_main, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

    htky = Hotkey("g")
    t1= threading.Thread(target=htky.run)
    logging.info("Starting hotkey thread")
    t1.start()

    logging.info("Starting state machine")
    while htky.alive:
        if htky.active:
            pass
        else:
            print("Inactive")
            while not htky.active:
                if htky.alive:
                    time.sleep(1)
                else:
                    break
            print("Active")
    logging.info("State Machine Finished")

    t1.join()
    logging.info("End main")
