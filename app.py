import tkinter as tk
from tkinter import messagebox

from app.gui import ConstructionApp


def main():
    root = tk.Tk()
    try:
        app = ConstructionApp(root)
    except Exception as exc:
        messagebox.showerror("Startup Error", str(exc))
        root.destroy()
        return

    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


if __name__ == "__main__":
    main()
