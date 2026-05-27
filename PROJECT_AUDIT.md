# Project Uno - Construction Management Application
## Comprehensive Audit Report
**Date:** May 27, 2026

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
project_uno_app/
├── app.py                 # Main entry point (alternative wrapper)
├── main.py                # Primary entry point
├── db_config.py           # Database configuration settings
├── db_connection.py       # Database connection manager
├── requirements.txt       # Python dependencies
├── inspect.txt            # Binary inspection file (non-functional)
├── app/
│   ├── __init__.py        # Package initialization
│   └── gui.py             # Main GUI application components
└── PROJECT_AUDIT.md       # This audit document
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

### 3.3 Database Module

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

#### `app/__init__.py`
- **Purpose:** Package marker file
- **Content:** Package documentation comment

#### `app/gui.py`
- **Purpose:** Complete GUI application implementation
- **Size:** ~800+ lines of code
- **Contains 7 Classes:** (see section 4.2)

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
MainFrame with 4 tabs
    ├── Dashboard
    ├── Task Monitoring
    ├── Resource Management
    └── Task Assignment
```

### 4.2 GUI Components (Classes in gui.py)

#### 1. **LoginFrame** (ttk.Frame)
- **Purpose:** Authentication layer
- **Features:**
  - Blue and white themed login form
  - Username/password fields
  - Hardcoded credentials validation (reysosmena / Rey244456)
  - Displays error messages for invalid credentials
  - Enter key support for form submission
- **UI Elements:**
  - Title: "Construction Management Login"
  - Input fields for username and password
  - Login button with event binding

#### 2. **DashboardTab** (ttk.Frame)
- **Purpose:** Overview of all project data
- **Features:**
  - 6 data tables (Treeviews) with search capability
  - Search functionality by task description/WBS code
  - Refresh button for manual data reload
  - Scrollable tables with headers
- **Displays:**
  1. Material Assignment and Cost
  2. Materials Usage
  3. Materials
  4. Tasks
  5. Workers
  6. Task Assignments
- **Functionality:**
  - `search_tasks()` - Search by description or WBS code
  - `refresh_all_tables()` - Reload all data from database
  - `_load_*()` methods - Individual table data loaders

#### 3. **TaskMonitoringTab** (ttk.Frame)
- **Purpose:** Task creation, search, and management
- **Features:**
  - Add new tasks with form validation
  - Search tasks by description or Task ID
  - Delete tasks functionality
  - Task selection with status display
- **Form Fields:**
  - WBS Code (required)
  - Task Description (required)
  - Duration (integer validation)
  - Start Date (YYYY-MM-DD format)
  - Finish Date (YYYY-MM-DD format)
  - Predecessors (optional)
- **Validation Methods:**
  - `_validate_integer()` - Ensures integer inputs
  - `_validate_date()` - Validates YYYY-MM-DD format
- **Operations:**
  - Add Task
  - Search by Description
  - Search by Task ID
  - Delete Task

#### 4. **ResourceManagementTab** (ttk.Frame)
- **Purpose:** Manage workers and materials
- **Left Panel - Workers:**
  - Worker list (Treeview)
  - Add new worker
  - Update existing worker
  - Remove worker
  - Selectable form (Name, Position)
- **Right Panel - Materials:**
  - Materials overview table
  - Display columns: MaterialID, Materials, Quantity, Unit, Cost
- **Operations:**
  - `add_worker()` - Insert new worker
  - `update_worker()` - Modify worker details
  - `remove_worker()` - Delete worker
  - `load_workers()` - Populate worker list
  - `load_materials()` - Populate materials list

#### 5. **TaskAssignmentTab** (ttk.Frame)
- **Purpose:** Assign workers to tasks
- **Features:**
  - Dropdown selectors for tasks and workers
  - Assign worker to task
  - View all current assignments
  - Delete assignments
  - Assignment list with joined data
- **Operations:**
  - `add_assignment()` - Create task-worker assignment
  - `delete_assignment()` - Remove assignment
  - `refresh_assignments()` - Reload assignment data
  - `load_task_options()` - Populate task dropdown
  - `load_worker_options()` - Populate worker dropdown

#### 6. **MainFrame** (ttk.Frame)
- **Purpose:** Container for all tabbed content
- **Features:**
  - Tabbed notebook interface
  - Integrates all 4 main tabs
  - Consistent styling across application
  - Window sizing: 1180x760 pixels (non-resizable)
- **Tabs:**
  - Dashboard
  - Task Monitoring
  - Resource Management
  - Task Assignment

#### 7. **ConstructionApp** (ttk.Frame)
- **Purpose:** High-level application controller
- **Responsibilities:**
  - Window initialization and setup
  - Database connection management
  - Login/logout flow
  - Application lifecycle
- **Key Methods:**
  - `show_main_interface()` - Switch from login to main app
  - `refresh_dashboard()` - Update dashboard when data changes
  - `close()` - Cleanup and close application

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

### Libraries Used
```python
import tkinter as tk                      # GUI framework
from tkinter import ttk, messagebox       # Widgets and dialogs
from datetime import datetime             # Date handling
import mysql.connector                    # Database connection
import logging                            # Error logging
import os                                 # Environment variables
```

### UI Framework
- **Tkinter (ttk)** - Standard Python GUI toolkit
- **Themed widgets** (ttk) for modern appearance
- **Color scheme:** Blue (#1f4e79) and white (#e7f0ff)

### Database
- **MySQL** (required to be running)
- **Default port:** 3306
- **Autocommit:** Disabled (manual transaction control)
- **Dictionary cursors:** Enabled (field access by name)

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

- **Window Size:** 1180 × 760 pixels (fixed, non-resizable)
- **Window Title:** "Project Uno - Login" (changes to "Project Uno - Construction Manager" after login)
- **Theme:** Default Tkinter theme with custom styling
- **Font:** Segoe UI (11-12pt regular, 16pt bold for headings, 18pt bold for titles)

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

### Areas for Enhancement
- [ ] Implement role-based access control
- [ ] Add database authentication layer
- [ ] Implement audit logging
- [ ] Add data export functionality
- [ ] Implement budget tracking/reporting
- [ ] Add task progress tracking
- [ ] Implement material inventory alerts
- [ ] Add user management interface
- [ ] Implement backup/restore functionality

---

## 13. File Dependencies Graph

```
main.py / app.py
    ↓
