import tkinter as tk
from tkinter import ttk, messagebox

from db_connection import DatabaseConnection
from app import theme
from app.sidebar import CollapsibleSidebar
from app.views.dashboard   import DashboardView
from app.views.tasks       import TaskMonitoringView
from app.views.resources   import ResourceManagementView
from app.views.assignments import TaskAssignmentView


class LoginFrame(tk.Frame):
    """Login page — dark navy header, white card body."""

    def __init__(self, master, app):
        super().__init__(master, bg=theme.MAIN_BG)
        self.app = app
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        self._build()

    def _build(self):
        self.master.title("Project Uno - Login")
        self.master.geometry("440x560")
        self.master.configure(bg=theme.MAIN_BG)

        # Centred card
        card = tk.Frame(self.master, bg=theme.CARD_BG, padx=44, pady=44,
                        highlightbackground=theme.CARD_BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Logo area
        logo_bar = tk.Frame(card, bg=theme.PRIMARY, width=56, height=56)
        logo_bar.pack(anchor="center", pady=(0, 12))
        logo_bar.pack_propagate(False)
        tk.Label(logo_bar, text="🏗", bg=theme.PRIMARY,
                 font=(theme.FONT_FAMILY, 22)).place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="Project Uno",
                 bg=theme.CARD_BG, fg=theme.TEXT_DARK,
                 font=(theme.FONT_FAMILY, 22, "bold")).pack(anchor="center")
        tk.Label(card, text="Construction Management",
                 bg=theme.CARD_BG, fg=theme.TEXT_MUTED,
                 font=(theme.FONT_FAMILY, 10)).pack(anchor="center", pady=(2, 24))

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Username
        tk.Label(card, text="Username", bg=theme.CARD_BG, fg=theme.TEXT_BODY,
                 font=(theme.FONT_FAMILY, 10)).pack(anchor="w")
        self.username_entry = tk.Entry(card, textvariable=self.username_var,
                                       relief="solid", bd=1,
                                       highlightthickness=1, highlightcolor=theme.PRIMARY,
                                       font=(theme.FONT_FAMILY, 11), width=28)
        self.username_entry.pack(pady=(2, 12), fill="x")

        # Password
        tk.Label(card, text="Password", bg=theme.CARD_BG, fg=theme.TEXT_BODY,
                 font=(theme.FONT_FAMILY, 10)).pack(anchor="w")
        self.password_entry = tk.Entry(card, textvariable=self.password_var, show="*",
                                       relief="solid", bd=1,
                                       highlightthickness=1, highlightcolor=theme.PRIMARY,
                                       font=(theme.FONT_FAMILY, 11), width=28)
        self.password_entry.pack(pady=(2, 20), fill="x")

        # Login button
        login_btn = tk.Button(card, text="Login",
                              bg=theme.PRIMARY, fg=theme.TEXT_WHITE,
                              activebackground=theme.ACCENT,
                              activeforeground=theme.TEXT_WHITE,
                              font=(theme.FONT_FAMILY, 11, "bold"),
                              relief="flat", cursor="hand2",
                              width=26, pady=9,
                              command=self._handle_login)
        login_btn.pack()
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg=theme.ACCENT))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg=theme.PRIMARY))

        self.username_entry.focus()
        self.username_entry.bind("<Return>", lambda e: self._handle_login())
        self.password_entry.bind("<Return>", lambda e: self._handle_login())

    def _handle_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if username == "reysosmena" and password == "Rey244456":
            self.destroy()
            self.app.show_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")



class MainFrame(tk.Frame):
    """Main application shell: dark-navy sidebar (left) + scrollable content area (right)."""

    _NAV = [
        ("📊", "Dashboard",          DashboardView),
        ("📋", "Task Monitoring",    TaskMonitoringView),
        ("👷", "Resources",          ResourceManagementView),
        ("🔗", "Task Assignment",    TaskAssignmentView),
    ]

    def __init__(self, master, app):
        super().__init__(master, bg=theme.MAIN_BG)
        self.app = app
        self.grid(row=0, column=0, sticky="nsew")
        self._current_view = None

        self._apply_styles()
        self._build()
        # Show dashboard by default
        self._navigate(0)

    def _apply_styles(self):
        style = ttk.Style()
        theme.apply_styles(style)
        self.master.title("Project Uno - Construction Manager")

    def _build(self):
        # Sidebar
        self.sidebar = CollapsibleSidebar(self, on_width_change=None)
        self.sidebar.pack(side="left", fill="y")

        # Right content pane
        self.content_pane = tk.Frame(self, bg=theme.MAIN_BG)
        self.content_pane.pack(side="left", fill="both", expand=True)
        self.content_pane.grid_rowconfigure(0, weight=1)
        self.content_pane.grid_columnconfigure(0, weight=1)

        # Register nav items
        for idx, (icon, label, _view_cls) in enumerate(self._NAV):
            self.sidebar.add_item(icon, label, lambda i=idx: self._navigate(i))

    def _navigate(self, index: int):
        """Destroy the current view and instantiate the one at *index*."""
        if self._current_view is not None:
            self._current_view.destroy()
            self._current_view = None

        self.sidebar.set_active(index)

        _icon, _label, ViewClass = self._NAV[index]

        # Dashboard gets no on_data_change (it IS the data display)
        if ViewClass is DashboardView:
            view = ViewClass(self.content_pane, db=self.app.db)
        else:
            view = ViewClass(self.content_pane, db=self.app.db,
                             on_data_change=self._on_data_change)

        view.grid(row=0, column=0, sticky="nsew")
        self._current_view = view

    def _on_data_change(self):
        """Called by any view when it mutates data — refreshes dashboard if active."""
        # Dashboard will auto-refresh next time it's navigated to (recreated).
        # If it's currently active, refresh now.
        if isinstance(self._current_view, DashboardView):
            self._current_view.refresh()


class ConstructionApp:
    """High-level application controller."""

    def __init__(self, root):
        self.root = root
        self.root.geometry("1340x820")
        self.root.minsize(900, 600)
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        try:
            self.root.wm_attributes("-alpha", 1.0)
            self.root.configure(bg=theme.MAIN_BG)
        except Exception:
            pass
        self.db = DatabaseConnection()
        self.login_frame = LoginFrame(self.root, self)
        self.main_frame = None

    def show_main_interface(self):
        if self.login_frame:
            self.login_frame.destroy()
            self.login_frame = None
        self.main_frame = MainFrame(self.root, self)

    def refresh_dashboard(self):
        """Compatibility shim — called by any code that still uses the old API."""
        if self.main_frame and isinstance(self.main_frame._current_view, DashboardView):
            self.main_frame._current_view.refresh()

    def close(self):
        try:
            self.db.close()
        except Exception:
            pass
        self.root.destroy()
