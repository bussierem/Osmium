import sys, os, stat
import tkinter as tk
from tkinter import filedialog, messagebox
import pexpect

BUTTON_FONT = ("Helvetica", 17)
LABEL_FONT = ("Helvetica", 14)
ENTRY_FONT = ("DejaVu Sans Mono", 12)
POLL_TIME = 50  # Polling frequency in milliseconds

def main():
    app = App()
    app.master.title("Copy with progress bar")
    app.mainloop()

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.__createWidgets()

    def __createWidgets(self):
        self.fromFileVar = tk.StringVar()
        self.fromFileEntry = tk.Entry(self,
                                      textvariable=self.fromFileVar,
                                      font=ENTRY_FONT, width=50)
        rowx, colx = 0, 0
        self.fromFileEntry.grid(row=rowx, column=colx, sticky=tk.E)

        self.fromFileBrowse = tk.Button(self,
                                        command=self.__browseFrom,
                                        font=BUTTON_FONT, text="Browse")
        colx += 1
        self.fromFileBrowse.grid(row=rowx, column=colx)

        self.fromFileLabel = tk.Label(self,
                                      font=LABEL_FONT, text="Source file")
        colx += 1
        self.fromFileLabel.grid(row=rowx, column=colx, sticky=tk.W)

        self.toFileVar = tk.StringVar()
        self.toFileEntry = tk.Entry(self,
                                    textvariable=self.toFileVar,
                                    font=ENTRY_FONT, width=50)
        rowx, colx = rowx + 1, 0
        self.toFileEntry.grid(row=rowx, column=colx, sticky=tk.E)

        self.toFileBrowse = tk.Button(self,
                                      command=self.__browseTo,
                                      font=BUTTON_FONT, text="Browse")
        colx += 1
        self.toFileBrowse.grid(row=rowx, column=colx)

        self.toFileLabel = tk.Label(self,
                                    font=LABEL_FONT, text="Destination file")
        colx += 1
        self.toFileLabel.grid(row=rowx, column=colx, sticky=tk.W)

        self.progressVar = tk.DoubleVar()
        self.progressScale = tk.Scale(self,
                                      length=400, orient=tk.HORIZONTAL,
                                      from_=0.0, to=100.0, resolution=0.1, tickinterval=20.0,
                                      variable=self.progressVar,
                                      label="Percent completion", font=LABEL_FONT)
        rowx, colx = rowx + 1, 0
        self.progressScale.grid(row=rowx, column=colx, sticky=tk.E)

        self.copyButton = tk.Button(self,
                                    command=self.__copyHandler,
                                    font=BUTTON_FONT, text="Copy")
        colx += 1
        self.copyButton.grid(row=rowx, column=colx)

        self.quitButton = tk.Button(self, command=self.quit,
                                    font=BUTTON_FONT, text="Quit")
        colx += 1
        self.quitButton.grid(row=rowx, column=colx, sticky=tk.W)

    def __browseFrom(self):
        f = filedialog.askopenfilename(title="Source file name")
        if len(f) == 0:
            return
        else:
            self.fromFileVar.set(f)

    def __browseTo(self):
        f = filedialog.asksaveasfilename(title="Destination file name")
        if len(f) == 0:
            return
        else:
            self.toFileVar.set(f)

    def __copyHandler(self):
        if len(self.fromFileVar.get()) == 0:
            messagebox.showerror("Error",
                                   "Please enter a source file name.")
            return
        toFileName = self.toFileVar.get()
        if len(toFileName) == 0:
            messagebox.showerror("Error",
                                   "Please enter a destination file name.")
            return
        elif os.path.exists(toFileName):
            message = ("File '%s' exists.\nDo you want to overwrite "
                       "it?" % toFileName)
            answer = messagebox.askokcancel("Destination file exists",
                                              message, default=messagebox.CANCEL)
            if not answer:
                return
        if not self.__copySetup():
            return
        self.__startCopy()

    def __copySetup(self):
        fromFileName = self.fromFileVar.get()
        try:
            self.fromFileSize = self.__measureFile(fromFileName)
        except OSError as e:
            messagebox.showerror("Source file error",
                                   "File %s: %s" % (fromFileName, str(e)))
            return False
        return True

    def __startCopy(self):
        command = ("cp -f %s %s" %
                   (self.fromFileVar.get(), self.toFileVar.get()))
        self.progressVar.set(0.0)
        self.after(POLL_TIME, self.__poll)
        self.child = pexpect.spawn(command)

    def __measureFile(self, fileName):
        status = os.stat(fileName)
        return status[stat.ST_SIZE]

    def __poll(self):
        if not self.child.isalive():
            self.child.close()
            self.progressVar.set(100.0)
            messagebox.showinfo("Success",
                                  "File %s has been copied to %s, size %s." %
                                  (self.fromFileVar.get(), self.toFileVar.get(),
                                   self.fromFileSize))
            return
        toFileName = self.toFileVar.get()
        try:
            toFileSize = self.__measureFile(toFileName)
        except OSError as e:
            messagebox.showerror("Destination file error",
                                   "File %s: %s" % (toFileName, str(e)))
            return
        self.progressVar.set(100.0 * float(toFileSize) /
                             float(self.fromFileSize))
        self.after(POLL_TIME, self.__poll)

if __name__ == "__main__":
    main()