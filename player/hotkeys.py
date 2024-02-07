"""hotkeys.py
"""
import logging
import time
from pynput.keyboard import Key, Listener
import threading


class Hotkey:
    """_summary_
    """
    def __init__(self, key: str):
        # Set key to be monitored
        # self.key = key
        # self.key = Key(key)
        self.key = Key.alt_gr

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
                if key == self.key:
                    self.active = not self.active
        else:
            logging.info("killed press")
            return False

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
        if key == Key.ctrl_r:
            # Stop listener
            self.alive = False
            logging.info("killed release")
            return False

    def run(self):
        """_summary_
        """
        # Collect events until released
        logging.info("Initializing listener...")
        start = time.time()

        # Don't suppress, that disables keyboard output
        listener = Listener(
                on_press=self.on_press,
                on_release=self.on_release)

        logging.info("Listening...")
        listener.start()

        stop = time.time()
        logging.info("Took %f seconds", stop-start)

        listener.join()
        logging.info("Hotkey Finished")


if __name__ == "__main__":
    # Initial Logger Settings
    fmt_main = "%(asctime)s\t| %(levelname)s\t| %(message)s"
    logging.basicConfig(format=fmt_main, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

    ACTIVE = False
    ALIVE = True

    htky = Hotkey("g")

    def foo():
        """_summary_
        """
        global ACTIVE, ALIVE
        while ALIVE:
            if ACTIVE:
                pass
            else:
                while not ACTIVE:
                    if ALIVE:
                        time.sleep(1)
                    else:
                        break
        logging.info("Foo Finished")

    def check():
        """_summary_
        """
        global ACTIVE, ALIVE
        while ALIVE:
            if ACTIVE != htky.active:
                logging.info("Active = %s", htky.active)
                ACTIVE = htky.active
            ALIVE = htky.alive
        logging.info("Check Finished")

    t1 = threading.Thread(target=foo)
    t2 = threading.Thread(target=check)
    logging.info("Starting t1")
    t1.start()
    logging.info("Starting t2")
    t2.start()


    logging.info("Starting hotkey thread")
    htky.run()
    t1.join()
    t2.join()
    logging.info("End main")
