""" @file obs_renamer.py
    @author Sean Duffie
    @brief aid tool for organizing and renaming OBS clips
    
    Features:
    - [ ] Add game name to the filename
    - [ ] Group Clips by month/year
    - [ ] Mark overlapping clips??
"""
import sys

if sys.platform == 'win32':
    import winreg
elif sys.platform == 'linux' or sys.platform == 'linux2':
    import os
    import re

def get_running_steam_game():
    """ Returns the process id of the currently running steam game.

    Returns:
        _type_: _description_
    """
    if sys.platform == 'win32':
        try:
            key = winreg.OpenKey(
                key=winreg.HKEY_CURRENT_USER,
                sub_key=r"Software\Valve\Steam",
                reserved=0,
                access=winreg.KEY_READ
            )
            value, _ = winreg.QueryValueEx(key, "RunningAppID")
            winreg.CloseKey(key)

            if value:
                return value
            else:
                return None
        except FileNotFoundError:
            return None
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        try:
            with open(os.path.expanduser("~/.steam/registry.vdf"), 'r', encoding="utf-8") as f:
                content = f.read()
                match = re.search(r'"RunningAppID"\s+"(\d+)"', content)
                if match:
                    return match.group(1)
                else:
                    return None
        except FileNotFoundError:
            return None
    else:
        return None

if __name__ == "__main__":
    running_app_id = get_running_steam_game()
    if running_app_id:
        print(f"Running Steam App ID: {running_app_id}")
    else:
        print("No Steam game is currently running.")
