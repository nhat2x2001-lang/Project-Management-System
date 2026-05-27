import tkinter as tk
from tkinter import messagebox

from app.gui import ConstructionApp


if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = ConstructionApp(root)
    except Exception as exc:
        messagebox.showerror("Startup Error", str(exc))
        root.destroy()
    else:
        root.protocol("WM_DELETE_WINDOW", app.close)
        root.mainloop()
