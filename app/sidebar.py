# app/sidebar.py — Collapsible dark-navy sidebar navigation widget.

import tkinter as tk
from tkinter import ttk

from app import theme


class SidebarItem:
    """Holds the widgets and state for a single navigation item."""
    __slots__ = ("btn", "icon", "label", "command")

    def __init__(self, btn: tk.Button, icon: str, label: str, command):
        self.btn     = btn
        self.icon    = icon
        self.label   = label
        self.command = command


class CollapsibleSidebar(tk.Frame):
    """A collapsible sidebar with navigation items.

    Expanded width : 220 px   (icon + text visible)
    Collapsed width:  64 px   (icon only)

    Usage
    -----
    sidebar = CollapsibleSidebar(parent, on_width_change=lambda: ...)
    sidebar.add_item("📊", "Dashboard",         callback_dashboard)
    sidebar.add_item("📋", "Task Monitoring",   callback_tasks)
    sidebar.set_active(0)
    sidebar.pack(side="left", fill="y")
    """

    EXPANDED_W  = 220
    COLLAPSED_W = 64

    def __init__(self, parent, on_width_change=None, **kwargs):
        super().__init__(parent, bg=theme.SIDEBAR_BG,
                         width=self.EXPANDED_W, **kwargs)
        self.pack_propagate(False)          # keep fixed width

        self._items = []
        self._active_index = None
        self._expanded: bool            = True
        self._on_width_change           = on_width_change

        self._build_header()
        self._separator()
        # Items will be appended below the separator
        self._items_frame = tk.Frame(self, bg=theme.SIDEBAR_BG)
        self._items_frame.pack(fill="x", pady=(4, 0))

        # Bottom separator + version
        self._separator()
        self._build_footer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_item(self, icon: str, label: str, command) -> int:
        """Append a nav item and return its index."""
        idx = len(self._items)

        btn = tk.Button(
            self._items_frame,
            text=f"  {icon}  {label}",
            anchor="w",
            bg=theme.SIDEBAR_BG,
            fg=theme.SIDEBAR_TEXT,
            activebackground=theme.SIDEBAR_HOVER,
            activeforeground=theme.SIDEBAR_TEXT,
            font=(theme.FONT_FAMILY, 10),
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=10,
            bd=0,
        )
        btn.pack(fill="x", padx=0, pady=1)
        btn.bind("<Enter>", lambda e, b=btn: self._on_hover_enter(b))
        btn.bind("<Leave>", lambda e, b=btn, i=idx: self._on_hover_leave(b, i))

        item = SidebarItem(btn, icon, label, command)
        self._items.append(item)

        btn.config(command=lambda i=idx: self._handle_click(i))
        return idx

    def set_active(self, index: int) -> None:
        """Highlight the item at *index* as active; de-highlight others."""
        for i, item in enumerate(self._items):
            if i == index:
                item.btn.config(bg=theme.SIDEBAR_ACTIVE,
                                fg=theme.SIDEBAR_TEXT,
                                font=(theme.FONT_FAMILY, 10, "bold"))
            else:
                item.btn.config(bg=theme.SIDEBAR_BG,
                                fg=theme.SIDEBAR_TEXT,
                                font=(theme.FONT_FAMILY, 10))
        self._active_index = index

    # ------------------------------------------------------------------
    # Internal builders
    # ------------------------------------------------------------------

    def _build_header(self):
        header = tk.Frame(self, bg=theme.SIDEBAR_BG)
        header.pack(fill="x", pady=(10, 4))

        # App logo / name
        self._logo_label = tk.Label(
            header,
            text="  🏗  Project Uno",
            bg=theme.SIDEBAR_BG,
            fg=theme.SIDEBAR_TEXT,
            font=(theme.FONT_FAMILY, 13, "bold"),
            anchor="w",
        )
        self._logo_label.pack(side="left", fill="x", expand=True, padx=(4, 0))

        # Toggle chevron button
        self._toggle_btn = tk.Button(
            header,
            text="◀",
            bg=theme.SIDEBAR_BG,
            fg=theme.SIDEBAR_ICON,
            activebackground=theme.SIDEBAR_HOVER,
            activeforeground=theme.SIDEBAR_TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(theme.FONT_FAMILY, 10),
            padx=8, pady=4,
            command=self._toggle,
        )
        self._toggle_btn.pack(side="right", padx=4)

    def _build_footer(self):
        footer = tk.Frame(self, bg=theme.SIDEBAR_BG)
        footer.pack(side="bottom", fill="x", pady=10)
        self._footer_label = tk.Label(
            footer,
            text="  Construction Mgmt",
            bg=theme.SIDEBAR_BG,
            fg=theme.SIDEBAR_ICON,
            font=(theme.FONT_FAMILY, 8),
            anchor="w",
        )
        self._footer_label.pack(fill="x", padx=4)

    def _separator(self):
        sep = tk.Frame(self, bg=theme.SIDEBAR_BORDER, height=1)
        sep.pack(fill="x")

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------

    def _toggle(self):
        if self._expanded:
            self._collapse()
        else:
            self._expand()
        if self._on_width_change:
            self._on_width_change()

    def _expand(self):
        self._expanded = True
        self.config(width=self.EXPANDED_W)
        self._toggle_btn.config(text="◀")

        self._logo_label.config(text="  🏗  Project Uno")
        self._footer_label.config(text="  Construction Mgmt")

        for item in self._items:
            item.btn.config(text=f"  {item.icon}  {item.label}", anchor="w")

    def _collapse(self):
        self._expanded = False
        self.config(width=self.COLLAPSED_W)
        self._toggle_btn.config(text="▶")

        self._logo_label.config(text="")
        self._footer_label.config(text="")

        for item in self._items:
            item.btn.config(text=f"  {item.icon}", anchor="center")

    def _handle_click(self, index: int):
        self.set_active(index)
        item = self._items[index]
        if item.command:
            item.command()

    def _on_hover_enter(self, btn: tk.Button):
        if btn.cget("bg") != theme.SIDEBAR_ACTIVE:
            btn.config(bg=theme.SIDEBAR_HOVER)

    def _on_hover_leave(self, btn: tk.Button, index: int):
        if index != self._active_index:
            btn.config(bg=theme.SIDEBAR_BG)
