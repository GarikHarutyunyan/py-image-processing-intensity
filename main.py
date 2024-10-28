import tkinter as tk
from gui import setup_gui

def main():
    root = tk.Tk()
    root.title("Image Transformations")
    setup_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
