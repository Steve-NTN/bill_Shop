from tkinter import *
from tkinter import ttk, messagebox

def newWindow():
    newW = Toplevel(root)
    newW.title("New window")
    newW.geometry("100x100")
root = Tk()
root.geometry("200x200")
bt = Button(root, text="Click", command=newWindow).pack()
root.mainloop()