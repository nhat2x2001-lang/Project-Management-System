import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv

from db_connection import DatabaseConnection


class LoginFrame(ttk.Frame):
    """Login page with blue and white theme."""

    def __init__(self, master, app):
        super().__init__(master, padding=20)
        self.app = app
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        self._build_login_form()

    def _build_login_form(self):
        self.master.title("Project Uno - Login")
        self.master.geometry("400x500")
        self.master.configure(bg="#f0f4f8")

        # Create centered card
        card_frame = tk.Frame(self.master, bg="white", padx=40, pady=40, relief="flat",
                              highlightbackground="#d0d7e2", highlightthickness=1)
        card_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title_label = tk.Label(card_frame, text="Project Uno", bg="white", fg="#1a3a5c",
                               font=("Segoe UI", 20, "bold"))
        title_label.pack(anchor="center")

        # Subtitle
        subtitle_label = tk.Label(card_frame, text="Construction Management", bg="white", fg="#6b7a8d",
                                  font=("Segoe UI", 10))
        subtitle_label.pack(anchor="center", pady=(0, 24))

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Username field
        username_label = tk.Label(card_frame, text="Username", bg="white", fg="#374151",
                                  font=("Segoe UI", 10))
        username_label.pack(anchor="w")
        self.username_entry = tk.Entry(card_frame, textvariable=self.username_var, relief="solid", bd=1,
                                        highlightthickness=1, highlightcolor="#1f4e79",
                                        font=("Segoe UI", 11), width=28)
        self.username_entry.pack(pady=(0, 12), fill="x")

        # Password field
        password_label = tk.Label(card_frame, text="Password", bg="white", fg="#374151",
                                  font=("Segoe UI", 10))
        password_label.pack(anchor="w")
        self.password_entry = tk.Entry(card_frame, textvariable=self.password_var, show="*", relief="solid", bd=1,
                                        highlightthickness=1, highlightcolor="#1f4e79",
                                        font=("Segoe UI", 11), width=28)
        self.password_entry.pack(pady=(0, 12), fill="x")

        # Login button with hover effect
        login_button = tk.Button(card_frame, text="Login", bg="#1f4e79", fg="white",
                                 font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
                                 width=26, pady=8, command=self._handle_login)
        login_button.pack(pady=(16, 0))

        # Hover effects
        def on_enter(e):
            login_button.config(bg="#163a61")
        def on_leave(e):
            login_button.config(bg="#1f4e79")
        login_button.bind("<Enter>", on_enter)
        login_button.bind("<Leave>", on_leave)

        self.username_entry.focus()
        self.username_entry.bind("<Return>", lambda event: self._handle_login())
        self.password_entry.bind("<Return>", lambda event: self._handle_login())

    def _handle_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if username == "reysosmena" and password == "Rey244456":
            self.destroy()
            self.app.show_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


