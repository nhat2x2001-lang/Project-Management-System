# Project Uno - Construction Management Application
## Comprehensive Audit Report
**Date:** May 28, 2026 (Updated)

---

## 1. Project Overview

**Project Name:** Project Uno  
**Type:** Desktop GUI Application for Construction Management  
**Framework:** Python Tkinter (Desktop GUI)  
**Database:** MySQL  
**Purpose:** Manage construction projects with task scheduling, resource allocation, material tracking, and worker assignment.

---

## 2. Project Structure

```
Project-Management-System/
├── app.py                      # Main entry point (alternative wrapper)
├── main.py                     # Primary entry point
├── db_config.py                # Database configuration settings
├── db_connection.py            # Database connection manager
├── audit_csv_data.py           # CSV data quality audit script
├── requirements.txt            # Python dependencies
├── inspect.txt                 # Binary inspection file (non-functional)
├── README.md                   # Project documentation
├── PROJECT_AUDIT.md            # This audit document
├── app/
│   ├── __init__.py             # Package initialization
│   ├── gui.py                  # Main application components (LoginFrame, MainFrame, ConstructionApp)
│   ├── theme.py                # Color palette, fonts, ttk style configuration
│   ├── sidebar.py              # Collapsible sidebar navigation component
│   ├── views/
│   │   ├── __init__.py         # Views package initialization
│   │   ├── dashboard.py        # Dashboard view with KPI cards and charts
│   │   ├── tasks.py            # Task monitoring and management view
│   │   ├── resources.py        # Resource management view (workers & materials)
│   │   └── assignments.py      # Task assignment view
│   └── widgets/
│       ├── __init__.py         # Widgets package initialization
│       ├── kpi_card.py         # Reusable KPI card widget
│       └── treeview.py         # Reusable scrollable treeview widget
└── docs/
    ├── Material Assignment and Cost.csv
    ├── Materials Usage.csv
    ├── Materials.csv
    ├── Task Assignment.csv
    ├── Task_Assignment.csv
    ├── Task_Description.csv
    ├── Task.csv
    ├── Workers.csv
    └── res/
        ├── materials-usage.csv
        ├── materials.csv
        ├── tasks.csv
        └── workers.csv
```

---

## 3. File Descriptions

### 3.1 Entry Points

#### `main.py` (Primary Entry Point)
- **Purpose:** Main application launcher
- **Flow:**
  1. Creates Tkinter root window
  2. Initializes `ConstructionApp` from `app.gui`
  3. Sets up window close protocol
  4. Starts event loop
- **Entry Function:** `main()` - wraps execution with error handling
- **Error Handling:** Catches initialization exceptions and displays error dialog

#### `app.py` (Alternative Entry Point)
- **Purpose:** Alternative launcher with identical functionality
- **Status:** Duplicate of `main.py` logic - suggests multiple ways to run the app
- **Usage:** `python app.py`

### 3.2 Configuration Files

#### `db_config.py`
- **Purpose:** Centralized database configuration
- **Contents:**
  - Database credentials (host, user, password, database name)
  - Environment variable support for security
  - Default values for local MySQL connection
- **Environment Variables Supported:**
  - `PROJECT_UNO_DB_HOST`
  - `PROJECT_UNO_DB_USER`
  - `PROJECT_UNO_DB_PASSWORD`
  - `PROJECT_UNO_DB_DATABASE`
- **Default Credentials:**
  - Host: 127.0.0.1
  - User: root
  - Password: Rey_244456
  - Database: project_uno

#### `db_connection.py`
- **Purpose:** MySQL connection management and schema setup
- **Class:** `DatabaseConnection`
- **Key Methods:**
  - `__init()` - Initializes connection, creates DB/tables if needed
  - `_ensure_database_exists()` - Handles database creation
  - `connect()` - Establishes MySQL connection with fallback options
  - `_setup_schema()` - Creates required tables
  - `execute_query()` - Runs INSERT/UPDATE/DELETE queries
  - `fetch_all()` - Executes SELECT queries
  - `close()` - Closes database connection
- **Features:**
  - Automatic database creation if missing
  - Connection retry with fallback hosts (127.0.0.1/localhost)
  - Transaction management with rollback on errors
  - Connection pooling/recovery
  - Comprehensive error logging

#### `audit_csv_data.py`
- **Purpose:** Automated CSV data quality auditor
- **Features:**
  - Validates CSV files in docs/ directory
  - Checks for encoding errors (UTF-8)
  - Detects duplicate records
  - Validates data formats (dates, costs, etc.)
  - Identifies column name issues and typos
  - Generates comprehensive audit reports
- **Key Methods:**
  - `audit_file()` - Read and validate CSV files
  - `audit_task_csv()` - Audit Task.csv for format issues
  - `audit_workers_csv()` - Check for duplicate Worker IDs
  - `audit_materials_csv()` - Validate material data

### 3.3 Application Package (app/)

#### `app/__init__.py`
- **Purpose:** Package marker file
- **Content:** Package documentation comment

#### `app/gui.py` (Core Application Components)
- **Purpose:** Main application controller and login system
- **Size:** ~200 lines of code
- **Contains 3 Classes:**
  1. **LoginFrame** - Authentication interface with dark navy theme
  2. **MainFrame** - Main application shell with sidebar navigation
  3. **ConstructionApp** - High-level application controller
- **Key Features:**
  - Login authentication (reysosmena / Rey244456)
  - Sidebar-based navigation system
  - View routing and lifecycle management
  - Database connection initialization
  - Data change callbacks for cross-view updates

