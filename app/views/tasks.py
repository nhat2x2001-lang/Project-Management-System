# app/views/tasks.py — Task Monitoring view.

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime

from app import theme
from app.widgets.treeview import ScrollableTreeview


class TaskMonitoringView(tk.Frame):
    """View for browsing, adding, editing, and deleting tasks."""

    def __init__(self, parent, db, on_data_change=None, **kwargs):
        super().__init__(parent, bg=theme.MAIN_BG, **kwargs)
        self.db             = db
        self.on_data_change = on_data_change  # callback to refresh dashboard KPIs

        self.task_id_var           = tk.StringVar()
        self.wbs_var               = tk.StringVar()
        self.task_description_var  = tk.StringVar()
        self.duration_var          = tk.StringVar()
        self.start_var             = tk.StringVar()
        self.finish_var            = tk.StringVar()
        self.predecessors_var      = tk.StringVar()
        self.search_query_var      = tk.StringVar()
        self.search_id_var         = tk.StringVar()
        self.selected_task_id      = tk.StringVar()
        self.selected_task_desc    = tk.StringVar()

        self._build()
        self.refresh_task_list()

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def _build(self):
        # Page header
        header = tk.Frame(self, bg=theme.MAIN_BG)
        header.pack(fill="x", padx=20, pady=(20, 8))
        tk.Label(header, text="Task Monitoring",
                 bg=theme.MAIN_BG, fg=theme.TEXT_DARK,
                 font=(theme.FONT_FAMILY, 20, "bold")).pack(side="left")

        # Main content area (form left | table right)
        body = tk.Frame(self, bg=theme.MAIN_BG)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        left_card = self._panel(body, "Manage Tasks")
        left_card.pack(side="left", fill="y", padx=(0, 10))

        right_card = self._panel(body, "Task List")
        right_card.pack(side="left", fill="both", expand=True)

        self._build_form(left_card)
        self._build_table(right_card)

    def _build_form(self, parent):
        f = tk.Frame(parent, bg=theme.CARD_BG)
        f.pack(fill="x", padx=14, pady=(0, 14))

        # Import button
        self._import_btn(f, "⬆  Import Tasks CSV", self.import_tasks_csv,
                         "Expected: Task ID · WBS Code · Task Discription · Duration · Start · Finish · Predecessors")

        tk.Frame(f, bg=theme.CARD_BORDER, height=1).pack(fill="x", pady=8)

        # Form fields
        fields = [
            ("Task ID",            self.task_id_var),
            ("WBS Code",           self.wbs_var),
            ("Task Description",   self.task_description_var),
            ("Duration (days)",    self.duration_var),
            ("Start (YYYY-MM-DD)", self.start_var),
            ("Finish (YYYY-MM-DD)",self.finish_var),
            ("Predecessors",       self.predecessors_var),
        ]
        for label, var in fields:
            row = tk.Frame(f, bg=theme.CARD_BG)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, bg=theme.CARD_BG, fg=theme.TEXT_BODY,
                     font=(theme.FONT_FAMILY, 9), width=18, anchor="w").pack(side="left")
            ttk.Entry(row, textvariable=var, width=26).pack(side="left", fill="x", expand=True)

        tk.Frame(f, bg=theme.CARD_BORDER, height=1).pack(fill="x", pady=8)

        # Action buttons
        self._action_btn(f, "➕  Add Task",       theme.COLOR_GREEN,  self.add_task)
        self._action_btn(f, "🗑  Delete Task",     theme.COLOR_RED,    self.remove_task)
        self._action_btn(f, "🧹  Clear All Tasks", theme.TEXT_MUTED,   self.clear_tasks)

        tk.Frame(f, bg=theme.CARD_BORDER, height=1).pack(fill="x", pady=8)

        # Search
        tk.Label(f, text="Search by Description:", bg=theme.CARD_BG, fg=theme.TEXT_MUTED,
                 font=(theme.FONT_FAMILY, 9)).pack(anchor="w")
        search_row = tk.Frame(f, bg=theme.CARD_BG)
        search_row.pack(fill="x", pady=(2, 4))
        ttk.Entry(search_row, textvariable=self.search_query_var, width=22).pack(side="left")
        ttk.Button(search_row, text="Search", command=self.search_task).pack(side="left", padx=(4, 0))

        tk.Label(f, text="Search by Task ID:", bg=theme.CARD_BG, fg=theme.TEXT_MUTED,
                 font=(theme.FONT_FAMILY, 9)).pack(anchor="w", pady=(4, 0))
        id_row = tk.Frame(f, bg=theme.CARD_BG)
        id_row.pack(fill="x", pady=(2, 4))
        ttk.Entry(id_row, textvariable=self.search_id_var, width=22).pack(side="left")
        ttk.Button(id_row, text="Search", command=self.search_task_by_id).pack(side="left", padx=(4, 0))

        # Selected task info
        tk.Frame(f, bg=theme.CARD_BORDER, height=1).pack(fill="x", pady=8)
        sel_frame = tk.Frame(f, bg=theme.CARD_BG)
        sel_frame.pack(fill="x")
        tk.Label(sel_frame, text="Selected Task ID:", bg=theme.CARD_BG, fg=theme.TEXT_MUTED,
                 font=(theme.FONT_FAMILY, 9)).pack(anchor="w")
        tk.Label(sel_frame, textvariable=self.selected_task_id,
                 bg=theme.CARD_BG, fg=theme.PRIMARY,
                 font=(theme.FONT_FAMILY, 10, "bold")).pack(anchor="w")
        tk.Label(sel_frame, text="Description:", bg=theme.CARD_BG, fg=theme.TEXT_MUTED,
                 font=(theme.FONT_FAMILY, 9)).pack(anchor="w", pady=(4, 0))
        tk.Label(sel_frame, textvariable=self.selected_task_desc,
                 bg=theme.CARD_BG, fg=theme.TEXT_BODY,
                 font=(theme.FONT_FAMILY, 9), wraplength=220, justify="left").pack(anchor="w")

    def _build_table(self, parent):
        btn_row = tk.Frame(parent, bg=theme.CARD_BG)
        btn_row.pack(fill="x", padx=14, pady=(0, 8))
        ttk.Button(btn_row, text="⟳  Refresh", command=self.refresh_task_list).pack(side="right")

        self.task_tree = ScrollableTreeview(
            parent,
            columns=["TaskID", "WBS_Code", "Task_Description", "Duration", "Start", "Finish", "Predecessors"],
            height=22,
        )
        self.task_tree.tree.column("Task_Description", width=200, minwidth=120)
        self.task_tree.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.task_tree.bind_select(self.on_task_select)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def add_task(self):
        task_id     = self.task_id_var.get().strip()
        wbs_code    = self.wbs_var.get().strip()
        description = self.task_description_var.get().strip()
        duration    = self.duration_var.get().strip()
        start       = self.start_var.get().strip()
        finish      = self.finish_var.get().strip()
        predecessors = self.predecessors_var.get().strip()

        if not task_id or not description or not wbs_code:
            messagebox.showerror("Validation Error", "Task ID, WBS Code and Task Description are required.")
            return
        if not self._validate_integer(duration, "Duration"):
            return
        if not self._validate_date(start, "Start"):
            return
        if not self._validate_date(finish, "Finish"):
            return

        try:
            self.db.execute_query(
                "INSERT INTO Task (TaskID, WBS_Code, Task_Description, Duration, Start, Finish, Predecessors) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (task_id, wbs_code, description, int(duration), start, finish, predecessors)
            )
            messagebox.showinfo("Success", "Task added successfully.")
            self._clear_form()
            self.refresh_task_list()
            self._notify_change()
        except RuntimeError as exc:
            messagebox.showerror("Insert Failed", str(exc))

    def remove_task(self):
        task_id = self.search_id_var.get().strip()
        if not task_id:
            messagebox.showerror("Validation Error", "Enter a Task ID in the Search by Task ID field first.")
            return
        try:
            self.db.execute_query("DELETE FROM Task WHERE TaskID = %s", (task_id,))
            messagebox.showinfo("Success", "Task removed successfully.")
            self.selected_task_id.set("")
            self.selected_task_desc.set("")
            self.refresh_task_list()
            self._notify_change()
        except RuntimeError as exc:
            messagebox.showerror("Delete Failed", str(exc))

    def search_task(self):
        query = self.search_query_var.get().strip()
        if not query:
            self.refresh_task_list()
            return
        try:
            rows = self.db.fetch_all(
                "SELECT * FROM Task WHERE Task_Description LIKE %s OR WBS_Code LIKE %s",
                (f"%{query}%", f"%{query}%")
            )
            self._populate(rows)
            messagebox.showinfo("Search", f"Found {len(rows)} task(s).")
        except RuntimeError as exc:
            messagebox.showerror("Search Failed", str(exc))

    def search_task_by_id(self):
        task_id = self.search_id_var.get().strip()
        if not task_id:
            messagebox.showerror("Validation Error", "Task ID is required.")
            return
        try:
            rows = self.db.fetch_all("SELECT * FROM Task WHERE TaskID = %s", (task_id,))
            if rows:
                self._populate(rows)
                self.selected_task_id.set(rows[0]["TaskID"])
                self.selected_task_desc.set(rows[0]["Task_Description"])
                messagebox.showinfo("Found", "Task found.")
            else:
                messagebox.showinfo("Not Found", "No task found with that ID.")
        except RuntimeError as exc:
            messagebox.showerror("Search Failed", str(exc))

    def refresh_task_list(self):
        try:
            rows = self.db.fetch_all("SELECT * FROM Task ORDER BY TaskID")
            self._populate(rows)
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def on_task_select(self, _event):
        values = self.task_tree.get_selected_values()
        if not values:
            return
        self.selected_task_id.set(values[0])
        self.selected_task_desc.set(values[2])
        self.search_id_var.set(values[0])

    def clear_tasks(self):
        if not messagebox.askyesno("Clear Tasks",
                                   "This will permanently delete ALL tasks. Are you sure?"):
            return
        try:
            self.db.execute_query("SET SQL_SAFE_UPDATES = 0")
            self.db.execute_query("DELETE FROM Task")
            self.db.execute_query("SET SQL_SAFE_UPDATES = 1")
            messagebox.showinfo("Success", "All tasks cleared.")
            self.refresh_task_list()
            self._notify_change()
        except Exception as exc:
            messagebox.showerror("Clear Failed", str(exc))

    def import_tasks_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select Task CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filepath:
            return
        try:
            with open(filepath, newline="", encoding="cp1252", errors="replace") as f:
                rows = list(csv.DictReader(f))
            inserted = 0
            for row in rows:
                task_id = row.get("Task ID", "").strip()
                if not task_id:
                    continue
                self.db.execute_query(
                    "INSERT INTO Task (TaskID, WBS_Code, Task_Description, Duration, Start, Finish, Predecessors) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        task_id,
                        row.get("WBS Code", ""),
                        row.get("Task Discription", row.get("Task Description", "")),
                        self._parse_duration(row.get("Duration", "0")),
                        self._parse_date(row.get("Start", "")),
                        self._parse_date(row.get("Finish", "")),
                        row.get("Predecessors", ""),
                    )
                )
                inserted += 1
            messagebox.showinfo("Import Complete", f"{inserted} task(s) imported successfully.")
            self.refresh_task_list()
            self._notify_change()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _populate(self, rows: list):
        self.task_tree.clear()
        for idx, row in enumerate(rows):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.task_tree.tree.insert("", "end", values=(
                row["TaskID"], row["WBS_Code"], row["Task_Description"],
                row["Duration"], row["Start"], row["Finish"], row["Predecessors"]
            ), tags=(tag,))

    def _clear_form(self):
        for var in (self.task_id_var, self.wbs_var, self.task_description_var,
                    self.duration_var, self.start_var, self.finish_var,
                    self.predecessors_var):
            var.set("")

    def _notify_change(self):
        if self.on_data_change:
            self.on_data_change()

    @staticmethod
    def _validate_integer(value, label):
        if not value:
            messagebox.showerror("Validation Error", f"{label} is required.")
            return False
        if not value.isdigit():
            messagebox.showerror("Validation Error", f"{label} must be a whole number.")
            return False
        return True

    @staticmethod
    def _validate_date(value, label):
        if not value:
            messagebox.showerror("Validation Error", f"{label} date is required.")
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            messagebox.showerror("Validation Error", f"{label} date must be YYYY-MM-DD.")
            return False

    @staticmethod
    def _parse_date(value):
        if not value or not value.strip():
            return None
        for fmt in ("%a %m/%d/%y", "%m/%d/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(value.strip(), fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    @staticmethod
    def _parse_duration(value):
        try:
            return round(float(str(value).replace("days", "").replace("day", "").strip()))
        except (ValueError, TypeError):
            return 0

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------

    def _panel(self, parent, title: str) -> tk.Frame:
        panel = tk.Frame(parent, bg=theme.CARD_BG,
                         highlightbackground=theme.CARD_BORDER,
                         highlightthickness=1)
        hdr = tk.Frame(panel, bg=theme.CARD_BG)
        hdr.pack(fill="x", padx=14, pady=(12, 4))
        tk.Label(hdr, text=title, bg=theme.CARD_BG, fg=theme.TEXT_DARK,
                 font=(theme.FONT_FAMILY, 11, "bold")).pack(side="left")
        tk.Frame(panel, bg=theme.CARD_BORDER, height=1).pack(fill="x", padx=10)
        return panel

    def _import_btn(self, parent, text, command, hint=""):
        btn = tk.Button(parent, text=text,
                        bg=theme.PRIMARY, fg=theme.TEXT_WHITE,
                        activebackground=theme.ACCENT,
                        activeforeground=theme.TEXT_WHITE,
                        relief="flat", cursor="hand2",
                        font=(theme.FONT_FAMILY, 9),
                        padx=10, pady=5,
                        command=command)
        btn.pack(fill="x", pady=(0, 2))
        if hint:
            tk.Label(parent, text=hint, bg=theme.CARD_BG, fg=theme.TEXT_MUTED,
                     font=(theme.FONT_FAMILY, 7), wraplength=260, justify="left").pack(anchor="w")

    def _action_btn(self, parent, text, bg_color, command):
        btn = tk.Button(parent, text=text,
                        bg=bg_color, fg=theme.TEXT_WHITE,
                        activebackground=theme.ACCENT,
                        activeforeground=theme.TEXT_WHITE,
                        relief="flat", cursor="hand2",
                        font=(theme.FONT_FAMILY, 9),
                        padx=10, pady=5,
                        command=command)
        btn.pack(fill="x", pady=2)