class DashboardTab(ttk.Frame):
    """Dashboard tab displaying the four main tables with search support."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.search_var = tk.StringVar()
        self._build_dashboard()
        self.refresh_all_tables()

    def _build_dashboard(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=10)

        ttk.Label(top_frame, text="Dashboard", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)

        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side="right", padx=10)
        ttk.Label(search_frame, text="Search Tasks:").pack(side="left")
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side="left", padx=(5, 5))
        search_entry.bind("<Return>", lambda event: self.search_tasks())
        ttk.Button(search_frame, text="Search", command=self.search_tasks).pack(side="left")
        ttk.Button(search_frame, text="Refresh", command=self.refresh_all_tables).pack(side="left", padx=(5, 0))

        # Canvas with scrollbar for table_container
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.table_container = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=self.table_container, anchor="nw")

        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.table_container.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Material Assignment and Cost
        mac_frame = ttk.LabelFrame(self.table_container, text="Material Assignment and Cost")
        mac_frame.pack(fill="both", expand=True, padx=10, pady=5)
        mac_btn_frame = ttk.Frame(mac_frame)
        mac_btn_frame.pack(fill="x", padx=5, pady=(4, 2))
        ttk.Button(mac_btn_frame, text="⬆ Import CSV", command=self.import_assignment_cost_csv).pack(side="left")
        ttk.Label(mac_btn_frame,
            text="  Expected: Task Description · Materials · Quantity · Unit · Unit Price · Budget Cost",
            font=("Segoe UI", 8), foreground="#6b7a8d").pack(side="left", padx=(6, 0))
        self.assignment_costs_tree = self._create_treeview_in(
            mac_frame, ["ForemanID", "Task_Description", "Materials", "Quantity", "Unit", "UnitPrice", "BudgetCost"])

        # Materials Usage
        mu_frame = ttk.LabelFrame(self.table_container, text="Materials Usage")
        mu_frame.pack(fill="both", expand=True, padx=10, pady=5)
        mu_btn_frame = ttk.Frame(mu_frame)
        mu_btn_frame.pack(fill="x", padx=5, pady=(4, 2))
        ttk.Button(mu_btn_frame, text="⬆ Import CSV", command=self.import_materials_usage_csv).pack(side="left")
        ttk.Label(mu_btn_frame,
            text="  Expected: TASK ID · MATERIAL ID · MATERIALS · QUANTITY · Unit · Cost",
            font=("Segoe UI", 8), foreground="#6b7a8d").pack(side="left", padx=(6, 0))
        self.materials_usage_tree = self._create_treeview_in(
            mu_frame, ["UsageID", "TaskID", "MaterialID", "Materials", "Quantity", "Unit", "Cost"])

        self.materials_tree = self._create_treeview(
            "Materials",
            ["MaterialID", "Materials", "Quantity", "Unit", "Cost"]
        )
        self.tasks_tree = self._create_treeview(
            "Task",
            ["TaskID", "WBS_Code", "Task_Description", "Duration", "Start", "Finish", "Predecessors"]
        )
        self.workers_tree = self._create_treeview(
            "Workers",
            ["WorkerID", "WorkerName", "Position"]
        )
        self.assignments_tree = self._create_treeview(
            "Task Assignments",
            ["AssignmentID", "TaskID", "WorkerID", "WorkerName", "Task_Description", "AssignedDate"]
        )

    def _create_treeview(self, title, columns):
        frame = ttk.LabelFrame(self.table_container, text=title)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse", height=6)
        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for column in columns:
            tree.heading(column, text=column.replace("_", " "))
            tree.column(column, width=120, anchor="center")
        return tree

    def _create_treeview_in(self, parent_frame, columns):
        """Create a treeview in an existing parent frame without creating a LabelFrame."""
        container = ttk.Frame(parent_frame)
        container.pack(fill="both", expand=True)

        tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse", height=6)
        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for column in columns:
            tree.heading(column, text=column.replace("_", " "))
            tree.column(column, width=120, anchor="center")
        return tree

    def refresh_all_tables(self):
        self._load_assignment_costs()
        self._load_materials_usage()
        self._load_materials()
        self._load_tasks()
        self._load_workers()
        self._load_assignments()

    def search_tasks(self):
        query = self.search_var.get().strip()
        if not query:
            self.refresh_all_tables()
            return
        search_string = f"%{query}%"
        try:
            rows = self.app.db.fetch_all(
                "SELECT * FROM Task WHERE Task_Description LIKE %s OR WBS_Code LIKE %s",
                (search_string, search_string)
            )
            self._populate_tree(self.tasks_tree, rows)
            messagebox.showinfo("Search Complete", f"Found {len(rows)} task(s) matching '{query}'.")
        except RuntimeError as exc:
            messagebox.showerror("Search Failed", str(exc))

    def _populate_tree(self, tree, rows):
        tree.delete(*tree.get_children())
        columns = tree["columns"]
        for row in rows:
            tree.insert("", "end", values=tuple(row[col] for col in columns))

    def _load_assignment_costs(self):
        try:
            rows = self.app.db.fetch_all("SELECT * FROM MaterialAssignmentCost")
            self._populate_tree(self.assignment_costs_tree, rows)
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def _load_materials_usage(self):
        try:
            rows = self.app.db.fetch_all("SELECT * FROM MaterialsUsage")
            self._populate_tree(self.materials_usage_tree, rows)
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def _load_materials(self):
        try:
            rows = self.app.db.fetch_all("SELECT * FROM Materials")
            self._populate_tree(self.materials_tree, rows)
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def _load_tasks(self):
        try:
            rows = self.app.db.fetch_all("SELECT * FROM Task")
            self._populate_tree(self.tasks_tree, rows)
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def _load_workers(self):
        try:
            rows = self.app.db.fetch_all("SELECT * FROM Workers")
            self._populate_tree(self.workers_tree, rows)
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def _load_assignments(self):
        try:
            rows = self.app.db.fetch_all(
                "SELECT ta.AssignmentID, ta.TaskID, ta.WorkerID, w.WorkerName, t.Task_Description, ta.AssignedDate "
                "FROM TaskAssignments ta "
                "LEFT JOIN Workers w ON ta.WorkerID = w.WorkerID "
                "LEFT JOIN Task t ON ta.TaskID = t.TaskID"
            )
            self._populate_tree(self.assignments_tree, rows)
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    @staticmethod
    def _parse_float(value):
        try:
            return float(str(value).replace(",", "").strip())
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _parse_int(value):
        try:
            return int(str(value).replace(",", "").strip())
        except (ValueError, TypeError):
            return 0

    def import_assignment_cost_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select Material Assignment Cost CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filepath:
            return
        try:
            with open(filepath, newline="", encoding="cp1252", errors="replace") as f:
                rows = list(csv.DictReader(f))
            inserted = 0
            for row in rows:
                self.app.db.execute_query(
                    "INSERT INTO MaterialAssignmentCost "
                    "(ForemanID, Task_Description, Materials, Quantity, Unit, UnitPrice, BudgetCost) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        row.get("ForemanID", row.get("Foreman ID", "")).strip(),
                        row.get("Task Description", "").strip(),
                        row.get("Materials", "").strip(),
                        self._parse_float(row.get("Quantity", "0")),
                        row.get("Unit", "").strip(),
                        self._parse_float(row.get("Unit Price", "0")),
                        self._parse_float(row.get("Budget Cost", "0")),
                    )
                )
                inserted += 1
            messagebox.showinfo("Import Complete", f"{inserted} record(s) imported successfully.")
            self.refresh_all_tables()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))

    def import_materials_usage_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select Materials Usage CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filepath:
            return
        try:
            with open(filepath, newline="", encoding="cp1252", errors="replace") as f:
                rows = list(csv.DictReader(f))
            inserted = 0
            for row in rows:
                self.app.db.execute_query(
                    "INSERT INTO MaterialsUsage (TaskID, MaterialID, Materials, Quantity, Unit, Cost) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        row.get("TASK ID", "").strip(),
                        self._parse_int(row.get("MATERIAL ID", "0")),
                        row.get("MATERIALS", "").strip(),
                        self._parse_float(row.get("QUANTITY", "0")),
                        row.get("Unit", "").strip(),
                        self._parse_float(row.get("Cost", "0")),
                    )
                )
                inserted += 1
            messagebox.showinfo("Import Complete", f"{inserted} record(s) imported successfully.")
            self.refresh_all_tables()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))


class TaskMonitoringTab(ttk.Frame):
    """Task monitoring tab with add, search, and remove capabilities."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_task_id = tk.StringVar()
        self.selected_task_description = tk.StringVar()
        self._build_task_monitoring()
        self.refresh_task_list()

    def _build_task_monitoring(self):
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", pady=10)
        ttk.Label(title_frame, text="Task Monitoring", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)

        left_frame = ttk.LabelFrame(self, text="Add New Task")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.task_id_var = tk.StringVar()
        self.wbs_var = tk.StringVar()
        self.task_description_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.start_var = tk.StringVar()
        self.finish_var = tk.StringVar()
        self.predecessors_var = tk.StringVar()
        self.search_query_var = tk.StringVar()
        self.search_id_var = tk.StringVar()

        self._build_task_form(left_frame)

        right_frame = ttk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self._build_task_list(right_frame)

    def _build_task_form(self, frame):
        ttk.Button(frame, text="⬆ Import Tasks CSV", command=self.import_tasks_csv).grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 0))
        ttk.Label(frame, text="Expected columns: WBS Code · Task Discription · Duration · Start · Finish · Predecessors",
            font=("Segoe UI", 8), foreground="#6b7a8d").grid(row=1, column=0, columnspan=2, pady=(0, 8))

        labels = ["Task ID", "WBS Code", "Task Description", "Duration", "Start (YYYY-MM-DD)", "Finish (YYYY-MM-DD)", "Predecessors"]
        variables = [self.task_id_var, self.wbs_var, self.task_description_var, self.duration_var, self.start_var, self.finish_var, self.predecessors_var]
        for index, (label, var) in enumerate(zip(labels, variables), start=2):
            ttk.Label(frame, text=label).grid(row=index, column=0, sticky="e", pady=5, padx=5)
            ttk.Entry(frame, textvariable=var, width=30).grid(row=index, column=1, sticky="w", pady=5)

        ttk.Button(frame, text="Add Task", command=self.add_task).grid(row=9, column=0, columnspan=2, pady=10)
        ttk.Separator(frame, orient="horizontal").grid(row=10, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(frame, text="Search by Description:").grid(row=11, column=0, sticky="e", pady=5)
        ttk.Entry(frame, textvariable=self.search_query_var, width=30).grid(row=11, column=1, sticky="w", pady=5)
        ttk.Button(frame, text="Search Task", command=self.search_task).grid(row=12, column=0, columnspan=2, pady=5)
        ttk.Label(frame, text="Search by Task ID:").grid(row=13, column=0, sticky="e", pady=5)
        ttk.Entry(frame, textvariable=self.search_id_var, width=30).grid(row=13, column=1, sticky="w", pady=5)
        ttk.Button(frame, text="Search Task ID", command=self.search_task_by_id).grid(row=14, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Delete Task", command=self.remove_task).grid(row=15, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Clear All Tasks", command=self.clear_tasks).grid(row=16, column=0, columnspan=2, pady=(2, 5), sticky="ew", padx=5)

        status_frame = ttk.LabelFrame(frame, text="Selected Task")
        status_frame.grid(row=17, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(status_frame, text="Task ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(status_frame, textvariable=self.selected_task_id).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(status_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(status_frame, textvariable=self.selected_task_description).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def _build_task_list(self, frame):
        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        self.task_tree = ttk.Treeview(container, columns=["TaskID", "WBS_Code", "Task_Description", "Duration", "Start", "Finish", "Predecessors"], show="headings", height=16)
        for column in self.task_tree["columns"]:
            self.task_tree.heading(column, text=column.replace("_", " "))
            self.task_tree.column(column, width=120, anchor="center")

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.task_tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.task_tree.xview)
        self.task_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.task_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.task_tree.bind("<<TreeviewSelect>>", self.on_task_select)

    def add_task(self):
        task_id = self.task_id_var.get().strip()
        task_description = self.task_description_var.get().strip()
        wbs_code = self.wbs_var.get().strip()
        duration = self.duration_var.get().strip()
        start_date = self.start_var.get().strip()
        finish_date = self.finish_var.get().strip()
        predecessors = self.predecessors_var.get().strip()

        if not task_id or not task_description or not wbs_code:
            messagebox.showerror("Validation Error", "Task ID, WBS Code and Task Description are required.")
            return
        if not self._validate_integer(duration, "Duration"):
            return
        if not self._validate_date(start_date, "Start"):
            return
        if not self._validate_date(finish_date, "Finish"):
            return

        try:
            self.app.db.execute_query(
                "INSERT INTO Task (TaskID, WBS_Code, Task_Description, Duration, Start, Finish, Predecessors) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (task_id, wbs_code, task_description, int(duration), start_date, finish_date, predecessors)
            )
            messagebox.showinfo("Success", "Task added successfully.")
            self._clear_task_form()
            self.refresh_task_list()
            self.app.refresh_dashboard()
        except RuntimeError as exc:
            messagebox.showerror("Insert Failed", str(exc))

    def search_task(self):
        query = self.search_query_var.get().strip()
        if not query:
            self.refresh_task_list()
            return
        try:
            rows = self.app.db.fetch_all(
                "SELECT * FROM Task WHERE Task_Description LIKE %s OR WBS_Code LIKE %s",
                (f"%{query}%", f"%{query}%")
            )
            self._populate_task_tree(rows)
            messagebox.showinfo("Search Complete", f"Found {len(rows)} task(s).")
        except RuntimeError as exc:
            messagebox.showerror("Search Failed", str(exc))

    def search_task_by_id(self):
        task_id = self.search_id_var.get().strip()
        if not task_id:
            messagebox.showerror("Validation Error", "Task ID is required.")
            return
        try:
            rows = self.app.db.fetch_all("SELECT * FROM Task WHERE TaskID = %s", (task_id,))
            if rows:
                self._populate_task_tree(rows)
                self.selected_task_id.set(rows[0]["TaskID"])
                self.selected_task_description.set(rows[0]["Task_Description"])
                messagebox.showinfo("Search Complete", "Task found.")
            else:
                messagebox.showinfo("Search Complete", "No task found with that ID.")
        except RuntimeError as exc:
            messagebox.showerror("Search Failed", str(exc))

    def remove_task(self):
        task_id = self.search_id_var.get().strip()
        if not task_id:
            messagebox.showerror("Validation Error", "Task ID is required.")
            return
        try:
            self.app.db.execute_query("DELETE FROM Task WHERE TaskID = %s", (task_id,))
            messagebox.showinfo("Success", "Task removed successfully.")
            self.refresh_task_list()
            self.app.refresh_dashboard()
            self.selected_task_id.set("")
            self.selected_task_description.set("")
        except RuntimeError as exc:
            messagebox.showerror("Delete Failed", str(exc))

    def refresh_task_list(self):
        try:
            rows = self.app.db.fetch_all("SELECT * FROM Task")
            self._populate_task_tree(rows)
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def on_task_select(self, event):
        selected = self.task_tree.selection()
        if not selected:
            return
        values = self.task_tree.item(selected[0], "values")
        self.selected_task_id.set(values[0])
        self.selected_task_description.set(values[2])
        self.search_id_var.set(values[0])

    def _populate_task_tree(self, rows):
        self.task_tree.delete(*self.task_tree.get_children())
        for row in rows:
            self.task_tree.insert("", "end", values=(
                row["TaskID"],
                row["WBS_Code"],
                row["Task_Description"],
                row["Duration"],
                row["Start"],
                row["Finish"],
                row["Predecessors"]
            ))

    def _validate_integer(self, value, label):
        if not value:
            messagebox.showerror("Validation Error", f"{label} is required.")
            return False
        if not value.isdigit():
            messagebox.showerror("Validation Error", f"{label} must be a whole number.")
            return False
        return True

    def _validate_date(self, value, label):
        if not value:
            messagebox.showerror("Validation Error", f"{label} date is required.")
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            messagebox.showerror("Validation Error", f"{label} date must be YYYY-MM-DD.")
            return False

    def _clear_task_form(self):
        self.task_id_var.set("")
        self.wbs_var.set("")
        self.task_description_var.set("")
        self.duration_var.set("")
        self.start_var.set("")
        self.finish_var.set("")
        self.predecessors_var.set("")

    @staticmethod
    def _parse_float(value):
        try:
            return float(str(value).replace(",", "").strip())
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _parse_int(value):
        try:
            return int(str(value).replace(",", "").strip())
        except (ValueError, TypeError):
            return 0

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

    def clear_tasks(self):
        confirm = messagebox.askyesno(
            "Clear Tasks",
            "This will permanently delete ALL tasks. Are you sure?"
        )
        if not confirm:
            return
        try:
            self.app.db.execute_query("SET SQL_SAFE_UPDATES = 0")
            self.app.db.execute_query("DELETE FROM Task")
            self.app.db.execute_query("SET SQL_SAFE_UPDATES = 1")
            messagebox.showinfo("Success", "All tasks cleared.")
            self.refresh_task_list()
            self.app.refresh_dashboard()
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
                reader = csv.DictReader(f)
                rows = list(reader)

            inserted = 0
            for row in rows:
                task_id = row.get("Task ID", "").strip()
                if not task_id:
                    continue
                self.app.db.execute_query(
                    "INSERT INTO Task (TaskID, WBS_Code, Task_Description, Duration, Start, Finish, Predecessors) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        task_id,
                        row.get("WBS Code", ""),
                        row.get("Task Discription", ""),
                        self._parse_duration(row.get("Duration", "0")),
                        self._parse_date(row.get("Start", "")),
                        self._parse_date(row.get("Finish", "")),
                        row.get("Predecessors", ""),
                    )
                )
                inserted += 1

            messagebox.showinfo("Import Complete", f"{inserted} task(s) imported successfully.")
            self.refresh_task_list()
            self.app.refresh_dashboard()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))


