import tkinter as tk

if __name__ == "__main__":
    window = tk.Tk()
    window.title("My Tkinter App")

    label = tk.Label(window, text="Hello, Tkinter!")
    label.pack()
    button = tk.Button(window, text="Click Me")
    button.pack()
    button = tk.Button(window, text="Click Me")
    button.pack()
    button = tk.Button(window, text="Click Me")
    button.pack()

    window.mainloop()
