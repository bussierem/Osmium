from tkinter import Tk

from gui.main_app import MainApp

if __name__ == "__main__":
    root = Tk()
    root.geometry('{}x{}'.format(1024, 768))
    root.iconbitmap(r'./icons/osmium.ico')
    root.update()
    app = MainApp(master=root)
    app.mainloop()
