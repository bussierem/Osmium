if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    # root = Tk()
    # root.geometry('{}x{}'.format(1024, 768))
    # root.update()
    # app = MainApp(master=root)
    # app.mainloop()
