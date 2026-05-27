# app/views/dashboard.py — Dashboard view: KPI cards + charts + summary tables.

import tkinter as tk
from tkinter import ttk, messagebox

from app import theme
from app.widgets.kpi_card import KPICard
from app.widgets.treeview import ScrollableTreeview

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    _MPL_AVAILABLE = True
except ImportError:
    _MPL_AVAILABLE = False


# KPI card definitions ─ (label, icon, accent_color, db_query)
_CARDS = [
    ("Total Tasks",        "📋", theme.COLOR_BLUE,   "SELECT COUNT(*) AS n FROM Task"),
    ("Total Workers",      "👷", theme.COLOR_GREEN,  "SELECT COUNT(*) AS n FROM Workers"),
    ("Total Materials",    "🧱", theme.COLOR_ORANGE, "SELECT COUNT(*) AS n FROM Materials"),
    ("Budget Cost",        "💰", theme.COLOR_TEAL,   "SELECT COALESCE(SUM(BudgetCost),0) AS n FROM MaterialAssignmentCost"),
    ("Total Assignments",  "🔗", theme.COLOR_PURPLE, "SELECT COUNT(*) AS n FROM TaskAssignments"),
    ("Usage Cost",         "📦", theme.COLOR_RED,    "SELECT COALESCE(SUM(Cost),0) AS n FROM MaterialsUsage"),
]


