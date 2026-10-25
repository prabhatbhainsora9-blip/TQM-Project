"""
Database Schema Initialization and Seed Data for Employee Management System (TQM Edition).
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Ensures all SQLite tables, indices, and constraints are established automatically.
Includes schema migration tracking and optional realistic TQM demonstration data.
"""

import sqlite3
from datetime import datetime
from typing import Optional

SCHEMA_VERSION = 1

CREATE_TABLES_SQL = """
-- Table 1: Employee Records
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_code TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    department TEXT NOT NULL,
    designation TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    date_of_joining TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Active', 'Inactive')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Table 2: TQM Defect Log & Checksheet
CREATE TABLE IF NOT EXISTS defects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    defect_code TEXT UNIQUE NOT NULL,
    date_detected TEXT NOT NULL,
    module TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('Low', 'Medium', 'High', 'Critical')),
    occurrence_count INTEGER NOT NULL DEFAULT 1,
    root_cause TEXT,
    corrective_action TEXT,
    status TEXT NOT NULL DEFAULT 'Open' CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
    resolution_date TEXT,
    verification_notes TEXT,
    created_at TEXT NOT NULL
);

-- Table 3: FMEA Risk Analysis
CREATE TABLE IF NOT EXISTS fmea_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_code TEXT UNIQUE NOT NULL,
    process_component TEXT NOT NULL,
    potential_failure_mode TEXT NOT NULL,
    potential_effects TEXT NOT NULL,
    potential_causes TEXT NOT NULL,
    current_controls TEXT NOT NULL,
    severity INTEGER NOT NULL CHECK(severity BETWEEN 1 AND 10),
    occurrence INTEGER NOT NULL CHECK(occurrence BETWEEN 1 AND 10),
    detection INTEGER NOT NULL CHECK(detection BETWEEN 1 AND 10),
    rpn INTEGER NOT NULL,
    recommended_action TEXT NOT NULL,
    responsible_person TEXT,
    status TEXT NOT NULL DEFAULT 'Open' CHECK(status IN ('Open', 'In Progress', 'Completed')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Table 4: PDCA Continuous Improvement Records
CREATE TABLE IF NOT EXISTS pdca_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    plan_problem TEXT NOT NULL,
    plan_baseline TEXT,
    plan_root_cause TEXT,
    plan_target TEXT,
    plan_action TEXT NOT NULL,
    plan_owner TEXT,
    plan_start_date TEXT,
    plan_target_date TEXT,
    do_action_taken TEXT,
    do_completion_date TEXT,
    do_notes TEXT,
    check_before_metric TEXT,
    check_after_metric TEXT,
    check_evidence TEXT,
    check_target_achieved TEXT DEFAULT 'Pending',
    act_standardization TEXT,
    act_lessons_learned TEXT,
    act_followup TEXT,
    act_status TEXT NOT NULL DEFAULT 'In Plan' CHECK(act_status IN ('In Plan', 'In Implementation', 'Under Evaluation', 'Standardized', 'Completed')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Table 5: Ishikawa / Fishbone Causes connected to problem statements
CREATE TABLE IF NOT EXISTS fishbone_causes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_title TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('People', 'Process', 'Software Code', 'Infrastructure')),
    cause_text TEXT NOT NULL,
    is_investigated INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

-- Table 6: System Audit Trail (Activity Logs persistence)
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,
    description TEXT NOT NULL,
    user TEXT NOT NULL DEFAULT 'Admin',
    module TEXT NOT NULL DEFAULT 'SYSTEM',
    level TEXT NOT NULL DEFAULT 'INFO'
);

-- Table 7: Schema Version Tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Indices for rapid query performance
CREATE INDEX IF NOT EXISTS idx_employees_code ON employees(employee_code);
CREATE INDEX IF NOT EXISTS idx_employees_email ON employees(email);
CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department);
CREATE INDEX IF NOT EXISTS idx_employees_status ON employees(status);
CREATE INDEX IF NOT EXISTS idx_defects_category ON defects(category);
CREATE INDEX IF NOT EXISTS idx_defects_status ON defects(status);
CREATE INDEX IF NOT EXISTS idx_fmea_rpn ON fmea_records(rpn DESC);
"""


