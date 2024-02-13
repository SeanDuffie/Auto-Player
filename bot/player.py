""" player.py

    This file handles any interactions that simulate the player.
    It functions mainly as a wrapper for pyautogui
    Mouse functions:
        - Click buttons
    Keyboard functions:
        - Hold down key
        - Release key
        - Momentary press
"""
import time

import pyautogui as pg


class Player:
    """_summary_
    """
    def __init__(self):
        pass

    def basic_fisher(self):
        """ Simple iteration of the auto fisher
            Does initial cast, then waits 10 seconds to recast
        """
        self.mouse_clicks(button=1)

        while True:
            time.sleep(10)
            self.mouse_clicks(button=1, count=2, interval=10)

    def mouse_clicks(self,
                     button: str = "right",
                     count: int = 1,
                     interval: float = 0,
                     loc: tuple[int, int] = None):
        """ Click the mouse, options are configurable such as button, timing, and count.

        Args:
            button (str, optional): _description_. Defaults to "right".
            count (int, optional): _description_. Defaults to 1.
            interval (float, optional): _description_. Defaults to 0.
            loc (tuple[int, int]): _description_. Defaults to [None, None].

        Returns:
            _type_: _description_
        """
        pg.click(x=loc, clicks=count, interval=interval, button=button)
        # case _: # default
        #     print("Invalid Mouse Button")
        #     return False
        return True

    def key_press(self, key: str | list) -> bool:
        """ Presses and releases the specified key, if input is a list then holds down all.

        Available Keys:
            ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
            ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
            '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
            'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
            'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
            'browserback', 'browserfavorites', 'browserforward', 'browserhome',
            'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
            'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
            'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
            'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
            'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
            'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
            'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
            'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
            'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
            'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
            'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
            'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
            'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
            'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
            'command', 'option', 'optionleft', 'optionright']

        Args:
            key (str | list): key(s) to be pressed (options are in the list above)

        Returns:
            bool: _description_
        """
        if key.isType(list):
            for k in key:
                if not pg.isValidKey(k):
                    return False
            pg.press(key)
            return True

        if pg.isValidKey(key):
            pg.press(key)
        else:
            return False
        return True

    def key_down(self, key: str | list) -> bool:
        """ Holds down the specified button, if input is a list then holds down all.

        Available Keys:
            ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
            ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
            '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
            'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
            'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
            'browserback', 'browserfavorites', 'browserforward', 'browserhome',
            'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
            'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
            'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
            'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
            'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
            'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
            'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
            'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
            'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
            'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
            'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
            'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
            'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
            'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
            'command', 'option', 'optionleft', 'optionright']

        Args:
            key (str | list): key(s) to be held down (options are in the list above)

        Returns:
            bool: _description_
        """
        if pg.isValidKey(key):
            pg.keyDown(key)
        else:
            return False
        return True

    def key_up(self, key: str | list) -> bool:
        """ Releases the specified key, if input is a list then holds down all.

        Available Keys:
            ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
            ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
            '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
            'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
            'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
            'browserback', 'browserfavorites', 'browserforward', 'browserhome',
            'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
            'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
            'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
            'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
            'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
            'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
            'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
            'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
            'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
            'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
            'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
            'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
            'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
            'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
            'command', 'option', 'optionleft', 'optionright']

        Args:
            key (str | list):  key(s) to be released (options are in the list above)

        Returns:
            bool: _description_
        """
        if pg.isValidKey(key):
            pg.keyUp(key)
        else:
            return False
        return True