class DashboardView(tk.Frame):
    """The main dashboard view.

    Layout (top to bottom)
    ─────────────────────
    1. Page header
    2. KPI cards row (6 cards)
    3. Charts row: bar chart (budget by task) + donut (materials)
    4. Summary tables row: recent tasks + recent assignments
    """

    def __init__(self, parent, db, **kwargs):
        super().__init__(parent, bg=theme.MAIN_BG, **kwargs)
        self.db = db
        self._card_widgets: list[KPICard] = []
        self._bar_canvas  = None
        self._pie_canvas  = None

        self._build()
        self.refresh()

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def _build(self):
        # ---- Scrollable outer container --------------------------------
        outer = tk.Frame(self, bg=theme.MAIN_BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=theme.MAIN_BG, highlightthickness=0)
        v_scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scroll.set)

        v_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._scroll_frame = tk.Frame(canvas, bg=theme.MAIN_BG)
        _window = canvas.create_window((0, 0), window=self._scroll_frame, anchor="nw")

        def _on_frame_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_configure(e):
            canvas.itemconfig(_window, width=e.width)

        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        self._scroll_frame.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        content = self._scroll_frame

        # ---- Page header -----------------------------------------------
        header_frame = tk.Frame(content, bg=theme.MAIN_BG)
        header_frame.pack(fill="x", padx=20, pady=(20, 4))

        tk.Label(header_frame, text="Dashboard",
                 bg=theme.MAIN_BG, fg=theme.TEXT_DARK,
                 font=(theme.FONT_FAMILY, 20, "bold")).pack(side="left")

        self._refresh_btn = tk.Button(
            header_frame,
            text="⟳  Refresh",
            bg=theme.PRIMARY, fg=theme.TEXT_WHITE,
            activebackground=theme.ACCENT,
            activeforeground=theme.TEXT_WHITE,
            relief="flat", cursor="hand2",
            font=(theme.FONT_FAMILY, 10),
            padx=12, pady=5,
            command=self.refresh,
        )
        self._refresh_btn.pack(side="right")

        self._last_updated = tk.Label(
            header_frame, text="",
            bg=theme.MAIN_BG, fg=theme.TEXT_MUTED,
            font=(theme.FONT_FAMILY, 9)
        )
        self._last_updated.pack(side="right", padx=(0, 12))

        # ---- KPI Cards -------------------------------------------------
        cards_outer = tk.Frame(content, bg=theme.MAIN_BG)
        cards_outer.pack(fill="x", padx=20, pady=(10, 6))

        cards_row = tk.Frame(cards_outer, bg=theme.MAIN_BG)
        cards_row.pack(fill="x")

        self._card_widgets = []
        for col_idx, (label, icon, color, _) in enumerate(_CARDS):
            card = KPICard(cards_row, label=label, value="—",
                           icon=icon, accent_color=color)
            card.grid(row=0, column=col_idx, padx=8, pady=6, sticky="nsew")
            self._card_widgets.append(card)

        for col_idx in range(len(_CARDS)):
            cards_row.grid_columnconfigure(col_idx, weight=1, uniform="card")

        # ---- Charts row ------------------------------------------------
        charts_frame = tk.Frame(content, bg=theme.MAIN_BG)
        charts_frame.pack(fill="x", padx=20, pady=(12, 12))

        if _MPL_AVAILABLE:
            # Bar chart panel
            bar_panel = self._card_panel(charts_frame, "Budget Cost by Task (Top 10)")
            bar_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
            self._bar_panel_body = tk.Frame(bar_panel, bg=theme.CARD_BG)
            self._bar_panel_body.pack(fill="both", expand=True, padx=12, pady=(0, 12))

            # Donut chart panel
            pie_panel = self._card_panel(charts_frame, "Materials by Quantity (Top 8)")
            pie_panel.pack(side="left", fill="both", expand=True, padx=(10, 0))
            self._pie_panel_body = tk.Frame(pie_panel, bg=theme.CARD_BG)
            self._pie_panel_body.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        else:
            lbl = tk.Label(
                charts_frame,
                text="Install matplotlib to enable charts:  pip install matplotlib",
                bg=theme.CARD_BG, fg=theme.TEXT_MUTED,
                font=(theme.FONT_FAMILY, 10),
                pady=20,
            )
            lbl.pack(fill="x")

        # ---- Summary tables row ----------------------------------------
        tables_frame = tk.Frame(content, bg=theme.MAIN_BG)
        tables_frame.pack(fill="both", expand=True, padx=20, pady=(6, 20))

        # Recent tasks
        tasks_panel = self._card_panel(tables_frame, "Recent Tasks")
        tasks_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self._tasks_tree = ScrollableTreeview(
            tasks_panel,
            columns=["TaskID", "Task_Description", "Duration", "Start", "Finish"],
            height=8,
        )
        self._tasks_tree.tree.column("Task_Description", width=220, minwidth=120)
        self._tasks_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Recent assignments
        assign_panel = self._card_panel(tables_frame, "Recent Assignments")
        assign_panel.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self._assign_tree = ScrollableTreeview(
            assign_panel,
            columns=["AssignmentID", "WorkerName", "Task_Description", "AssignedDate"],
            height=8,
        )
        self._assign_tree.tree.column("Task_Description", width=200, minwidth=100)
        self._assign_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ------------------------------------------------------------------
    # Data refresh
    # ------------------------------------------------------------------

    def refresh(self):
        """Reload all KPI values, charts, and summary tables from the DB."""
        self._refresh_cards()
        if _MPL_AVAILABLE:
            self._refresh_bar_chart()
            self._refresh_pie_chart()
        self._refresh_tasks_table()
        self._refresh_assignments_table()
        self._update_timestamp()

    def _refresh_cards(self):
        for card, (label, icon, color, query) in zip(self._card_widgets, _CARDS):
            try:
                rows = self.db.fetch_all(query)
                raw = rows[0]["n"] if rows else 0
                # Format currency values
                if label in ("Budget Cost", "Usage Cost"):
                    try:
                        value = f"₱{float(raw):,.2f}"
                    except (TypeError, ValueError):
                        value = str(raw)
                else:
                    value = str(int(float(raw))) if raw is not None else "0"
                card.update_value(value)
            except Exception:
                card.update_value("—")

    def _refresh_bar_chart(self):
        try:
            rows = self.db.fetch_all(
                "SELECT Task_Description, SUM(BudgetCost) AS total "
                "FROM MaterialAssignmentCost "
                "GROUP BY Task_Description "
                "ORDER BY total DESC "
                "LIMIT 10"
            )
        except Exception:
            rows = []

        labels = [r["Task_Description"][:28] + "…" if len(r["Task_Description"]) > 28
                  else r["Task_Description"] for r in rows]
        values = [float(r["total"]) for r in rows]

        if self._bar_canvas:
            self._bar_canvas.get_tk_widget().destroy()
            self._bar_canvas = None

        fig = Figure(figsize=(5.4, 3.2), dpi=90, facecolor=theme.CARD_BG)
        ax  = fig.add_subplot(111)
        ax.set_facecolor(theme.CARD_BG)
        fig.subplots_adjust(left=0.22, right=0.96, top=0.94, bottom=0.10)

        if values:
            palette = theme.CHART_PALETTE[:len(values)]
            bars = ax.barh(labels, values, color=palette[::-1], height=0.60)
            ax.invert_yaxis()
            ax.set_xlabel("₱ Budget Cost", fontsize=8, color=theme.TEXT_MUTED, labelpad=6)
            ax.tick_params(axis="both", labelsize=8, colors=theme.TEXT_BODY)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.tick_params(axis="y", length=0)
            ax.xaxis.set_major_formatter(
                matplotlib.ticker.FuncFormatter(lambda x, _: f"₱{x:,.0f}")
            )
            # Value labels
            for bar in bars:
                w = bar.get_width()
                ax.text(w * 1.01, bar.get_y() + bar.get_height() / 2,
                        f"₱{w:,.0f}", va="center", fontsize=7,
                        color=theme.TEXT_BODY, fontweight="bold")
        else:
            ax.text(0.5, 0.5, "No data yet", ha="center", va="center",
                    transform=ax.transAxes, color=theme.TEXT_MUTED, fontsize=10)
            ax.axis("off")

        self._bar_canvas = FigureCanvasTkAgg(fig, master=self._bar_panel_body)
        self._bar_canvas.draw()
        self._bar_canvas.get_tk_widget().pack(fill="both", expand=True)

    def _refresh_pie_chart(self):
        try:
            rows = self.db.fetch_all(
                "SELECT Materials, Quantity FROM Materials "
                "ORDER BY Quantity DESC LIMIT 8"
            )
        except Exception:
            rows = []

        labels = [r["Materials"][:20] for r in rows]
        values = [float(r["Quantity"]) for r in rows]

        if self._pie_canvas:
            self._pie_canvas.get_tk_widget().destroy()
            self._pie_canvas = None

        fig = Figure(figsize=(4.2, 3.2), dpi=90, facecolor=theme.CARD_BG)
        ax  = fig.add_subplot(111)
        ax.set_facecolor(theme.CARD_BG)
        fig.subplots_adjust(left=0.05, right=0.95, top=0.88, bottom=0.20)

        if values:
            wedges, texts, auto_texts = ax.pie(
                values, labels=None,
                colors=theme.CHART_PALETTE[:len(values)],
                autopct="%1.0f%%",
                pctdistance=0.78,
                startangle=90,
                wedgeprops=dict(width=0.50, edgecolor=theme.CARD_BG, linewidth=2.5),
            )
            for t in auto_texts:
                t.set_fontsize(8)
                t.set_color(theme.TEXT_WHITE)
                t.set_fontweight("bold")
            ax.legend(wedges, labels,
                      loc="lower center",
                      bbox_to_anchor=(0.5, -0.02),
                      ncol=2,
                      fontsize=7,
                      frameon=False,
                      handlelength=1.2,
                      handleheight=1.2)
        else:
            ax.text(0.5, 0.5, "No data yet", ha="center", va="center",
                    transform=ax.transAxes, color=theme.TEXT_MUTED, fontsize=10)
            ax.axis("off")

        self._pie_canvas = FigureCanvasTkAgg(fig, master=self._pie_panel_body)
        self._pie_canvas.draw()
        self._pie_canvas.get_tk_widget().pack(fill="both", expand=True)

    def _refresh_tasks_table(self):
        try:
            rows = self.db.fetch_all(
                "SELECT TaskID, Task_Description, Duration, Start, Finish "
                "FROM Task ORDER BY TaskID DESC LIMIT 20"
            )
            self._tasks_tree.populate(rows)
        except Exception:
            self._tasks_tree.clear()

    def _refresh_assignments_table(self):
        try:
            rows = self.db.fetch_all(
                "SELECT ta.AssignmentID, w.WorkerName, t.Task_Description, ta.AssignedDate "
                "FROM TaskAssignments ta "
                "LEFT JOIN Workers w ON ta.WorkerID = w.WorkerID "
                "LEFT JOIN Task t ON ta.TaskID = t.TaskID "
                "ORDER BY ta.AssignmentID DESC LIMIT 20"
            )
            self._assign_tree.populate(rows)
        except Exception:
            self._assign_tree.clear()

    def _update_timestamp(self):
        from datetime import datetime
        now = datetime.now().strftime("%b %d, %Y  %H:%M")
        self._last_updated.config(text=f"Last updated: {now}")

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    def _card_panel(self, parent, title: str) -> tk.Frame:
        """Create a white rounded-ish panel with a title label."""
        panel = tk.Frame(parent,
                         bg=theme.CARD_BG,
                         highlightbackground=theme.CARD_BORDER,
                         highlightthickness=1)
        title_bar = tk.Frame(panel, bg=theme.CARD_BG)
        title_bar.pack(fill="x", padx=10, pady=(10, 6))
        tk.Label(title_bar, text=title,
                 bg=theme.CARD_BG, fg=theme.TEXT_DARK,
                 font=(theme.FONT_FAMILY, 10, "bold")).pack(side="left")

        tk.Frame(panel, bg=theme.CARD_BORDER, height=1).pack(fill="x", padx=10)
        return panel
