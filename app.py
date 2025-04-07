import tkinter as tk

RUNNING = False

border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

def save(event = None):
    print("save")

def load(event = None):
    print("load")

def toggle(event = None):
    """_summary_

    Args:
        event (_type_, optional): _description_. Defaults to None.
    """
    global RUNNING
    print("toggle")
    if RUNNING:
        button_toggle.config(text="Stop")
        RUNNING = False
    else:
        button_toggle.config(text="Start")
        RUNNING = True

def validate_input(new_text):
    """ Validates that a text input is a valid int

    Args:
        new_text (str): raw text input

    Returns:
        bool: Can the text value be converted to an int?
    """
    if not new_text:
        return True
    try:
        int(new_text)
        return True
    except ValueError:
        return False

# def resize(event):
#     button_save.config(width=event.width // 3)
#     button_load.config(width=event.width // 3)
#     button_toggle.config(width=event.width // 3)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Auto Player")

    for row in range(4):
        window.columnconfigure(row, weight=1, minsize=50)
        window.rowconfigure(row, weight=1, minsize=75)

        # for col in range(5):
        #     frame = tk.Frame(
        #         master=window,
        #     )
        #     # frame.grid(row=row, column=col, padx=1, pady=1)
        #     # label = tk.Label(master=frame, text="Hello")
        #     # label.pack()

    box = tk.Frame(master=window,relief=border_effects["groove"])
    # box.grid(column=0)

    buttons = tk.Frame(master=window)

    button_save = tk.Button(
        master=buttons,
        text="Save Preset",
        command=save,
    )
    button_load = tk.Button(
        master=buttons,
        text="Load Preset",
        command=load,
    )
    button_toggle = tk.Button(
        master=buttons,
        text="Start/Stop",
        command=toggle,
    )

    button_save.grid(row=2, column=1)
    button_load.grid(row=2, column=2)
    button_toggle.grid(row=2, column=3)
    buttons.grid(row=2)


    ### Binds
    # button_save.bind("<Button-1>", save)
    # button_load.bind("<Button-1>", load)
    # button_toggle.bind("<Button-1>", toggle)
    # window.bind("<Configure>", resize)

    # Begin the Loop
    window.mainloop()
