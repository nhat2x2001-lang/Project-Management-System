# app/widgets/treeview.py — Reusable scrollable treeview widget.

import tkinter as tk
from tkinter import ttk

from app import theme


class ScrollableTreeview(ttk.Frame):
    """A ttk.Treeview with vertical and horizontal scrollbars already wired up.

    Usage
    -----
    tree_widget = ScrollableTreeview(parent, columns=["ID", "Name", "Value"], height=10)
    tree_widget.pack(fill="both", expand=True)

    # Access the underlying Treeview:
    tree_widget.tree.insert("", "end", values=("1", "Alice", "100"))

    # Clear rows:
    tree_widget.clear()
    """

    def __init__(self, parent, columns: list, height: int = 8, **kwargs):
        super().__init__(parent, style="TFrame", **kwargs)

        self.tree = ttk.Treeview(
            self, columns=columns, show="headings",
            selectmode="browse", height=height
        )

        vsb = ttk.Scrollbar(self, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " "))
            self.tree.column(col, width=130, anchor="center", minwidth=60)

        # Zebra-stripe tags
        self.tree.tag_configure("evenrow", background="#f7f9fc")
        self.tree.tag_configure("oddrow",  background=theme.CARD_BG)

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def populate(self, rows: list, columns=None):
        """Insert rows into the treeview.

        Parameters
        ----------
        rows : list of dict
            Each dict must have keys matching the treeview column names.
        columns : list of str, optional
            Override column order. Defaults to the columns the tree was built with.
        """
        self.clear()
        cols = columns if columns else list(self.tree["columns"])
        for idx, row in enumerate(rows):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", "end",
                             values=tuple(row[col] for col in cols),
                             tags=(tag,))

    def bind_select(self, callback):
        """Shortcut to bind the TreeviewSelect event."""
        self.tree.bind("<<TreeviewSelect>>", callback)

    def get_selected_values(self) -> tuple | None:
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0], "values")
