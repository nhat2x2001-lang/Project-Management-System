# app/views/assignments.py — Task Assignment view.

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

from app import theme
from app.widgets.treeview import ScrollableTreeview


class TaskAssignmentView(tk.Frame):
    """View for assigning workers to tasks and managing those assignments."""

    def __init__(self, parent, db, on_data_change=None, **kwargs):
        super().__init__(parent, bg=theme.MAIN_BG, **kwargs)
        self.db             = db
        self.on_data_change = on_data_change

        self.task_var          = tk.StringVar()
        self.worker_var        = tk.StringVar()
        self.assignment_id_var = tk.StringVar()

        self._build()
        self.refresh_assignments()

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def _build(self):
        header = tk.Frame(self, bg=theme.MAIN_BG)
        header.pack(fill="x", padx=20, pady=(20, 8))
        tk.Label(header, text="Task Assignment",
                 bg=theme.MAIN_BG, fg=theme.TEXT_DARK,
                 font=(theme.FONT_FAMILY, 20, "bold")).pack(side="left")

        body = tk.Frame(self, bg=theme.MAIN_BG)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Form panel (left)
        form_panel = self._panel(body, "Assign Worker to Task")
        form_panel.pack(side="left", fill="y", padx=(0, 10))
        self._build_form(form_panel)

        # List panel (right)
        list_panel = self._panel(body, "Current Assignments")
        list_panel.pack(side="left", fill="both", expand=True)
        self._build_list(list_panel)

    def _build_form(self, parent):
        f = tk.Frame(parent, bg=theme.CARD_BG)
        f.pack(fill="x", padx=14, pady=(0, 14))

        # Task selector
        tk.Label(f, text="Task:", bg=theme.CARD_BG, fg=theme.TEXT_BODY,
                 font=(theme.FONT_FAMILY, 9)).pack(anchor="w", pady=(4, 2))
        self.task_selector = ttk.Combobox(f, textvariable=self.task_var,
                                          state="readonly", width=42)
        self.task_selector.pack(fill="x", pady=(0, 8))

        # Worker selector
        tk.Label(f, text="Worker:", bg=theme.CARD_BG, fg=theme.TEXT_BODY,
                 font=(theme.FONT_FAMILY, 9)).pack(anchor="w", pady=(0, 2))
        self.worker_selector = ttk.Combobox(f, textvariable=self.worker_var,
                                            state="readonly", width=42)
        self.worker_selector.pack(fill="x", pady=(0, 10))

        # Assign button
        assign_btn = tk.Button(
            f, text="🔗  Assign Worker",
            bg=theme.COLOR_GREEN, fg=theme.TEXT_WHITE,
            activebackground=theme.ACCENT,
            activeforeground=theme.TEXT_WHITE,
            relief="flat", cursor="hand2",
            font=(theme.FONT_FAMILY, 10, "bold"),
            padx=12, pady=7,
            command=self.add_assignment,
        )
        assign_btn.pack(fill="x", pady=(0, 10))

        tk.Frame(f, bg=theme.CARD_BORDER, height=1).pack(fill="x", pady=6)

        # Selected assignment ID
        tk.Label(f, text="Selected Assignment ID:", bg=theme.CARD_BG, fg=theme.TEXT_MUTED,
                 font=(theme.FONT_FAMILY, 9)).pack(anchor="w")
        ttk.Entry(f, textvariable=self.assignment_id_var, state="readonly",
                  width=44).pack(fill="x", pady=(2, 10))

        tk.Frame(f, bg=theme.CARD_BORDER, height=1).pack(fill="x", pady=6)

        # Control buttons
        ctrl = tk.Frame(f, bg=theme.CARD_BG)
        ctrl.pack(fill="x")

        for text, color, cmd in [
            ("⬆  Import CSV",          theme.PRIMARY,      self.import_task_assignments_csv),
            ("⟳  Refresh",              theme.COLOR_BLUE,   self.refresh_assignments),
            ("🗑  Delete Assignment",   theme.COLOR_RED,    self.delete_assignment),
        ]:
            btn = tk.Button(ctrl, text=text,
                            bg=color, fg=theme.TEXT_WHITE,
                            activebackground=theme.ACCENT,
                            activeforeground=theme.TEXT_WHITE,
                            relief="flat", cursor="hand2",
                            font=(theme.FONT_FAMILY, 9),
                            padx=10, pady=5,
                            command=cmd)
            btn.pack(fill="x", pady=2)

    def _build_list(self, parent):
        self.assignment_tree = ScrollableTreeview(
            parent,
            columns=["AssignmentID", "TaskID", "WorkerID", "WorkerName",
                     "Task_Description", "AssignedDate"],
            height=22,
        )
        self.assignment_tree.tree.column("Task_Description", width=200, minwidth=100)
        self.assignment_tree.tree.column("WorkerName", width=140, minwidth=80)
        self.assignment_tree.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.assignment_tree.bind_select(self.on_assignment_select)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def add_assignment(self):
        if not self.task_var.get() or not self.worker_var.get():
            messagebox.showerror("Validation Error", "Please select both task and worker.")
            return
        task_id   = self._parse_selection_id(self.task_var.get())
        worker_id = self._parse_selection_id(self.worker_var.get())
        if task_id is None or worker_id is None:
            messagebox.showerror("Validation Error", "Selected task or worker is malformed.")
            return
        try:
            self.db.execute_query(
                "INSERT INTO TaskAssignments (TaskID, WorkerID) VALUES (%s, %s)",
                (task_id, worker_id)
            )
            messagebox.showinfo("Success", "Worker assigned to task.")
            self.refresh_assignments()
            self._notify_change()
        except RuntimeError as exc:
            messagebox.showerror("Insert Failed", str(exc))

    def delete_assignment(self):
        assignment_id = self.assignment_id_var.get().strip()
        if not assignment_id:
            messagebox.showerror("Validation Error", "Select an assignment to delete.")
            return
        try:
            self.db.execute_query(
                "DELETE FROM TaskAssignments WHERE AssignmentID = %s",
                (int(assignment_id),)
            )
            messagebox.showinfo("Success", "Assignment deleted.")
            self.assignment_id_var.set("")
            self.refresh_assignments()
            self._notify_change()
        except RuntimeError as exc:
            messagebox.showerror("Delete Failed", str(exc))

    def refresh_assignments(self):
        self._load_task_options()
        self._load_worker_options()
        try:
            rows = self.db.fetch_all(
                "SELECT ta.AssignmentID, ta.TaskID, ta.WorkerID, w.WorkerName, "
                "t.Task_Description, ta.AssignedDate "
                "FROM TaskAssignments ta "
                "LEFT JOIN Workers w ON ta.WorkerID = w.WorkerID "
                "LEFT JOIN Task t ON ta.TaskID = t.TaskID "
                "ORDER BY ta.AssignmentID DESC"
            )
            self.assignment_tree.clear()
            for idx, row in enumerate(rows):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.assignment_tree.tree.insert("", "end", values=(
                    row["AssignmentID"], row["TaskID"], row["WorkerID"],
                    row["WorkerName"], row["Task_Description"], row["AssignedDate"],
                ), tags=(tag,))
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def on_assignment_select(self, _event):
        values = self.assignment_tree.get_selected_values()
        if values:
            self.assignment_id_var.set(values[0])

    def import_task_assignments_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select Task Assignment CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filepath:
            return
        try:
            with open(filepath, newline="", encoding="cp1252", errors="replace") as f:
                rows = list(csv.DictReader(f))

            tasks = self.db.fetch_all("SELECT TaskID, Task_Description FROM Task")
            task_desc_to_id = {t["Task_Description"].strip(): t["TaskID"] for t in tasks}

            inserted, skipped = 0, 0
            current_task_id = None

            for row in rows:
                task_desc = row.get("TASK DESCRIPTION", "").strip()
                worker_id = row.get("Worker ID", "").strip()

                if task_desc:
                    current_task_id = task_desc_to_id.get(task_desc)

                if not worker_id or not current_task_id:
                    skipped += 1
                    continue

                try:
                    self.db.execute_query(
                        "INSERT IGNORE INTO TaskAssignments (TaskID, WorkerID) VALUES (%s, %s)",
                        (current_task_id, worker_id)
                    )
                    inserted += 1
                except Exception:
                    skipped += 1

            messagebox.showinfo(
                "Import Complete",
                f"{inserted} assignment(s) imported.\n{skipped} rows skipped."
            )
            self.refresh_assignments()
            self._notify_change()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_task_options(self):
        try:
            rows = self.db.fetch_all("SELECT TaskID, Task_Description FROM Task ORDER BY TaskID")
            self.task_selector["values"] = [f"{r['TaskID']} - {r['Task_Description']}" for r in rows]
            if rows and not self.task_var.get():
                self.task_var.set(self.task_selector["values"][0])
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def _load_worker_options(self):
        try:
            rows = self.db.fetch_all("SELECT WorkerID, WorkerName FROM Workers ORDER BY WorkerID")
            self.worker_selector["values"] = [f"{r['WorkerID']} - {r['WorkerName']}" for r in rows]
            if rows and not self.worker_var.get():
                self.worker_var.set(self.worker_selector["values"][0])
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def _notify_change(self):
        if self.on_data_change:
            self.on_data_change()

    @staticmethod
    def _parse_selection_id(selection: str):
        if " - " not in selection:
            return None
        return selection.split(" - ", 1)[0].strip()

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