class ResourceManagementTab(ttk.Frame):
    """Resource management tab for workers and materials."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.worker_id_var = tk.StringVar()
        self.worker_name_var = tk.StringVar()
        self.position_var = tk.StringVar()
        self._build_resource_management()
        self.load_workers()
        self.load_materials()

    def _build_resource_management(self):
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", pady=10)
        ttk.Label(title_frame, text="Resource Management", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)

        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = ttk.LabelFrame(content_frame, text="Workers")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self._build_worker_form(left_frame)

        right_frame = ttk.LabelFrame(content_frame, text="Materials Overview")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self._build_material_tree(right_frame)

    def _build_worker_form(self, frame):
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=(4, 2))
        ttk.Button(btn_frame, text="⬆ Import Workers CSV", command=self.import_workers_csv).pack(side="left")
        ttk.Label(btn_frame, text="  Expected: Worker ID · Name · Resource Names",
            font=("Segoe UI", 8), foreground="#6b7a8d").pack(side="left", padx=(6, 0))

        worker_container = ttk.Frame(frame)
        worker_container.pack(fill="both", expand=True)

        self.workers_tree = ttk.Treeview(worker_container, columns=["WorkerID", "WorkerName", "Position"], show="headings", height=12)
        for column in self.workers_tree["columns"]:
            self.workers_tree.heading(column, text=column.replace("_", " "))
            self.workers_tree.column(column, width=120, anchor="center")

        workers_vsb = ttk.Scrollbar(worker_container, orient="vertical", command=self.workers_tree.yview)
        self.workers_tree.configure(yscrollcommand=workers_vsb.set)
        self.workers_tree.grid(row=0, column=0, sticky="nsew")
        workers_vsb.grid(row=0, column=1, sticky="ns")
        worker_container.grid_rowconfigure(0, weight=1)
        worker_container.grid_columnconfigure(0, weight=1)
        self.workers_tree.bind("<<TreeviewSelect>>", self.on_worker_select)

        form_frame = ttk.Frame(frame)
        form_frame.pack(fill="x", pady=10)
        ttk.Label(form_frame, text="Worker ID:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(form_frame, textvariable=self.worker_id_var, width=18, state="readonly").grid(row=0, column=1, padx=5, pady=3)
        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(form_frame, textvariable=self.worker_name_var, width=18).grid(row=1, column=1, padx=5, pady=3)
        ttk.Label(form_frame, text="Position:").grid(row=2, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(form_frame, textvariable=self.position_var, width=18).grid(row=2, column=1, padx=5, pady=3)

        ttk.Button(frame, text="Add Worker", command=self.add_worker).pack(fill="x", padx=5, pady=(5, 2))
        ttk.Button(frame, text="Update Worker", command=self.update_worker).pack(fill="x", padx=5, pady=(2, 2))
        ttk.Button(frame, text="Remove Worker", command=self.remove_worker).pack(fill="x", padx=5, pady=(2, 5))
        ttk.Button(frame, text="Clear All Workers", command=self.clear_workers).pack(fill="x", padx=5, pady=(2, 5))

    def _build_material_tree(self, frame):
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=(4, 2))
        ttk.Button(btn_frame, text="⬆ Import Materials CSV", command=self.import_materials_csv).pack(side="left")
        ttk.Label(btn_frame, text="  Expected: MATERIAL ID · MATERIALS · QUANTITY · Unit · Cost",
            font=("Segoe UI", 8), foreground="#6b7a8d").pack(side="left", padx=(6, 0))

        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        self.materials_tree = ttk.Treeview(container, columns=["MaterialID", "Materials", "Quantity", "Unit", "Cost"], show="headings", height=20)
        for column in self.materials_tree["columns"]:
            self.materials_tree.heading(column, text=column.replace("_", " "))
            self.materials_tree.column(column, width=120, anchor="center")

        materials_vsb = ttk.Scrollbar(container, orient="vertical", command=self.materials_tree.yview)
        materials_hsb = ttk.Scrollbar(container, orient="horizontal", command=self.materials_tree.xview)
        self.materials_tree.configure(yscrollcommand=materials_vsb.set, xscrollcommand=materials_hsb.set)

        self.materials_tree.grid(row=0, column=0, sticky="nsew")
        materials_vsb.grid(row=0, column=1, sticky="ns")
        materials_hsb.grid(row=1, column=0, sticky="ew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

    def load_workers(self):
        try:
            rows = self.app.db.fetch_all("SELECT * FROM Workers")
            self.workers_tree.delete(*self.workers_tree.get_children())
            for row in rows:
                self.workers_tree.insert("", "end", values=(row["WorkerID"], row["WorkerName"], row["Position"]))
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def load_materials(self):
        try:
            rows = self.app.db.fetch_all("SELECT * FROM Materials")
            self.materials_tree.delete(*self.materials_tree.get_children())
            for row in rows:
                self.materials_tree.insert("", "end", values=(
                    row["MaterialID"],
                    row["Materials"],
                    row["Quantity"],
                    row["Unit"],
                    row["Cost"]
                ))
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def clear_workers(self):
        confirm = messagebox.askyesno(
            "Clear Workers",
            "This will permanently delete ALL workers. Are you sure?"
        )
        if not confirm:
            return
        try:
            self.app.db.execute_query("SET SQL_SAFE_UPDATES = 0")
            self.app.db.execute_query("DELETE FROM Workers")
            self.app.db.execute_query("SET SQL_SAFE_UPDATES = 1")
            messagebox.showinfo("Success", "All workers cleared.")
            self.load_workers()
            self.app.refresh_dashboard()
        except Exception as exc:
            messagebox.showerror("Clear Failed", str(exc))

    def clear_materials(self):
        confirm = messagebox.askyesno(
            "Clear Materials",
            "This will permanently delete ALL materials. Are you sure?"
        )
        if not confirm:
            return
        try:
            self.app.db.execute_query("SET SQL_SAFE_UPDATES = 0")
            self.app.db.execute_query("DELETE FROM Materials WHERE MaterialID > 0")
            self.app.db.execute_query("ALTER TABLE Materials AUTO_INCREMENT = 1")
            self.app.db.execute_query("SET SQL_SAFE_UPDATES = 1")
            messagebox.showinfo("Success", "All materials cleared.")
            self.load_materials()
            self.app.refresh_dashboard()
        except Exception as exc:
            messagebox.showerror("Clear Failed", str(exc))

    def on_worker_select(self, event):
        selected = self.workers_tree.selection()
        if not selected:
            return
        values = self.workers_tree.item(selected[0], "values")
        self.worker_id_var.set(values[0])
        self.worker_name_var.set(values[1])
        self.position_var.set(values[2])

    def add_worker(self):
        name = self.worker_name_var.get().strip()
        position = self.position_var.get().strip()
        if not name or not position:
            messagebox.showerror("Validation Error", "Name and position are required.")
            return
        try:
            self.app.db.execute_query(
                "INSERT INTO Workers (WorkerName, Position) VALUES (%s, %s)",
                (name, position)
            )
            messagebox.showinfo("Success", "Worker added successfully.")
            self._clear_worker_form()
            self.load_workers()
            self.app.refresh_dashboard()
        except RuntimeError as exc:
            messagebox.showerror("Insert Failed", str(exc))

    def update_worker(self):
        worker_id = self.worker_id_var.get().strip()
        name = self.worker_name_var.get().strip()
        position = self.position_var.get().strip()
        if not worker_id or not name or not position:
            messagebox.showerror("Validation Error", "Worker ID, name, and position are required.")
            return
        try:
            self.app.db.execute_query(
                "UPDATE Workers SET WorkerName = %s, Position = %s WHERE WorkerID = %s",
                (name, position, worker_id)
            )
            messagebox.showinfo("Success", "Worker information updated.")
            self.load_workers()
            self.app.refresh_dashboard()
        except RuntimeError as exc:
            messagebox.showerror("Update Failed", str(exc))

    def remove_worker(self):
        worker_id = self.worker_id_var.get().strip()
        if not worker_id:
            messagebox.showerror("Validation Error", "Select a worker to remove.")
            return
        try:
            self.app.db.execute_query("DELETE FROM Workers WHERE WorkerID = %s", (worker_id,))
            messagebox.showinfo("Success", "Worker removed successfully.")
            self._clear_worker_form()
            self.load_workers()
            self.app.refresh_dashboard()
        except RuntimeError as exc:
            messagebox.showerror("Delete Failed", str(exc))

    def _clear_worker_form(self):
        self.worker_id_var.set("")
        self.worker_name_var.set("")
        self.position_var.set("")

    @staticmethod
    def _parse_float(value):
        try:
            return float(str(value).replace(",", "").strip())
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _parse_int(value):
        try:
            return int(str(value).replace(",", "").strip())
        except (ValueError, TypeError):
            return 0

    def import_workers_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select Workers CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filepath:
            return
        try:
            with open(filepath, newline="", encoding="cp1252", errors="replace") as f:
                rows = list(csv.DictReader(f))

            seen_ids = set()
            inserted = 0
            skipped = 0
            for row in rows:
                worker_id = row.get("Worker ID", "").strip()
                name = row.get("Name", "").strip()
                position = row.get("Resource Names", "").strip()

                if not worker_id or not name:
                    skipped += 1
                    continue
                if worker_id in seen_ids:
                    skipped += 1
                    continue
                seen_ids.add(worker_id)

                self.app.db.execute_query(
                    "INSERT IGNORE INTO Workers (WorkerID, WorkerName, Position) VALUES (%s, %s, %s)",
                    (worker_id, name, position)
                )
                inserted += 1

            messagebox.showinfo(
                "Import Complete",
                f"{inserted} unique worker(s) imported.\n{skipped} duplicate/empty rows skipped."
            )
            self.load_workers()
            self.app.refresh_dashboard()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))

    def import_materials_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select Materials CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filepath:
            return
        try:
            with open(filepath, newline="", encoding="cp1252", errors="replace") as f:
                rows = list(csv.DictReader(f))

            inserted = 0
            skipped = 0
            for row in rows:
                material_id = self._parse_int(row.get("MATERIAL ID", "0"))
                name = row.get("MATERIALS", "").strip()

                if not material_id or not name:
                    skipped += 1
                    continue

                self.app.db.execute_query(
                    "INSERT IGNORE INTO Materials (MaterialID, Materials, Quantity, Unit, Cost) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (
                        material_id,
                        name,
                        self._parse_float(row.get("QUANTITY", "0")),
                        row.get("Unit", "").strip(),
                        self._parse_float(row.get("Cost", "0")),
                    )
                )
                inserted += 1

            messagebox.showinfo(
                "Import Complete",
                f"{inserted} material(s) imported.\n{skipped} empty rows skipped."
            )
            self.load_materials()
            self.app.refresh_dashboard()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))


class TaskAssignmentTab(ttk.Frame):
    """Task assignment page where workers are assigned to tasks."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.task_var = tk.StringVar()
        self.worker_var = tk.StringVar()
        self.assignment_id_var = tk.StringVar()
        self._build_task_assignment()
        self.refresh_assignments()

    def _build_task_assignment(self):
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", pady=10)
        ttk.Label(title_frame, text="Task Assignment", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)

        form_frame = ttk.LabelFrame(self, text="Assign Worker to Task")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Task:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.task_selector = ttk.Combobox(form_frame, textvariable=self.task_var, state="readonly", width=45)
        self.task_selector.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(form_frame, text="Worker:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.worker_selector = ttk.Combobox(form_frame, textvariable=self.worker_var, state="readonly", width=45)
        self.worker_selector.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(form_frame, text="Assign Worker", command=self.add_assignment).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Label(form_frame, text="Selected Assignment ID:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.assignment_id_var, width=47, state="readonly").grid(row=3, column=1, sticky="w", padx=5, pady=5)

        control_frame = ttk.Frame(form_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(5, 0))
        ttk.Button(control_frame, text="⬆ Import CSV", command=self.import_task_assignments_csv).pack(side="left", padx=(0, 10))
        ttk.Button(control_frame, text="Refresh Assignments", command=self.refresh_assignments).pack(side="left", padx=(0, 10))
        ttk.Button(control_frame, text="Delete Assignment", command=self.delete_assignment).pack(side="left")

        list_frame = ttk.LabelFrame(self, text="Current Assignments")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        container = ttk.Frame(list_frame)
        container.pack(fill="both", expand=True)

        columns = ["AssignmentID", "TaskID", "WorkerID", "WorkerName", "Task_Description", "AssignedDate"]
        self.assignment_tree = ttk.Treeview(container, columns=columns, show="headings", height=16)
        for column in columns:
            self.assignment_tree.heading(column, text=column.replace("_", " "))
            self.assignment_tree.column(column, width=140, anchor="center")

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.assignment_tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.assignment_tree.xview)
        self.assignment_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.assignment_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.assignment_tree.bind("<<TreeviewSelect>>", self.on_assignment_select)

    def load_task_options(self):
        try:
            rows = self.app.db.fetch_all("SELECT TaskID, Task_Description FROM Task ORDER BY TaskID")
            self.task_selector["values"] = [f"{row['TaskID']} - {row['Task_Description']}" for row in rows]
            self.task_var.set(self.task_selector["values"][0] if rows else "")
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def load_worker_options(self):
        try:
            rows = self.app.db.fetch_all("SELECT WorkerID, WorkerName FROM Workers ORDER BY WorkerID")
            self.worker_selector["values"] = [f"{row['WorkerID']} - {row['WorkerName']}" for row in rows]
            self.worker_var.set(self.worker_selector["values"][0] if rows else "")
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def add_assignment(self):
        if not self.task_var.get() or not self.worker_var.get():
            messagebox.showerror("Validation Error", "Please select both task and worker.")
            return

        task_id = self._parse_selection_id(self.task_var.get())
        worker_id = self._parse_selection_id(self.worker_var.get())
        if task_id is None or worker_id is None:
            messagebox.showerror("Validation Error", "Selected task or worker is malformed.")
            return

        try:
            self.app.db.execute_query(
                "INSERT INTO TaskAssignments (TaskID, WorkerID) VALUES (%s, %s)",
                (task_id, worker_id)
            )
            messagebox.showinfo("Success", "Worker assigned to task successfully.")
            self.refresh_assignments()
            self.app.refresh_dashboard()
        except RuntimeError as exc:
            messagebox.showerror("Insert Failed", str(exc))

    def delete_assignment(self):
        assignment_id = self.assignment_id_var.get().strip()
        if not assignment_id:
            messagebox.showerror("Validation Error", "Select an assignment to delete.")
            return
        try:
            self.app.db.execute_query("DELETE FROM TaskAssignments WHERE AssignmentID = %s", (int(assignment_id),))
            messagebox.showinfo("Success", "Assignment deleted successfully.")
            self.assignment_id_var.set("")
            self.refresh_assignments()
            self.app.refresh_dashboard()
        except RuntimeError as exc:
            messagebox.showerror("Delete Failed", str(exc))

    def import_task_assignments_csv(self):
        """Import task assignments from CSV file."""
        filepath = filedialog.askopenfilename(
            title="Select Task Assignment CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filepath:
            return
        try:
            with open(filepath, newline="", encoding="cp1252", errors="replace") as f:
                rows = list(csv.DictReader(f))

            # Build a mapping of task descriptions to TaskIDs
            tasks = self.app.db.fetch_all("SELECT TaskID, Task_Description FROM Task")
            task_desc_to_id = {task["Task_Description"].strip(): task["TaskID"] for task in tasks}

            inserted = 0
            skipped = 0
            current_task_id = None

            for row in rows:
                task_desc = row.get("TASK DESCRIPTION", "").strip()
                worker_id = row.get("Worker ID", "").strip()

                # Update current task if description is provided
                if task_desc:
                    current_task_id = task_desc_to_id.get(task_desc)

                # Skip rows without worker ID or if we don't have a current task
                if not worker_id or not current_task_id:
                    skipped += 1
                    continue

                # Insert assignment
                try:
                    self.app.db.execute_query(
                        "INSERT IGNORE INTO TaskAssignments (TaskID, WorkerID) VALUES (%s, %s)",
                        (current_task_id, worker_id)
                    )
                    inserted += 1
                except:
                    skipped += 1

            messagebox.showinfo(
                "Import Complete",
                f"{inserted} assignment(s) imported.\n{skipped} rows skipped (duplicates/invalid data)."
            )
            self.refresh_assignments()
            self.app.refresh_dashboard()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))

    def refresh_assignments(self):
        self.load_task_options()
        self.load_worker_options()
        try:
            rows = self.app.db.fetch_all(
                "SELECT ta.AssignmentID, ta.TaskID, ta.WorkerID, w.WorkerName, t.Task_Description, ta.AssignedDate "
                "FROM TaskAssignments ta "
                "LEFT JOIN Workers w ON ta.WorkerID = w.WorkerID "
                "LEFT JOIN Task t ON ta.TaskID = t.TaskID "
                "ORDER BY ta.AssignmentID"
            )
            self.assignment_tree.delete(*self.assignment_tree.get_children())
            for row in rows:
                self.assignment_tree.insert("", "end", values=(
                    row["AssignmentID"],
                    row["TaskID"],
                    row["WorkerID"],
                    row["WorkerName"],
                    row["Task_Description"],
                    row["AssignedDate"],
                ))
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def on_assignment_select(self, event):
        selected = self.assignment_tree.selection()
        if not selected:
            return
        values = self.assignment_tree.item(selected[0], "values")
        self.assignment_id_var.set(values[0])

    @staticmethod
    def _parse_selection_id(selection):
        """Extract ID from 'ID - Description' format."""
        if " - " not in selection:
            return None
        # Return string ID without converting to int (supports VARCHAR IDs like "002", "PE001")
        return selection.split(" - ", 1)[0].strip()


