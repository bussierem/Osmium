from tkinter import Tk
from gui.window_manager import WindowManager

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    app = WindowManager(master=root)
    app.mainloop()