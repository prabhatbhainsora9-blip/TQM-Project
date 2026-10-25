# User Manual and Operator Guide
## Employee Management System with Maintainability Enhancement and TQM Quality Analysis

**Document Version:** 1.0.0  
**Student Name:** Prabhat Singh Bhainsora  
**Roll Number:** 2410302046  
**Course Code:** BBAT104 — Fundamentals of Total Quality Management  
**Quality Goal:** Q11 — Improve Maintainability  

---

## 1. System Requirements & Installation

### 1.1 Hardware Requirements
- **Processor:** 1.6 GHz or faster dual-core x64 CPU.
- **RAM:** Minimum 2 GB (4 GB recommended).
- **Storage:** Minimum 150 MB free disk space.
- **Display Resolution:** 1280 × 720 minimum (1920 × 1080 recommended).
- **OS:** Windows 10 or Windows 11.

### 1.2 Software Requirements
- **Python:** Python 3.10, 3.11, or 3.12.
- **Dependencies:** Listed in `requirements.txt` (CustomTkinter, Pandas, Matplotlib, ReportLab, OpenPyXL, Pytest).

### 1.3 Quick Start Instructions
1. Open a terminal or PowerShell in the project directory:
   ```powershell
   cd c:\Users\bhain\TQM-Project
   ```
2. (Optional) Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install required dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Launch the desktop application:
   ```powershell
   python main.py
   ```
   *Alternative:* Double-click `run.bat` in Windows File Explorer.

---

## 2. Navigating the Interface

The desktop window is structured into two primary areas:
- **Left Navigation Sidebar:** Accesses Dashboard, Employees, Add Employee, Defect Log, FMEA Risk Analysis, SQC Charts, PDCA Tracker, Reports, Activity Logs, System Settings, and Help.
- **Central Main Content Area:** Dynamic workspace that displays views without screen flickering.

---

## 3. Core Modules Step-by-Step

### 3.1 Executive Dashboard
- **KPI Stat Cards:** View real-time counts for Total Employees, Active Staff, Inactive Staff, Open Defects, High-Risk FMEA items ($RPN \ge 120$), and Active PDCA Cycles.
- **Department Distribution:** Visual breakdown of employee count per department.
- **Recent Activity:** Quick preview of the most recently registered employees.
- **Quick Shortcuts:** Direct buttons to register employees, record defects, or generate reports.

### 3.2 Managing Employees (CRUD)
- **Adding an Employee:**
  1. Click **"+ New Employee"** from the toolbar or sidebar.
  2. Enter Employee Code (e.g., `EMP-1050`), Full Name, select Department from the dropdown, Designation, Email, Phone (10+ digits), Date of Joining (`YYYY-MM-DD`), and Status.
  3. Click **"Create Employee"**. If validation fails (e.g. malformed email or duplicate code), a red warning will display above the form.
- **Editing an Employee:**
  1. Locate the employee in the table and click the blue **"Edit"** button.
  2. Modify required fields and click **"Save Changes"**.
- **Deleting an Employee:**
  1. Click the red **"Delete"** button next to an employee.
  2. Confirm the safety dialog ("Are you sure you want to permanently delete...?").
- **Searching & Filtering:**
  1. Type any search keyword (name, code, email, designation) in the search box and press Enter.
  2. Filter by Department or Status using the dropdown selectors.
- **Pagination & Sorting:**
  1. Click any column header with the `↕` symbol to toggle Ascending/Descending sort.
  2. Use the `<<`, `< Prev`, `Next >`, `>>` buttons in the footer to navigate pages.

### 3.3 TQM Defect Log & Checksheet
- **Logging a Defect:** Click **"+ Log Quality Defect"**, select Module, Category, Severity (Critical, High, Medium, Low), count, and root cause.
- **Resolving a Defect:** Click **"Resolve"** on an active defect, record corrective action and verification notes, and change status to `Resolved`.
- **Checksheet Summary:** The top panel automatically aggregates total observations per defect category and highlights critical counts without double counting.