class MainFrame(ttk.Frame):
    """Main application frame containing all tabs."""

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.grid(row=0, column=0, sticky="nsew")
        self._build_main_interface()

    def _build_main_interface(self):
        self.master.title("Project Uno - Construction Manager")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TFrame", background="#f0f4f8")
        style.configure("TLabel", background="#f0f4f8", foreground="#1a3a5c")
        style.configure("TLabelframe", background="#f0f4f8", foreground="#1a3a5c")
        style.configure("TLabelframe.Label", background="#f0f4f8", foreground="#1a3a5c", font=("Segoe UI", 10, "bold"))
        style.configure("TNotebook", background="#f0f4f8")
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=24)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), foreground="#1a3a5c")
        style.configure("TButton", font=("Segoe UI", 10), padding=[8, 4])
        style.configure("TEntry", font=("Segoe UI", 10))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.dashboard_tab = DashboardTab(notebook, self.app)
        self.task_tab = TaskMonitoringTab(notebook, self.app)
        self.resource_tab = ResourceManagementTab(notebook, self.app)
        self.assignment_tab = TaskAssignmentTab(notebook, self.app)

        notebook.add(self.dashboard_tab, text="Dashboard")
        notebook.add(self.task_tab, text="Task Monitoring")
        notebook.add(self.resource_tab, text="Resource Management")
        notebook.add(self.assignment_tab, text="Task Assignment")


class ConstructionApp(ttk.Frame):
    """High-level application controller."""

    def __init__(self, root):
        self.root = root
        self.root.geometry("1180x760")
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        try:
            self.root.wm_attributes("-alpha", 1.0)
            self.root.configure(bg="#f0f4f8")
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
        if self.main_frame:
            self.main_frame.dashboard_tab.refresh_all_tables()

    def close(self):
        try:
            self.db.close()
        except Exception:
            pass
        self.root.destroy()