#### `app/theme.py` (Design System)
- **Purpose:** Centralized color palette, typography, and ttk styling
- **Color Palette:**
  - **Sidebar:** Dark navy (#1a2744) with active state (#2d4a7a)
  - **Main BG:** Light gray (#f0f4f8)
  - **Cards:** White (#ffffff) with border (#e2e8f0)
  - **Typography:** Dark text (#1a3a5c), body text (#374151), muted (#6b7a8d)
  - **Brand:** Primary (#1f4e79), Accent (#2563eb)
  - **Semantic:** Blue, Green, Orange, Red, Purple, Teal (for KPI cards)
- **Typography:**
  - **Font Family:** Segoe UI
  - **Font Sizes:** H1 (18pt bold), H2 (14pt bold), H3 (12pt bold), Body (10pt), Small (9pt)
- **Functions:**
  - `apply_styles(style)` - Configure all ttk widget styles globally
  - `font(size, weight)` - Generate font tuples

#### `app/sidebar.py` (Navigation Component)
- **Purpose:** Collapsible sidebar navigation widget
- **Class:** `CollapsibleSidebar(tk.Frame)`
- **Features:**
  - **Expanded width:** 220px (icon + text visible)
  - **Collapsed width:** 64px (icon only)
  - Dynamic item addition with callbacks
  - Active state highlighting
  - Hover effects
  - Toggle collapse/expand functionality
- **Public API:**
  - `add_item(icon, label, command)` - Append navigation item
  - `set_active(index)` - Highlight active view
  - Toggle button for collapse/expand

### 3.4 Views Package (app/views/)

#### `app/views/dashboard.py` (Dashboard View)
- **Purpose:** Main dashboard with KPI cards, charts, and summary tables
- **Class:** `DashboardView(tk.Frame)`
- **Features:**
  - **6 KPI Cards:**
    1. Total Tasks (📋) - Blue
    2. Total Workers (👷) - Green
    3. Total Materials (🧱) - Orange
    4. Budget Cost (💰) - Teal
    5. Total Assignments (🔗) - Purple
    6. Usage Cost (📦) - Red
  - **Charts (Matplotlib):**
    - Bar chart for budget cost by task
    - Donut chart for materials distribution
  - **Summary Tables:**
    - Recent tasks
    - Recent assignments
  - Scrollable layout with mouse wheel support
  - Refresh button for manual data reload
- **KPI Queries:**
  - Tasks: `SELECT COUNT(*) FROM Task`
  - Workers: `SELECT COUNT(*) FROM Workers`
  - Materials: `SELECT COUNT(*) FROM Materials`
  - Budget: `SELECT COALESCE(SUM(BudgetCost),0) FROM MaterialAssignmentCost`
  - Assignments: `SELECT COUNT(*) FROM TaskAssignments`
  - Usage: `SELECT COALESCE(SUM(Cost),0) FROM MaterialsUsage`

#### `app/views/tasks.py` (Task Monitoring View)
- **Purpose:** Task creation, search, editing, and deletion
- **Class:** `TaskMonitoringView(tk.Frame)`
- **Features:**
  - Add new tasks with validation
  - Search by description or Task ID
  - Delete tasks (with cascade)
  - CSV import (Task ID, WBS Code, Task Description, Duration, Start, Finish, Predecessors)
  - Clear all tasks functionality
  - Form fields with validation:
    - Task ID (auto-assigned)
    - WBS Code
    - Task Description
    - Duration (days)
    - Start Date (YYYY-MM-DD)
    - Finish Date (YYYY-MM-DD)
    - Predecessors
  - Task list with full details (sortable treeview)
  - Selected task info display
- **Operations:**
  - `add_task()` - Insert new task
  - `remove_task()` - Delete selected task
  - `search_task()` - Search by description
  - `search_task_by_id()` - Search by Task ID
  - `import_tasks_csv()` - Bulk import from CSV
  - `clear_tasks()` - Remove all tasks

#### `app/views/resources.py` (Resource Management View)
- **Purpose:** Manage workers and materials
- **Class:** `ResourceManagementView(tk.Frame)`
- **Features:**
  - **Workers Panel (Left):**
    - Workers treeview (WorkerID, WorkerName, Position)
    - Add new worker
    - Update existing worker
    - Remove worker
    - Clear all workers
    - CSV import (Worker ID, Name, Resource Names)
  - **Materials Panel (Right):**
    - Materials treeview (MaterialID, Materials, Quantity, Unit, Cost)
    - View material inventory
    - CSV import
    - Clear all materials
- **Operations:**
  - `add_worker()` - Insert new worker
  - `update_worker()` - Modify worker details
  - `remove_worker()` - Delete worker
  - `clear_workers()` - Remove all workers
  - `import_workers_csv()` - Bulk import workers
  - `import_materials_csv()` - Bulk import materials
  - `load_workers()` - Populate worker list
  - `load_materials()` - Populate materials list

#### `app/views/assignments.py` (Task Assignment View)
- **Purpose:** Assign workers to tasks and manage assignments
- **Class:** `TaskAssignmentView(tk.Frame)`
- **Features:**
  - Task dropdown selector (populated from Task table)
  - Worker dropdown selector (populated from Workers table)
  - Assign worker to task button
  - Assignments treeview with joined data:
    - AssignmentID
    - TaskID
    - WorkerID
    - WorkerName (joined from Workers)
    - Task_Description (joined from Task)
    - AssignedDate
  - Delete assignment functionality
  - CSV import (Task ID, Worker ID)
  - Refresh assignments list
- **Operations:**
  - `add_assignment()` - Create task-worker assignment
  - `delete_assignment()` - Remove assignment
  - `refresh_assignments()` - Reload assignment data with joins
  - `import_task_assignments_csv()` - Bulk import assignments
  - `load_task_options()` - Populate task dropdown
  - `load_worker_options()` - Populate worker dropdown

### 3.5 Widgets Package (app/widgets/)

#### `app/widgets/kpi_card.py` (KPI Card Widget)
- **Purpose:** Reusable KPI metric display card
- **Class:** `KPICard(tk.Frame)`
- **Features:**
  - Left-side accent bar (color-coded per metric)
  - Large value number (responsive font sizing)
  - Descriptive label (uppercase)
  - Icon character (emoji support)
  - Automatic font scaling based on value length
- **Parameters:**
  - `label` - Metric title (e.g., "Total Tasks")
  - `value` - Initial value to display (string or integer)
  - `icon` - Unicode character for icon (e.g., "📋")
  - `accent_color` - Hex color for accent bar
- **Methods:**
  - `update_value(value)` - Update displayed value with auto font-sizing

#### `app/widgets/treeview.py` (Scrollable Treeview Widget)
- **Purpose:** Reusable treeview with built-in scrollbars
- **Class:** `ScrollableTreeview(ttk.Frame)`
- **Features:**
  - Vertical and horizontal scrollbars (pre-wired)
  - Zebra-stripe rows (alternating colors)
  - Column header auto-formatting
  - Configurable height
  - Selection handling
- **Methods:**
  - `clear()` - Remove all rows
  - `populate(rows, columns)` - Bulk insert rows from list of dicts
  - `bind_select(callback)` - Bind selection event handler
  - `get_selected_values()` - Retrieve selected row values
- **Usage:**
  ```python
  tree_widget = ScrollableTreeview(parent, columns=["ID", "Name", "Value"], height=10)
  tree_widget.pack(fill="both", expand=True)
  tree_widget.populate(data_rows)
  ```

---

## 4. Application Architecture

### 4.1 Application Flow

```
User Starts Application
    ↓
main.py / app.py
    ↓
ConstructionApp.__init__()
    ↓
DatabaseConnection (auto-setup DB/tables)
    ↓
LoginFrame displays
    ↓
User Login (reysosmena / Rey244456)
    ↓
MainFrame with CollapsibleSidebar
    ↓
View-based routing system (_navigate method)
    ├── 📊 Dashboard (DashboardView)
    │   ├── 6 KPI Cards (Tasks, Workers, Materials, Budget, Assignments, Usage)
    │   ├── Charts (Matplotlib: bar chart, donut chart)
    │   └── Summary Tables (recent tasks, recent assignments)
    ├── 📋 Task Monitoring (TaskMonitoringView)
    │   ├── Task form (add/edit/delete)
    │   ├── Search functionality
    │   └── CSV import
    ├── 👷 Resources (ResourceManagementView)
    │   ├── Workers panel (CRUD operations)
    │   └── Materials panel (view/import)
    └── 🔗 Task Assignment (TaskAssignmentView)
        ├── Assign worker to task
        ├── View assignments (with joins)
        └── Delete assignments
```

### 4.2 Navigation System

#### CollapsibleSidebar
- **Location:** Left side of MainFrame
- **Width:** 220px (expanded) / 64px (collapsed)
- **Navigation Items:**
  1. 📊 Dashboard
  2. 📋 Task Monitoring
  3. 👷 Resources
  4. 🔗 Task Assignment
- **Features:**
  - Click to navigate between views
  - Active state highlighting (dark blue background)
  - Hover effects (lighter blue)
  - Toggle button to collapse/expand
  - Icon-based navigation in collapsed state

#### View Routing
- **Method:** `MainFrame._navigate(index)`
- **Process:**
  1. Destroy current view (if exists)
  2. Update sidebar active state
  3. Instantiate new view class
  4. Pass database connection and callbacks
  5. Grid new view into content pane
- **Data Flow:**
  - Views call `on_data_change()` callback after mutations
  - MainFrame refreshes dashboard if active
  - Cross-view data consistency maintained

### 4.3 Core Application Components

#### 1. **LoginFrame** (tk.Frame)
- **Purpose:** Authentication layer
- **Features:**
  - Centered card design with dark navy header
  - White card body with form fields
  - Logo area with emoji icon (🏗)
  - Username/password fields with focus management
  - Hardcoded credentials validation (reysosmena / Rey244456)
  - Enter key support for form submission
  - Error dialog for invalid credentials
- **Styling:**
  - Card background: White (#ffffff)
  - Primary color: Navy (#1f4e79)
  - Accent on hover: Blue (#2563eb)
  - Font: Segoe UI (22pt bold for title, 10pt for labels)
- **Window Size:** 440 × 560 pixels

#### 2. **MainFrame** (tk.Frame)
- **Purpose:** Main application shell
- **Layout:**
  - Left: CollapsibleSidebar (220px / 64px)
  - Right: Content pane (dynamic views)
- **Navigation Items:** 4 views (defined in `_NAV` class variable)
- **Features:**
  - Dynamic view instantiation
  - Data change callbacks
  - Automatic dashboard refresh
  - Grid-based layout (responsive)
- **Window Size:** 1340 × 820 pixels (resizable, min: 900 × 600)

#### 3. **ConstructionApp**
- **Purpose:** High-level application controller
- **Responsibilities:**
  - Window initialization and configuration
  - Database connection management
  - Login/main interface transitions
  - Application lifecycle (close handler)
- **Key Methods:**
  - `__init__(root)` - Initialize window, database, login frame
  - `show_main_interface()` - Transition from login to main app
  - `refresh_dashboard()` - Compatibility shim for dashboard refresh
  - `close()` - Cleanup database connection

### 4.4 View Architecture

#### View Base Pattern
All views inherit from `tk.Frame` and follow this pattern:
```python
class ViewName(tk.Frame):
    def __init__(self, parent, db, on_data_change=None):
        super().__init__(parent, bg=theme.MAIN_BG)
        self.db = db
        self.on_data_change = on_data_change
        self._build()       # Build UI
        self.load_data()    # Load initial data
    
    def _notify_change(self):
        if self.on_data_change:
            self.on_data_change()
```

#### DashboardView
- **Purpose:** KPI overview, charts, and summary data
- **Layout:**
  - Page header with refresh button
  - KPI cards row (6 cards in grid)
  - Charts row (bar chart + donut chart)
  - Summary tables row (tasks + assignments)
- **Features:**
  - Scrollable content (mouse wheel support)
  - Matplotlib integration (bar/donut charts)
  - Live KPI queries from database
  - Auto-refresh on data changes

#### TaskMonitoringView
- **Purpose:** Task CRUD operations
- **Layout:**
  - Left panel: Task form (add/delete/search/import)
  - Right panel: Task list (treeview with 7 columns)
- **Features:**
  - Form validation (dates, duration)
  - Search by description or Task ID
  - CSV import with format detection
  - Selected task info display
  - Clear all tasks functionality

#### ResourceManagementView
- **Purpose:** Worker and material management
- **Layout:**
  - Left panel: Workers (list + CRUD form)
  - Right panel: Materials (list + import)
- **Features:**
  - Worker CRUD (add, update, remove, clear)
  - CSV import for workers and materials
  - Form pre-population on row selection
  - Separate treeviews for workers and materials

#### TaskAssignmentView
- **Purpose:** Worker-task assignment management
- **Layout:**
  - Left panel: Assignment form (dropdowns + controls)
  - Right panel: Assignments list (with joined data)
- **Features:**
  - Task dropdown (loaded from Task table)
  - Worker dropdown (loaded from Workers table)
  - Assignments treeview with JOIN query (shows names, not just IDs)
  - Delete assignment functionality
  - CSV import for bulk assignments
  - Refresh button for manual reload

#### 1. **LoginFrame** (ttk.Frame)
- **Purpose:** Authentication layer
- **Features:**
  - Blue and white themed login form
  - Username/password fields
  - Hardcoded credentials validation (reysosmena / Rey244456)
  - Displays error messages for invalid credentials


---

## 5. Database Schema

### 5.1 Tables Created Automatically

#### 1. **Task**
```sql
CREATE TABLE Task (
    TaskID INT AUTO_INCREMENT PRIMARY KEY,
    WBS_Code VARCHAR(50),
    Task_Description VARCHAR(255),
    Duration INT,
    Start DATE,
    Finish DATE,
    Predecessors VARCHAR(100)
)
```
- Stores construction tasks and their schedule

#### 2. **Materials**
```sql
CREATE TABLE Materials (
    MaterialID INT AUTO_INCREMENT PRIMARY KEY,
    Materials VARCHAR(255),
    Quantity INT,
    Unit VARCHAR(50),
    Cost DECIMAL(10,2)
)
```
- Stores material inventory

#### 3. **Workers**
```sql
CREATE TABLE Workers (
    WorkerID INT AUTO_INCREMENT PRIMARY KEY,
    WorkerName VARCHAR(255),
    Position VARCHAR(100)
)
```
- Stores worker information

#### 4. **MaterialAssignmentCost**
```sql
CREATE TABLE MaterialAssignmentCost (
    ForemanID INT AUTO_INCREMENT PRIMARY KEY,
    Task_Description VARCHAR(255),
    Materials VARCHAR(255),
    Quantity INT,
    Unit VARCHAR(50),
    UnitPrice DECIMAL(10,2),
    BudgetCost DECIMAL(10,2)
)
```
- Tracks material costs per task/foreman

#### 5. **MaterialsUsage**
```sql
CREATE TABLE MaterialsUsage (
    UsageID INT AUTO_INCREMENT PRIMARY KEY,
    TaskID INT,
    MaterialID INT,
    Materials VARCHAR(255),
    Quantity INT,
    Unit VARCHAR(50),
    Cost DECIMAL(10,2),
    FOREIGN KEY (TaskID) REFERENCES Task(TaskID) ON DELETE CASCADE,
    FOREIGN KEY (MaterialID) REFERENCES Materials(MaterialID) ON DELETE CASCADE
)
```
- Records material usage on tasks with foreign key relationships

#### 6. **TaskAssignments**
```sql
CREATE TABLE TaskAssignments (
    AssignmentID INT AUTO_INCREMENT PRIMARY KEY,
    TaskID INT,
    WorkerID INT,
    AssignedDate DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (TaskID) REFERENCES Task(TaskID) ON DELETE CASCADE,
    FOREIGN KEY (WorkerID) REFERENCES Workers(WorkerID) ON DELETE CASCADE
)
```
- Links workers to tasks

### 5.2 Database Relationships

```
Task
  ├── 1:N → TaskAssignments
  └── 1:N → MaterialsUsage

Workers
  └── 1:N → TaskAssignments

Materials
  └── 1:N → MaterialsUsage

MaterialAssignmentCost (Standalone - master list)
```

---

## 6. Features Summary

### 6.1 Authentication
- ✅ Login screen with username/password
- ✅ Hardcoded credentials (for this version)
- ✅ Error handling for invalid credentials

### 6.2 Dashboard
- ✅ Multi-table data display
- ✅ Global search across tasks
- ✅ Manual refresh capability
- ✅ Horizontal/vertical scrolling for large datasets

### 6.3 Task Management
- ✅ Create tasks with WBS codes
- ✅ Track task schedule (start/finish dates)
- ✅ Define task dependencies (predecessors)
- ✅ Search tasks by ID or description
- ✅ Delete tasks with cascade cleanup

### 6.4 Resource Management
- ✅ Add/update/remove workers
- ✅ Track worker positions
- ✅ View material inventory
- ✅ Display material costs

### 6.5 Task Assignment
- ✅ Assign workers to tasks
- ✅ View all assignments with joined data
- ✅ Track assignment dates
- ✅ Delete assignments

### 6.6 Data Management
- ✅ CRUD operations on all entities
- ✅ Data validation (integers, dates)
- ✅ Transaction support with rollback
- ✅ Cascade delete on foreign keys
- ✅ Auto-increment primary keys

---

## 7. Technical Stack

### Dependencies
- **mysql-connector-python** - MySQL database driver
- **matplotlib** - Charting library for KPI visualization (bar charts, donut charts)

### Libraries Used
```python
import tkinter as tk                      # GUI framework
from tkinter import ttk, messagebox       # Widgets and dialogs
from datetime import datetime             # Date handling
import mysql.connector                    # Database connection
import logging                            # Error logging
import os                                 # Environment variables
import csv                                # CSV import/export
import matplotlib                         # Charting library
from matplotlib.figure import Figure      # Chart figures
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Tkinter integration
```

### UI Framework
- **Tkinter (ttk)** - Standard Python GUI toolkit
- **Themed widgets** (ttk) for modern appearance
- **Custom theme system** - Centralized color palette and styling (app/theme.py)
- **Reusable components** - KPICard, ScrollableTreeview widgets
- **Color scheme:** 
  - **Primary:** Navy (#1f4e79)
  - **Accent:** Blue (#2563eb)
  - **Background:** Light gray (#f0f4f8)
  - **Cards:** White (#ffffff)
  - **Sidebar:** Dark navy (#1a2744)

### Database
- **MySQL** (required to be running)
- **Default port:** 3306
- **Autocommit:** Disabled (manual transaction control)
- **Dictionary cursors:** Enabled (field access by name)
- **Default credentials:** root / Rey_244456

---

## 8. Configuration & Setup

### 8.1 Database Prerequisites
- MySQL server running (localhost/127.0.0.1:3306)
- User account: `project_uno` with password `ProjectUnoPass!23`
- Or use environment variables to override defaults

### 8.2 Connection Flow
1. App checks if database exists
2. Creates database if missing
3. Establishes connection
4. Creates all tables if missing
5. Application ready for use

### 8.3 Environment Variables
Set these to override defaults:
```
PROJECT_UNO_DB_HOST=your_host
PROJECT_UNO_DB_USER=your_user
PROJECT_UNO_DB_PASSWORD=your_password
PROJECT_UNO_DB_DATABASE=project_uno
```

---

## 9. Application Window Properties

### Login Window
- **Window Size:** 440 × 560 pixels (centered card design)
- **Window Title:** "Project Uno - Login"
- **Theme:** Dark navy header with white card body
- **Font:** Segoe UI (22pt bold for title, 10pt for labels)

### Main Application Window
- **Window Size:** 1340 × 820 pixels (resizable)
- **Minimum Size:** 900 × 600 pixels
- **Window Title:** "Project Uno - Construction Manager"
- **Theme:** Custom theme system (app/theme.py)
  - **Sidebar:** Dark navy (#1a2744)
  - **Content:** Light gray (#f0f4f8)
  - **Cards:** White (#ffffff)
- **Font:** Segoe UI
  - **H1:** 20pt bold (page headers)
  - **H2:** 14pt bold (section headers)
  - **H3:** 12pt bold (labels)
  - **Body:** 10pt regular
  - **Small:** 9pt regular
- **Layout:** Sidebar (220px / 64px) + Dynamic content pane

---

## 10. Error Handling

### 10.1 Database Errors
- Connection failures → RuntimeError with detailed message
- Query execution failures → Automatic rollback
- Access denied (errno 1045) → Specific permission instructions

### 10.2 GUI Errors
- Login failures → messagebox.showerror dialog
- Data loading failures → messagebox.showerror with query error
- Validation failures → messagebox.showerror with field name
- Success messages → messagebox.showinfo dialog

### 10.3 Logging
- Logger configured: `logging.getLogger(__name__)`
- Debug level: Database connection info
- Error level: Access denied, connection failures
- Exception level: All error details

---

## 11. Key Execution Paths

### Path 1: Application Startup
```
main.py → ConstructionApp() → LoginFrame() → [Wait for login]
```

### Path 2: Login to Main App
```
LoginFrame._handle_login() → app.show_main_interface() 
→ MainFrame() → [Display 4 tabs]
```

### Path 3: Dashboard Search
```
Search input → search_tasks() → Database query 
→ _populate_tree() → Display results
```

### Path 4: Task Creation
```
TaskMonitoringTab.add_task() → Validation → execute_query() 
→ refresh_task_list() → app.refresh_dashboard()
```

### Path 5: Worker Assignment
```
TaskAssignmentTab.add_assignment() → Parse selections 
→ execute_query() → refresh_assignments() → app.refresh_dashboard()
```

---

## 12. Potential Issues & Notes

### Issues Identified
1. **Hardcoded Credentials:** Login uses hardcoded username/password
2. **No Session Management:** Credentials checked against fixed values
3. **No User Permissions:** All logged-in users have same access level
4. **Database Privileges:** Hardcoded password in db_config.py (not ideal for production)
5. **inspect.txt:** Binary file that serves no clear purpose
6. **Missing Dependencies:** Current environment lacks mysql-connector-python and matplotlib installations

### Technical Observations (May 28, 2026)
- **Architecture Evolution:** Application has been refactored from monolithic gui.py (~800 lines) to modular architecture:
  - Views package (app/views/) with 4 separate view modules
  - Widgets package (app/widgets/) with reusable components
  - Theme system (app/theme.py) for consistent styling
  - Sidebar navigation (app/sidebar.py) for improved UX
- **Additional CSV Files:** Discovered in docs/res/ folder:
  - materials-usage.csv
  - materials.csv
  - tasks.csv
  - workers.csv
- **Matplotlib Integration:** Dashboard now includes charts (bar chart, donut chart) for data visualization
- **Enhanced Dashboard:** 6 KPI cards with color-coded metrics and icons

### Areas for Enhancement
- [ ] Implement role-based access control
- [ ] Add database authentication layer
- [ ] Implement audit logging
- [ ] Add data export functionality (CSV, PDF reports)
- [ ] Implement budget tracking/reporting with charts
- [ ] Add task progress tracking (% complete)
- [ ] Implement material inventory alerts (low stock warnings)
- [ ] Add user management interface
- [ ] Implement backup/restore functionality
- [ ] Consider SQLite migration for portable deployment
- [ ] Add dark mode theme option

---

## 13. File Dependencies Graph

```
main.py / app.py
    ↓
ConstructionApp (from app.gui)
    ↓
├── LoginFrame (from app.gui)
│
├── MainFrame (from app.gui)
│   ├── CollapsibleSidebar (from app.sidebar)
│   │   └── theme (from app.theme)
│   │
│   └── View Routing (_navigate method)
│       ├── DashboardView (from app.views.dashboard)
│       │   ├── KPICard (from app.widgets.kpi_card)
│       │   ├── ScrollableTreeview (from app.widgets.treeview)
│       │   └── matplotlib (charts)
│       │
│       ├── TaskMonitoringView (from app.views.tasks)
│       │   └── ScrollableTreeview (from app.widgets.treeview)
│       │
│       ├── ResourceManagementView (from app.views.resources)
│       │   └── ScrollableTreeview (from app.widgets.treeview)
│       │
│       └── TaskAssignmentView (from app.views.assignments)
│           └── ScrollableTreeview (from app.widgets.treeview)
│
└── DatabaseConnection (from db_connection)
    ├── db_config.DB_CONFIG
    └── mysql.connector

All views import:
    └── theme (from app.theme)
```

---

## 14. Testing Checklist

### Setup
- [ ] MySQL server running on localhost:3306
- [ ] Database credentials configured or env vars set
- [ ] Python dependencies installed (`pip install -r requirements.txt`)

### Functional Testing
- [ ] Application launches without errors
- [ ] Login with correct credentials works
- [ ] Login with wrong credentials shows error
- [ ] All 4 tabs load without errors
- [ ] Dashboard displays all 6 tables
- [ ] Search functionality works on Dashboard
- [ ] Can add/edit/delete tasks
- [ ] Can add/update/remove workers
- [ ] Can add/remove task assignments
- [ ] Task deletion cascades properly
- [ ] Data refreshes across tabs

### Data Validation
- [ ] Date format validation (YYYY-MM-DD)
- [ ] Integer field validation (Duration, etc.)
- [ ] Required field validation
- [ ] Foreign key relationships maintained

---

## 15. CSV Data Audit Report

**Date Conducted:** May 27, 2026  
**Audit Tool:** audit_csv_data.py

### 15.1 Audit Overview

A comprehensive audit of the CSV files in the `docs/` directory was performed to identify data quality issues and inconsistencies. The audit examined 8 CSV files containing project data.

### 15.2 Critical Issues Found

#### **Critical: Encoding Errors (3 files)**
- **Material Assignment and Cost.csv** - UTF-8 decode error at byte position 5599
- **Materials Usage.csv** - UTF-8 decode error at byte position 3807  
- **Materials.csv** - UTF-8 decode error at byte position 3282

**Impact:** These files cannot be loaded with UTF-8 encoding. Likely causes:
- Files saved with UTF-16 encoding
- Contains special characters (em-dashes, smart quotes, etc.)
- Requires character encoding detection and conversion

**Recommendation:** Re-save these files with UTF-8 encoding or identify the correct encoding.

#### **High: Duplicate Worker IDs (32 unique IDs with duplicates)**
- PE001: 9 occurrences
- L001-L016: 6-11 occurrences each
- LM001-LM004: 2 occurrences each
- L017-L027: 2-4 occurrences each

**Total:** 213 worker records with massive duplication

**Impact:** 
- Cannot maintain referential integrity in database
- Task assignments will be ambiguous
- Data import will fail or create inconsistent records

**Recommendation:** 
1. Deduplicate Workers.csv (remove duplicate rows, keep only unique workers)
2. Verify that Workers.csv and Task_Assignment.csv are related (they appear to be)
3. Consider if Workers.csv should be flattened (currently expanded for each task assignment)

#### **Medium: Data Format & Naming Issues**

**Task.csv:**
- Column name typo: `Task Discription` should be `Task Description`
- Date format: Uses "Day MM/DD/YY" format (e.g., "Tue 10/07/25") - non-standard for database import
- Duration format: Contains text "days" (e.g., "3.22 days") - will require parsing

**Workers.csv:**
- 3 records with leading/trailing spaces
- Misspelling: "Safey Practitioner" should be "Safety Practitioner"

**Materials.csv:**
- Cost values contain comma separators (e.g., "1,560.00") - non-numeric format for database

**Material Assignment and Cost.csv:**
- Cost values contain comma separators - non-numeric format

**Materials Usage.csv:**
- Cost values contain comma separators - non-numeric format

### 15.3 File-by-File Analysis

| File | Records | Status | Issues |
|------|---------|--------|--------|
| Task.csv | 66 | ⚠️ Warning | 1 column typo, date/duration format |
| Task_Description.csv | 66 | ✅ OK | No issues detected |
| Task_Assignment.csv | 232 | ⚠️ Warning | 232 worker-task combinations |
| Workers.csv | 213 | ❌ Critical | 32 duplicate IDs, spacing issues, misspelling |
| Materials.csv | N/A | ❌ Critical | Encoding error, comma-separated costs |
| Material Assignment and Cost.csv | N/A | ❌ Critical | Encoding error, comma-separated costs |
| Materials Usage.csv | N/A | ❌ Critical | Encoding error, comma-separated costs |

### 15.4 Data Quality Issues Summary

**Total Issues Found: 38**

- **Encoding Errors:** 3 files
- **Duplicate Records:** 32 unique Worker IDs (213 total duplicates)
- **Format Issues:** Column typos, date formats, cost formatting
- **Text Issues:** Misspellings, leading/trailing spaces

### 15.5 CSV File Relationships

```
Task.csv (66 tasks)
  ↓
Task_Assignment.csv (232 worker-task combinations)
  ├── References Workers (by Worker ID)
  └── References Task (implicit via description)

Workers.csv (213 records - mostly duplicates)
  ├── Lists all workers (with high duplication)
  └── Used in Task_Assignment.csv

Materials.csv
  ↓
Material Assignment and Cost.csv
  (tracks material costs per foreman/task)
  ↓
Materials Usage.csv
  (tracks actual material usage on tasks)
```

### 15.6 Recommendations for Data Import

1. **Fix Encoding Issues First:**
   - Convert Materials.csv, Material Assignment and Cost.csv, Materials Usage.csv to UTF-8
   - Use: iconv, PowerShell, or Python script to convert

2. **Deduplicate Workers:**
   - Extract unique worker records from Workers.csv
   - Create separate "TaskWorkerAssignments" or enhance Task_Assignment.csv structure
   - Result: ~50-70 unique workers (estimate)

3. **Standardize Formats:**
   - Remove comma separators from all currency values
   - Convert dates to YYYY-MM-DD format
   - Extract numeric values from Duration field
   - Fix column name typo in Task.csv

4. **Clean Text Data:**
   - Trim leading/trailing spaces from all text fields
   - Fix misspellings (Safey → Safety)
   - Validate against database schema

5. **Data Validation:**
   - Verify task ID references in Task_Assignment.csv
   - Verify worker ID references are consistent
   - Check for circular dependencies in task predecessors
   - Validate date ranges (Start ≤ Finish)

### 15.7 Suggested Data Import Strategy

1. Fix CSV encoding (convert to UTF-8)
2. Run data cleaning scripts
3. Create intermediate staging table for bulk import
4. Import with deduplication logic
5. Validate referential integrity
6. Move to production tables

---

## 17. Creating an Executable File

This section provides comprehensive steps to create a standalone Windows executable (.exe) for Project Uno using PyInstaller.

### 17.1 Prerequisites

#### Install Dependencies
```powershell
# Install required Python packages
pip install mysql-connector-python matplotlib pyinstaller
```

#### Verify Installation
```powershell
# Check PyInstaller version
pyinstaller --version

# Verify packages
pip list | Select-String "mysql|matplotlib|pyinstaller"
```

### 17.2 Basic Executable Creation

#### Option A: Single-File Executable (Recommended for Distribution)
```powershell
# Navigate to project directory
cd C:\external-projects\Project-Management-System

# Create single-file executable
pyinstaller --onefile --windowed --name "ProjectUno" main.py
```

**Pros:**
- Single .exe file (easy distribution)
- Clean deployment (no folder structure)

**Cons:**
- Slower startup (extracts to temp folder)
- Larger file size (~80-120 MB)

#### Option B: Directory-Based Executable (Recommended for Development)
```powershell
# Create directory-based executable
pyinstaller --onedir --windowed --name "ProjectUno" main.py
```

**Pros:**
- Faster startup (no extraction needed)
- Easier debugging

**Cons:**
- Multiple files/folders to distribute
- Requires folder structure preservation

### 17.3 Advanced Configuration with Spec File

Create a custom `ProjectUno.spec` file for better control:

```python
# ProjectUno.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app', 'app'),                    # Include app package
        ('db_config.py', '.'),              # Include config files
        ('db_connection.py', '.'),
        ('docs', 'docs'),                   # Include CSV data files (optional)
    ],
    hiddenimports=[
        'mysql.connector',
        'mysql.connector.pooling',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'PIL',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest', 'unittest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ProjectUno',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                              # Compress executable (optional)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                         # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'                        # Custom icon (if available)
)
```

#### Build from Spec File
```powershell
pyinstaller ProjectUno.spec
```

### 17.4 Adding Application Icon

#### Create or Download Icon
1. Create a 256x256 PNG icon with construction theme (🏗)
2. Convert to .ico format using online tools (e.g., convertio.co)
3. Save as `icon.ico` in project root

#### Build with Icon
```powershell
pyinstaller --onefile --windowed --name "ProjectUno" --icon=icon.ico main.py
```

### 17.5 Database Configuration for Executable

#### Issue: Hardcoded Database Credentials
The executable will still require MySQL server running with credentials from `db_config.py`.

#### Solution Options:

**Option A: External MySQL (Recommended for Multi-User)**
Include instructions with executable:
1. Install MySQL or XAMPP
2. Create database and user:
   ```sql
   CREATE DATABASE project_uno;
   CREATE USER 'root'@'localhost' IDENTIFIED BY 'Rey_244456';
   GRANT ALL PRIVILEGES ON project_uno.* TO 'root'@'localhost';
   FLUSH PRIVILEGES;
   ```
3. Run executable

**Option B: MySQL Portable (Recommended for Single-User)**
Bundle XAMPP Portable with executable:
1. Download XAMPP Portable
2. Package with executable
3. Create startup script:
   ```powershell
   # start_project_uno.ps1
   Start-Process "xampp-portable\mysql\bin\mysqld.exe"
   Start-Sleep -Seconds 5
   Start-Process "ProjectUno.exe"
   ```

**Option C: SQLite Migration (Best for Portability)**
Convert application to use SQLite:
1. Replace `mysql.connector` with `sqlite3`
2. Update `db_connection.py` for SQLite syntax
3. No external database required
4. Database file bundled with executable

**Benefits of SQLite:**
- ✅ No installation required
- ✅ Single-file database (portable)
- ✅ No server management
- ✅ Perfect for standalone deployment

**SQLite Migration Steps:**
```python
# db_connection.py (SQLite version)
import sqlite3

class DatabaseConnection:
    def __init__(self, db_path='project_uno.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self._setup_schema()
    
    def execute_query(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
    
    def fetch_all(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
```

### 17.6 Build and Test

#### Full Build Process
```powershell
# 1. Clean previous builds
Remove-Item -Path "build", "dist" -Recurse -Force -ErrorAction SilentlyContinue

# 2. Build executable
pyinstaller ProjectUno.spec

# 3. Test executable
cd dist
.\ProjectUno.exe
```

#### Testing Checklist
- [ ] Application launches without errors
- [ ] Login screen appears correctly
- [ ] Database connection works
- [ ] All 4 views load properly
- [ ] KPI cards display data
- [ ] Charts render correctly (matplotlib)
- [ ] CRUD operations work
- [ ] CSV import functions properly
- [ ] Window sizing and resizing work
- [ ] Sidebar collapse/expand functions
- [ ] No console window appears

### 17.7 Distribution Packaging

#### Option A: Simple Zip Archive
```powershell
# For single-file executable
Compress-Archive -Path "dist\ProjectUno.exe" -DestinationPath "ProjectUno_v1.0.zip"

# For directory-based executable
Compress-Archive -Path "dist\ProjectUno" -DestinationPath "ProjectUno_v1.0.zip"
```

#### Option B: Installer Creation (Professional)
Use Inno Setup to create professional installer:

1. Download Inno Setup: https://jrsoftware.org/isinfo.php
2. Create setup script (`setup.iss`):

```ini
; ProjectUno_Setup.iss
[Setup]
AppName=Project Uno
AppVersion=1.0
DefaultDirName={pf}\ProjectUno
DefaultGroupName=Project Uno
OutputDir=.\installer
OutputBaseFilename=ProjectUno_Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\ProjectUno\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Project Uno"; Filename: "{app}\ProjectUno.exe"
Name: "{userdesktop}\Project Uno"; Filename: "{app}\ProjectUno.exe"

[Run]
Filename: "{app}\ProjectUno.exe"; Description: "Launch Project Uno"; Flags: postinstall nowait skipifsilent
```

3. Compile installer:
```powershell
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss
```

#### Option C: Portable Package
Create portable version with all dependencies:
```
ProjectUno_Portable/
├── ProjectUno.exe
├── README.txt           (usage instructions)
├── LICENSE.txt          (if applicable)
├── docs/                (sample CSV files)
│   └── *.csv
├── xampp-portable/      (optional: MySQL portable)
│   └── mysql/
└── start_with_mysql.bat (startup script)
```

### 17.8 Troubleshooting

#### Issue: "Import Error: No module named mysql.connector"
**Solution:** Add hidden import to spec file:
```python
hiddenimports=['mysql.connector', 'mysql.connector.pooling']
```

#### Issue: "Import Error: No module named matplotlib"
**Solution:** Add matplotlib to hidden imports:
```python
hiddenimports=['matplotlib', 'matplotlib.backends.backend_tkagg']
```

#### Issue: Charts don't render
**Solution:** Ensure backend is set in code before import:
```python
import matplotlib
matplotlib.use('TkAgg')  # Must be before other matplotlib imports
```

#### Issue: "FileNotFoundError: app/views/dashboard.py"
**Solution:** Add app package to datas in spec file:
```python
datas=[('app', 'app')]
```

#### Issue: Database connection fails in executable
**Solution:** Check:
1. MySQL server is running
2. Credentials in db_config.py match MySQL user
3. Firewall allows MySQL connection (port 3306)
4. User has permissions on project_uno database

#### Issue: Executable size is too large (>200 MB)
**Solutions:**
1. Exclude unnecessary packages:
   ```python
   excludes=['pytest', 'unittest', 'setuptools', 'pip']
   ```
2. Use UPX compression:
   ```python
   upx=True
   ```
3. Use --onefile mode (reduces total size)

#### Issue: Slow startup time (>10 seconds)
**Cause:** Single-file executable extracts to temp on each launch

**Solutions:**
1. Use --onedir mode instead
2. Reduce hidden imports to only essential modules
3. Consider PyInstaller bootloader optimizations

### 17.9 Deployment Best Practices

#### For End Users
1. **Create User Guide:**
   - Installation steps
   - Database setup instructions
   - Screenshot walkthrough
   - Troubleshooting FAQ

2. **Version Management:**
   ```
   ProjectUno_v1.0.zip
   ProjectUno_v1.1.zip
   ```

3. **Include Sample Data:**
   - Sample CSV files in docs/ folder
   - Pre-populated database (SQLite)
   - Tutorial project

#### For IT Deployment
1. **Silent Installation:**
   ```powershell
   ProjectUno_Setup.exe /SILENT /DIR="C:\Program Files\ProjectUno"
   ```

2. **Registry Configuration:**
   - Store database credentials in registry (encrypted)
   - Application settings persistence

3. **Network Deployment:**
   - Shared MySQL database on server
   - Environment variables for connection:
     ```powershell
     $env:PROJECT_UNO_DB_HOST = "192.168.1.100"
     $env:PROJECT_UNO_DB_USER = "project_uno"
     $env:PROJECT_UNO_DB_PASSWORD = "SecurePassword123"
     ```

### 17.10 Alternative Tools

#### PyInstaller Alternatives

**cx_Freeze:**
```powershell
pip install cx_Freeze
python setup.py build
```

**py2exe (Windows-only):**
```powershell
pip install py2exe
python setup.py py2exe
```

**Nuitka (Best Performance):**
```powershell
pip install nuitka
python -m nuitka --standalone --onefile --windows-disable-console main.py
```

**Comparison:**
| Tool | Size | Speed | Complexity |
|------|------|-------|------------|
| PyInstaller | Large | Medium | Easy |
| cx_Freeze | Medium | Medium | Medium |
| py2exe | Medium | Fast | Medium |
| Nuitka | Small | Very Fast | Complex |

**Recommendation:** PyInstaller for ease of use and reliability.

---

## 16. Summary

**Project Uno** is a desktop-based construction management application built with Python Tkinter. It provides essential project management features including task scheduling, resource management, material tracking, and worker assignment. The application uses MySQL for persistent data storage with automatic schema initialization. The GUI features a modern sidebar navigation system with view-based routing, KPI dashboard with charts, and comprehensive CRUD capabilities.

**Architecture:** The application has evolved to a well-organized modular structure:
- **Core:** ConstructionApp, MainFrame, LoginFrame (app/gui.py)
- **Navigation:** CollapsibleSidebar (220px / 64px) with icon-based navigation
- **Views:** 4 separate view modules (Dashboard, Tasks, Resources, Assignments)
- **Widgets:** Reusable components (KPICard, ScrollableTreeview)
- **Theme:** Centralized design system with color palette and typography
- **Charts:** Matplotlib integration for data visualization (bar chart, donut chart)

**Current Status:** Functional with hardcoded authentication and local database configuration. Data import from CSV files requires preprocessing due to encoding and format issues (see Section 15). Current environment lacks mysql-connector-python and matplotlib installations.

**Key Features:**
- ✅ Login authentication with themed interface
- ✅ Collapsible sidebar navigation (4 views)
- ✅ Dashboard with 6 KPI cards (color-coded metrics)
- ✅ Charts visualization (budget by task, materials distribution)
- ✅ Task monitoring (CRUD, search, CSV import)
- ✅ Resource management (workers and materials)
- ✅ Task assignment with joined data display
- ✅ Scrollable layouts with mouse wheel support
- ✅ Responsive window sizing (resizable, min 900×600)

**CSV Data Status:** 
- ✅ Task data ready for import (minor format fixes needed)
- ❌ Material data requires encoding conversion
- ⚠️ Worker data requires deduplication before import
- ⚠️ All cost data requires comma removal
- 📁 Additional CSV files found in docs/res/ folder

**Priority Actions:**
1. Resolve CSV encoding issues (Materials, Material Assignment, Materials Usage)
2. Deduplicate and clean Workers.csv
3. Implement data import pipeline with validation
4. Address authentication security (see Section 12)
5. Install missing dependencies (mysql-connector-python, matplotlib)
6. Consider SQLite migration for portable deployment (see Section 17.5)

**Executable Creation:** See Section 17 for comprehensive steps to create standalone Windows executable using PyInstaller, including database configuration options (external MySQL, MySQL Portable, or SQLite migration).

---

*Audit completed: May 28, 2026*