### 3.4 FMEA Risk Analysis (Failure Mode & Effects Analysis)
- **Understanding RPN:** $RPN = \text{Severity} \times \text{Occurrence} \times \text{Detection}$.
- **Rating Scales:** Each factor is rated from 1 (lowest risk) to 10 (highest risk / most difficult detection).
- **High-Risk Threshold:** Any item with $RPN \ge 120$ is highlighted in red.
- **Adding an Item:** Click **"+ Add FMEA Item"**, enter failure mode details, and adjust the three interactive score sliders. The RPN calculation previews in real time.

### 3.5 Interactive SQC Charts
- **Pareto Chart (80/20):** Displays bars ordered descending by defect frequency with a red cumulative percentage curve and an amber 80% vital few benchmark line.
- **Fishbone Diagram:** Visualizes investigated and suspected causes across People, Process, Software Code, and Infrastructure.
- **SIPOC Map:** Illustrates the 5-column employee data lifecycle from Suppliers to Customers.
- **CTQ Tree:** Shows decomposition of user needs into measurable quality drivers.
- **Exporting Charts:** Click **"Export Chart (PNG)"** to save a 200 DPI image into the `reports/` folder.

### 3.6 PDCA Continuous Improvement Tracker
- **Creating a Cycle:** Click **"+ New PDCA Cycle"** and document the problem statement, baseline metric, target metric, and proposed action plan.
- **Updating Phases:** Click **"View/Edit"** on a cycle to log action taken (Do), compare before-and-after metrics (Check), and record standardization notes (Act).

### 3.7 Generating Reports & Exports
- In the **Reports** view, click:
  - **"Generate PDF"** for audit-ready PDF documents formatted with ReportLab.
  - **"Export Excel (.xlsx)"** for multi-column spreadsheets.
  - **"Export CSV"** for raw tabular data.
- Click **"Open Reports Folder"** to open Windows Explorer directly to the output directory.

### 3.8 System Settings (Q11 Feature 3)
- **Theme Selection:** Toggle between **Dark**, **Light**, and **System** appearance modes.
- **Scaling:** Adjust interface scaling between 90%, 100%, 110%, and 120%.
- **Records per Page:** Select 5, 10, 20, 50, or 100 records per table page.
- **Reset to Defaults:** Reverts all configurations back to safe factory settings.

### 3.9 Activity Logs (Q11 Feature 4)
- View timestamped audit logs recorded by Python's `RotatingFileHandler`.
- Filter entries by log level (`ALL`, `INFO`, `WARNING`, `ERROR`, `DEBUG`) or search by keyword.
- Click **"Export Log Copy"** to extract a plaintext copy for administrative auditing.

### 3.10 Database Backups & Disaster Recovery
- In **System Settings**, click **"Create Backup Snapshot"** to generate an atomic timestamped `.db` backup in `backups/`.
- Click **"List / Restore Backups"** to inspect backup sizes, verify SQLite integrity, and restore from an earlier snapshot. A pre-restore safety copy is created automatically before overwriting.

---

## 4. Troubleshooting Guide

| Problem | Probable Cause | Corrective Action |
| :--- | :--- | :--- |
| **Window scaling appears blurry** | Windows OS display scaling mismatch | Adjust UI scaling dropdown in System Settings to 100% or 110%. |
| **"Employee Code already exists" error** | Duplicate primary key entered | Use a unique identifier (e.g. `EMP-1025`). Poka-Yoke blocks duplicates. |
| **Missing reports or logs directory** | Accidentally deleted workspace folders | Restart application. `Application._ensure_directories()` recreates them automatically. |
| **"Invalid email format" error** | Email missing `@` or domain suffix | Ensure email matches RFC pattern (e.g. `name@domain.com`). |
| **Database appears empty on clean clone** | Initial startup state | Click "Seed Demo Data" in Employee view or restart to trigger initial seeding. |
