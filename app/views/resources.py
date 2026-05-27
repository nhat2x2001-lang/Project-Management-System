# app/views/resources.py — Resource Management view (workers + materials).

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

from app import theme
from app.widgets.treeview import ScrollableTreeview


class ResourceManagementView(tk.Frame):
    """View for managing workers and materials."""

    def __init__(self, parent, db, on_data_change=None, **kwargs):
        super().__init__(parent, bg=theme.MAIN_BG, **kwargs)
        self.db             = db
        self.on_data_change = on_data_change

        self.worker_id_var   = tk.StringVar()
        self.worker_name_var = tk.StringVar()
        self.position_var    = tk.StringVar()

        self._build()
        self.load_workers()
        self.load_materials()

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def _build(self):
        header = tk.Frame(self, bg=theme.MAIN_BG)
        header.pack(fill="x", padx=20, pady=(20, 8))
        tk.Label(header, text="Resource Management",
                 bg=theme.MAIN_BG, fg=theme.TEXT_DARK,
                 font=(theme.FONT_FAMILY, 20, "bold")).pack(side="left")

        body = tk.Frame(self, bg=theme.MAIN_BG)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Workers panel (left)
        workers_panel = self._panel(body, "Workers")
        workers_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._build_workers_section(workers_panel)

        # Materials panel (right)
        materials_panel = self._panel(body, "Materials")
        materials_panel.pack(side="left", fill="both", expand=True)
        self._build_materials_section(materials_panel)

    def _build_workers_section(self, parent):
        content = tk.Frame(parent, bg=theme.CARD_BG)
        content.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Import button
        self._import_btn(content, "⬆  Import Workers CSV", self.import_workers_csv,
                         "Expected: Worker ID · Name · Resource Names")

        # Workers treeview
        self.workers_tree = ScrollableTreeview(
            content,
            columns=["WorkerID", "WorkerName", "Position"],
            height=12,
        )
        self.workers_tree.pack(fill="both", expand=True, pady=(6, 0))
        self.workers_tree.bind_select(self.on_worker_select)

        tk.Frame(content, bg=theme.CARD_BORDER, height=1).pack(fill="x", pady=10)

        # Form
        form = tk.Frame(content, bg=theme.CARD_BG)
        form.pack(fill="x")

        for label, var, state in [
            ("Worker ID", self.worker_id_var, "readonly"),
            ("Name",      self.worker_name_var, "normal"),
            ("Position",  self.position_var,    "normal"),
        ]:
            row = tk.Frame(form, bg=theme.CARD_BG)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, bg=theme.CARD_BG, fg=theme.TEXT_BODY,
                     font=(theme.FONT_FAMILY, 9), width=10, anchor="w").pack(side="left")
            ttk.Entry(row, textvariable=var, width=24, state=state).pack(side="left")

        btn_row = tk.Frame(content, bg=theme.CARD_BG)
        btn_row.pack(fill="x", pady=(10, 0))
        self._action_btn(btn_row, "➕ Add",    theme.COLOR_GREEN,  self.add_worker,    side="left")
        self._action_btn(btn_row, "✏ Update",  theme.COLOR_BLUE,   self.update_worker, side="left")
        self._action_btn(btn_row, "🗑 Remove",  theme.COLOR_RED,    self.remove_worker, side="left")
        self._action_btn(btn_row, "🧹 Clear",   theme.TEXT_MUTED,   self.clear_workers, side="left")

    def _build_materials_section(self, parent):
        content = tk.Frame(parent, bg=theme.CARD_BG)
        content.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self._import_btn(content, "⬆  Import Materials CSV", self.import_materials_csv,
                         "Expected: MATERIAL ID · MATERIALS · QUANTITY · Unit · Cost")

        self.materials_tree = ScrollableTreeview(
            content,
            columns=["MaterialID", "Materials", "Quantity", "Unit", "Cost"],
            height=20,
        )
        self.materials_tree.tree.column("Materials", width=200, minwidth=100)
        self.materials_tree.pack(fill="both", expand=True, pady=(6, 0))

        btn_row = tk.Frame(content, bg=theme.CARD_BG)
        btn_row.pack(fill="x", pady=(10, 0))
        self._action_btn(btn_row, "🧹 Clear All Materials",
                         theme.TEXT_MUTED, self.clear_materials, side="left")

    # ------------------------------------------------------------------
    # Workers CRUD
    # ------------------------------------------------------------------

    def load_workers(self):
        try:
            rows = self.db.fetch_all("SELECT * FROM Workers ORDER BY WorkerID")
            self.workers_tree.populate(rows, columns=["WorkerID", "WorkerName", "Position"])
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def on_worker_select(self, _event):
        values = self.workers_tree.get_selected_values()
        if not values:
            return
        self.worker_id_var.set(values[0])
        self.worker_name_var.set(values[1])
        self.position_var.set(values[2])

    def add_worker(self):
        name     = self.worker_name_var.get().strip()
        position = self.position_var.get().strip()
        if not name or not position:
            messagebox.showerror("Validation Error", "Name and position are required.")
            return
        try:
            self.db.execute_query(
                "INSERT INTO Workers (WorkerName, Position) VALUES (%s, %s)",
                (name, position)
            )
            messagebox.showinfo("Success", "Worker added successfully.")
            self._clear_worker_form()
            self.load_workers()
            self._notify_change()
        except RuntimeError as exc:
            messagebox.showerror("Insert Failed", str(exc))

    def update_worker(self):
        worker_id = self.worker_id_var.get().strip()
        name      = self.worker_name_var.get().strip()
        position  = self.position_var.get().strip()
        if not worker_id or not name or not position:
            messagebox.showerror("Validation Error", "Select a worker and fill in all fields.")
            return
        try:
            self.db.execute_query(
                "UPDATE Workers SET WorkerName = %s, Position = %s WHERE WorkerID = %s",
                (name, position, worker_id)
            )
            messagebox.showinfo("Success", "Worker updated.")
            self.load_workers()
            self._notify_change()
        except RuntimeError as exc:
            messagebox.showerror("Update Failed", str(exc))

    def remove_worker(self):
        worker_id = self.worker_id_var.get().strip()
        if not worker_id:
            messagebox.showerror("Validation Error", "Select a worker first.")
            return
        try:
            self.db.execute_query("DELETE FROM Workers WHERE WorkerID = %s", (worker_id,))
            messagebox.showinfo("Success", "Worker removed.")
            self._clear_worker_form()
            self.load_workers()
            self._notify_change()
        except RuntimeError as exc:
            messagebox.showerror("Delete Failed", str(exc))

    def clear_workers(self):
        if not messagebox.askyesno("Clear Workers",
                                   "Permanently delete ALL workers?"):
            return
        try:
            self.db.execute_query("SET SQL_SAFE_UPDATES = 0")
            self.db.execute_query("DELETE FROM Workers")
            self.db.execute_query("SET SQL_SAFE_UPDATES = 1")
            messagebox.showinfo("Success", "All workers cleared.")
            self.load_workers()
            self._notify_change()
        except Exception as exc:
            messagebox.showerror("Clear Failed", str(exc))

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
            seen_ids, inserted, skipped = set(), 0, 0
            for row in rows:
                worker_id = row.get("Worker ID", "").strip()
                name      = row.get("Name", "").strip()
                position  = row.get("Resource Names", "").strip()
                if not worker_id or not name or worker_id in seen_ids:
                    skipped += 1
                    continue
                seen_ids.add(worker_id)
                self.db.execute_query(
                    "INSERT IGNORE INTO Workers (WorkerID, WorkerName, Position) VALUES (%s, %s, %s)",
                    (worker_id, name, position)
                )
                inserted += 1
            messagebox.showinfo("Import Complete",
                                f"{inserted} worker(s) imported.\n{skipped} rows skipped.")
            self.load_workers()
            self._notify_change()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))

    # ------------------------------------------------------------------
    # Materials
    # ------------------------------------------------------------------

    def load_materials(self):
        try:
            rows = self.db.fetch_all("SELECT * FROM Materials ORDER BY MaterialID")
            self.materials_tree.populate(rows,
                columns=["MaterialID", "Materials", "Quantity", "Unit", "Cost"])
        except RuntimeError as exc:
            messagebox.showerror("Load Failed", str(exc))

    def clear_materials(self):
        if not messagebox.askyesno("Clear Materials",
                                   "Permanently delete ALL materials?"):
            return
        try:
            self.db.execute_query("SET SQL_SAFE_UPDATES = 0")
            self.db.execute_query("DELETE FROM Materials WHERE MaterialID > 0")
            self.db.execute_query("ALTER TABLE Materials AUTO_INCREMENT = 1")
            self.db.execute_query("SET SQL_SAFE_UPDATES = 1")
            messagebox.showinfo("Success", "All materials cleared.")
            self.load_materials()
            self._notify_change()
        except Exception as exc:
            messagebox.showerror("Clear Failed", str(exc))

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
            inserted, skipped = 0, 0
            for row in rows:
                material_id = self._parse_int(row.get("MATERIAL ID", "0"))
                name        = row.get("MATERIALS", "").strip()
                if not material_id or not name:
                    skipped += 1
                    continue
                self.db.execute_query(
                    "INSERT IGNORE INTO Materials (MaterialID, Materials, Quantity, Unit, Cost) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (
                        material_id, name,
                        self._parse_float(row.get("QUANTITY", "0")),
                        row.get("Unit", "").strip(),
                        self._parse_float(row.get("Cost", "0")),
                    )
                )
                inserted += 1
            messagebox.showinfo("Import Complete",
                                f"{inserted} material(s) imported.\n{skipped} rows skipped.")
            self.load_materials()
            self._notify_change()
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _clear_worker_form(self):
        self.worker_id_var.set("")
        self.worker_name_var.set("")
        self.position_var.set("")

    def _notify_change(self):
        if self.on_data_change:
            self.on_data_change()

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
                     font=(theme.FONT_FAMILY, 7), wraplength=240, justify="left").pack(anchor="w")

    def _action_btn(self, parent, text, bg_color, command, side="top"):
        btn = tk.Button(parent, text=text,
                        bg=bg_color, fg=theme.TEXT_WHITE,
                        activebackground=theme.ACCENT,
                        activeforeground=theme.TEXT_WHITE,
                        relief="flat", cursor="hand2",
                        font=(theme.FONT_FAMILY, 9),
                        padx=8, pady=5,
                        command=command)
        btn.pack(side=side, padx=(0, 4) if side == "left" else 0, pady=2, fill="x" if side == "top" else None)