def initialize_database(conn: sqlite3.Connection) -> None:
    """Initializes tables, indices, and baseline schema migration record."""
    cursor = conn.cursor()
    cursor.executescript(CREATE_TABLES_SQL)

    # Check migration version
    cursor.execute("SELECT version FROM schema_migrations WHERE version = ?", (SCHEMA_VERSION,))
    if not cursor.fetchone():
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO schema_migrations (version, applied_at, description) VALUES (?, ?, ?)",
            (SCHEMA_VERSION, now_str, "Initial baseline schema with employees, TQM, and audit tables.")
        )
    conn.commit()


def seed_sample_data(conn: sqlite3.Connection, clear_existing: bool = False) -> None:
    """
    Populates clearly marked demonstration data for academic viva and evaluation.
    Only seeds if table is empty or clear_existing=True.
    """
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Employees Sample Data
    cursor.execute("SELECT COUNT(*) FROM employees")
    emp_count = cursor.fetchone()[0]

    if clear_existing or emp_count == 0:
        if clear_existing:
            cursor.execute("DELETE FROM employees")

        sample_employees = [
            ("EMP-1001", "Aarav Sharma", "Engineering", "Senior Software Engineer", "aarav.sharma@example.com", "+91 9876543210", "2023-01-15", "Active"),
            ("EMP-1002", "Priya Patel", "Quality Assurance", "QA Lead", "priya.patel@example.com", "+91 9876543211", "2023-03-01", "Active"),
            ("EMP-1003", "Rohan Verma", "Engineering", "Backend Developer", "rohan.verma@example.com", "+91 9876543212", "2023-06-10", "Active"),
            ("EMP-1004", "Ananya Iyer", "Human Resources", "HR Generalist", "ananya.iyer@example.com", "+91 9876543213", "2022-11-20", "Active"),
            ("EMP-1005", "Vikram Malhotra", "Operations", "Operations Manager", "vikram.malhotra@example.com", "+91 9876543214", "2021-08-05", "Active"),
            ("EMP-1006", "Sneha Roy", "Finance", "Senior Financial Analyst", "sneha.roy@example.com", "+91 9876543215", "2022-04-18", "Active"),
            ("EMP-1007", "Kavita Reddy", "Quality Assurance", "SQC Specialist", "kavita.reddy@example.com", "+91 9876543216", "2024-02-01", "Active"),
            ("EMP-1008", "Manish Joshi", "Information Technology", "System Administrator", "manish.joshi@example.com", "+91 9876543217", "2022-09-12", "Active"),
            ("EMP-1009", "Neha Kapoor", "Marketing", "Brand Strategist", "neha.kapoor@example.com", "+91 9876543218", "2024-05-15", "Active"),
            ("EMP-1010", "Devendra Singh", "Engineering", "DevOps Engineer", "devendra.singh@example.com", "+91 9876543219", "2023-08-22", "Inactive"),
            ("EMP-1011", "Meera Nambiar", "Research & Development", "Data Scientist", "meera.nambiar@example.com", "+91 9876543220", "2024-01-10", "Active"),
            ("EMP-1012", "Arjun Bhatia", "Operations", "Process Coordinator", "arjun.bhatia@example.com", "+91 9876543221", "2023-11-05", "Inactive"),
        ]
        cursor.executemany(
            """
            INSERT OR IGNORE INTO employees
            (employee_code, full_name, department, designation, email, phone, date_of_joining, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [(c, n, d, des, e, p, doj, s, now_str, now_str) for c, n, d, des, e, p, doj, s in sample_employees]
        )

    # 2. Defect Log Sample Data (Realistic TQM defect occurrences across categories)
    cursor.execute("SELECT COUNT(*) FROM defects")
    defect_count = cursor.fetchone()[0]

    if clear_existing or defect_count == 0:
        if clear_existing:
            cursor.execute("DELETE FROM defects")

        sample_defects = [
            ("DEF-001", "2026-09-01", "Employee Form", "Missing email syntax validation allowed malformed string", "Validation Error", "High", 18, "Unchecked regex in front-end form", "Implemented RFC-compliant regex in validation_service", "Resolved", "2026-09-03", "Verified unit tests pass"),
            ("DEF-002", "2026-09-05", "Employee Form", "Phone number length under 10 digits accepted", "Validation Error", "Medium", 14, "Length boundary condition omitted", "Added length 10-15 digits constraint", "Resolved", "2026-09-06", "All phone test cases green"),
            ("DEF-003", "2026-09-08", "Database Layer", "Database lock during concurrent report generation", "Database Error", "High", 9, "Default journal mode was rollback delete", "Enabled WAL mode and connection pooling", "Resolved", "2026-09-10", "Tested concurrent reads/writes"),
            ("DEF-004", "2026-09-12", "UI Theme", "Dark mode contrast ratio insufficient on header text", "UI Glitch", "Low", 7, "Hex color mismatch with CustomTkinter Dark theme", "Standardized color tokens in theme.py", "Resolved", "2026-09-13", "Visual check passed"),
            ("DEF-005", "2026-09-15", "Export Engine", "PDF export truncated long department names", "Report Formatting", "Medium", 6, "Fixed cell width in ReportLab table layout", "Implemented dynamic colWidths and wrapping", "Resolved", "2026-09-16", "Export verified"),
            ("DEF-006", "2026-09-20", "Data Layer", "Duplicate employee code error gave raw SQLite traceback", "Data Inconsistency", "High", 4, "UniqueConstraintException not caught cleanly", "Handled IntegrityError with friendly modal message", "Resolved", "2026-09-21", "Verified Poka-Yoke error handling"),
            ("DEF-007", "2026-09-25", "Search Filter", "Query latency exceeded 200ms with unindexed search", "Performance Lag", "Medium", 3, "Missing SQLite indices on code and email", "Added index idx_employees_code & idx_employees_email", "Resolved", "2026-09-26", "Query time dropped to <5ms"),
            ("DEF-008", "2026-10-02", "Settings Module", "Window scaling reset on application restart", "UI Glitch", "Low", 2, "Config save omitted scaling key in dict", "Updated ConfigurationService save handler", "Resolved", "2026-10-03", "Persistent across restarts"),
            ("DEF-009", "2026-10-10", "Employee Table", "Pagination label showed page 0 when dataset was empty", "UI Glitch", "Low", 2, "Zero records boundary division error", "Added empty state guard condition", "Resolved", "2026-10-11", "Tested with 0 records"),
            ("DEF-010", "2026-10-15", "Logging", "Log file grew above 5MB without rotation", "Maintenance Issue", "Medium", 1, "RotatingFileHandler missing maxBytes argument", "Configured RotatingFileHandler with 1MB limit & 5 backups", "Resolved", "2026-10-16", "Rotation verified")
        ]
        cursor.executemany(
            """
            INSERT OR IGNORE INTO defects
            (defect_code, date_detected, module, description, category, severity, occurrence_count, root_cause, corrective_action, status, resolution_date, verification_notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [(c, dt, m, d, cat, s, occ, rc, ca, st, rd, vn, now_str) for c, dt, m, d, cat, s, occ, rc, ca, st, rd, vn in sample_defects]
        )

    # 3. FMEA Sample Records (With Severity, Occurrence, Detection and calculated RPN)
    cursor.execute("SELECT COUNT(*) FROM fmea_records")
    fmea_count = cursor.fetchone()[0]

    if clear_existing or fmea_count == 0:
        if clear_existing:
            cursor.execute("DELETE FROM fmea_records")

        # RPN = S * O * D
        sample_fmea = [
            ("FMEA-01", "Database Persistence", "Database file corruption or accidental deletion", "Total loss of employee records and audit logs", "Sudden power interruption, ungraceful exit", "WAL mode enabled, synchronous NORMAL", 9, 3, 4, 9*3*4, "Implement automatic startup backup and backup manager", "Prabhat S. (QA)", "Completed"),
            ("FMEA-02", "Employee Registration", "Duplicate Employee Code entered by operator", "Data duplication, incorrect salary/attendance mapping", "Operator typo or lack of immediate unique check", "SQLite UNIQUE constraint on employee_code", 7, 5, 3, 7*5*3, "Add pre-insert uniqueness validation and Poka-Yoke warning", "Prabhat S. (Lead)", "Completed"),
            ("FMEA-03", "Configuration Management", "Corrupted or missing config.json file", "Application fails to launch or crashes with JSONDecodeError", "Manual editing typo or unexpected disk write failure", "Try/except fallback in configuration_service", 8, 4, 2, 8*4*2, "Self-healing config: restore safe defaults on read failure", "Prabhat S. (Dev)", "Completed"),
            ("FMEA-04", "Input Validation", "Invalid email format or phone format accepted", "Communication delivery failure, bad contact records", "Insufficient client-side regex check", "RFC regex in validation_service", 6, 6, 2, 6*6*2, "Centralize validation service with comprehensive unit tests", "QA Team", "Completed"),
            ("FMEA-05", "Activity Logging", "Log file unbounded growth exhausts local disk space", "System slowdown, disk full alert", "Standard FileHandler used without rotation", "RotatingFileHandler with 1MB limit", 7, 3, 3, 7*3*3, "Add log retention policy and log viewer in admin UI", "DevOps Admin", "Completed"),
            ("FMEA-06", "Reporting & Export", "Report generation freezes UI on large dataset", "Application appears unresponsive to user", "Synchronous PDF generation on GUI main thread", "Progress indicators", 5, 4, 3, 5*4*3, "Ensure lightweight operations and background workers for large PDF jobs", "UI Team", "Completed"),
        ]
        cursor.executemany(
            """
            INSERT OR IGNORE INTO fmea_records
            (item_code, process_component, potential_failure_mode, potential_effects, potential_causes, current_controls, severity, occurrence, detection, rpn, recommended_action, responsible_person, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [(code, comp, mode, eff, cause, ctrl, s, o, d, rpn, act, resp, st, now_str, now_str) for code, comp, mode, eff, cause, ctrl, s, o, d, rpn, act, resp, st in sample_fmea]
        )

    # 4. PDCA Sample Records
    cursor.execute("SELECT COUNT(*) FROM pdca_records")
    pdca_count = cursor.fetchone()[0]

    if clear_existing or pdca_count == 0:
        if clear_existing:
            cursor.execute("DELETE FROM pdca_records")

        sample_pdca = [
            (
                "PDCA-01",
                "Reduction of Input Validation Errors via Poka-Yoke",
                "Users encountered 32 validation errors per 100 entries due to unassisted manual text fields.",
                "32 validation rejections per 100 employee entries",
                "Absence of proactive real-time formatting guidance and strict pre-commit validation",
                "< 5 validation rejections per 100 entries (< 85% reduction)",
                "Introduce centralized ValidationService with regex checks, department dropdown, and friendly Poka-Yoke hints.",
                "Prabhat Singh Bhainsora",
                "2026-09-01",
                "2026-09-15",
                "Created validation_service.py with RFC email regex, digit length enforcement, and dropdown widgets.",
                "2026-09-12",
                "Form testing executed with 150 simulated edge-case inputs.",
                "32% failure rate",
                "2.1% failure rate",
                "Defect logs show validation failures dropped from 32 to 3 across 140 sample operations.",
                "Yes - Target Exceeded",
                "Enforce validation_service across all form sub-components and automated CI test suite.",
                "Clear error messages and proactive UI dropdowns eliminate over 90% of user data entry defects.",
                "Implement phone number auto-masking in version 1.1.",
                "Standardized"
            ),
            (
                "PDCA-02",
                "Database Resilience and Zero-Data-Loss Architecture",
                "Application risk of database locking and missing automated recovery mechanisms during power failures.",
                "0 automated backups; standard rollback journal vulnerable to sudden termination",
                "SQLite default configuration lacking WAL mode and scheduled snapshot routine",
                "Zero data loss; backup restoration time < 10 seconds",
                "Enable SQLite Write-Ahead Logging (WAL) mode; create modular BackupService with single-click restore.",
                "Database Sub-team",
                "2026-09-16",
                "2026-09-30",
                "Implemented WAL PRAGMA in connection.py; added automated backup_service with integrity checks.",
                "2026-09-25",
                "Simulated forced process termination during active insert transaction.",
                "0 automated recovery checkpoints",
                "100% data recovery within 3 seconds using backup snapshot",
                "Integrity checks passed with 0 corrupt blocks across 50 stress iterations.",
                "Yes - Target Exceeded",
                "Integrate backup verification into application startup health check.",
                "WAL mode significantly increases concurrency and prevents read locks during reporting.",
                "Add compressed ZIP archiving for backups older than 30 days.",
                "Standardized"
            )
        ]
        cursor.executemany(
            """
            INSERT OR IGNORE INTO pdca_records
            (cycle_code, title, plan_problem, plan_baseline, plan_root_cause, plan_target, plan_action, plan_owner, plan_start_date, plan_target_date, do_action_taken, do_completion_date, do_notes, check_before_metric, check_after_metric, check_evidence, check_target_achieved, act_standardization, act_lessons_learned, act_followup, act_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [(c, t, p, b, rc, tg, pa, po, psd, ptd, dat, dcd, dn, cbm, cam, ce, cta, as_, all_, af, ast, now_str, now_str) for c, t, p, b, rc, tg, pa, po, psd, ptd, dat, dcd, dn, cbm, cam, ce, cta, as_, all_, af, ast in sample_pdca]
        )

    # 5. Fishbone Root Cause Sample Data
    cursor.execute("SELECT COUNT(*) FROM fishbone_causes")
    fb_count = cursor.fetchone()[0]

    if clear_existing or fb_count == 0:
        if clear_existing:
            cursor.execute("DELETE FROM fishbone_causes")

        sample_fishbone = [
            ("High Employee Registration Data Errors", "People", "Lack of operator training on standardized date formats (YYYY-MM-DD)", 1),
            ("High Employee Registration Data Errors", "People", "Typing fatigue during bulk employee batch entries", 0),
            ("High Employee Registration Data Errors", "Process", "Absence of real-time Poka-Yoke feedback before form submission", 1),
            ("High Employee Registration Data Errors", "Process", "Manual dual-entry from paper hiring forms", 0),
            ("High Employee Registration Data Errors", "Software Code", "Front-end lacked RFC-compliant email regex checking", 1),
            ("High Employee Registration Data Errors", "Software Code", "No client-side check for duplicate employee code prior to DB insert", 1),
            ("High Employee Registration Data Errors", "Infrastructure", "Intermittent local network latency during database save", 0),
            ("High Employee Registration Data Errors", "Infrastructure", "Unregulated display scaling distorting error message dialogs", 1)
        ]
        cursor.executemany(
            """
            INSERT INTO fishbone_causes (problem_title, category, cause_text, is_investigated, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            [(pt, cat, ct, inv, now_str) for pt, cat, ct, inv in sample_fishbone]
        )

    conn.commit()