ConstructionApp (from app.gui)
    ↓
├── LoginFrame (from app.gui)
├── MainFrame (from app.gui)
│   ├── DashboardTab
│   ├── TaskMonitoringTab
│   ├── ResourceManagementTab
│   └── TaskAssignmentTab
│
└── DatabaseConnection (from db_connection)
    ├── db_config.DB_CONFIG
    └── mysql.connector
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

## 16. Summary

**Project Uno** is a desktop-based construction management application built with Python Tkinter. It provides essential project management features including task scheduling, resource management, material tracking, and worker assignment. The application uses MySQL for persistent data storage with automatic schema initialization. The GUI presents information through a multi-tab interface with search and CRUD capabilities.

**Current Status:** Functional with hardcoded authentication and local database configuration. Data import from CSV files requires preprocessing due to encoding and format issues (see Section 15).

**CSV Data Status:** 
- ✅ Task data ready for import (minor format fixes needed)
- ❌ Material data requires encoding conversion
- ⚠️ Worker data requires deduplication before import
- ⚠️ All cost data requires comma removal

**Priority Actions:**
1. Resolve CSV encoding issues (Materials, Material Assignment, Materials Usage)
2. Deduplicate and clean Workers.csv
3. Implement data import pipeline with validation
4. Address authentication security (see Section 12)

---

*Audit completed: May 27, 2026*
