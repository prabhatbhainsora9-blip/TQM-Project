# Software Requirements Specification (SRS)
## Employee Management System with Maintainability Enhancement and TQM-Based Quality Analysis

**Document Version:** 1.0.0  
**Course Code:** BBAT104  
**Course Name:** Fundamentals of Total Quality Management (TQM)  
**Academic Session:** 2026–27  
**Student Name:** Prabhat Singh Bhainsora  
**Roll / Registration Number:** 2410302046  
**Branch & Section:** Computer Science & Engineering (CSE) — Section B  
**Assigned Quality Goal:** Q11 — Improve Maintainability  
**Baseline System:** Employee Management System  
**Target Repository:** `BBAT104_TQM_2410302046`

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) establishes the complete functional and non-functional requirements for the **Employee Management System (TQM Edition)**. The software serves dual objectives:
1. Providing an administrative desktop system for managing the complete lifecycle of organizational employee records (CRUD, searching, filtering, and reporting).
2. Demonstrating the practical integration of Total Quality Management (TQM) and Statistical Quality Control (SQC) tools, focusing specifically on **Q11: Improve Maintainability**.

### 1.2 Scope
The desktop system provides local, persistent, secure employee records management on Windows operating systems using Python 3.x, CustomTkinter, SQLite3, Pandas, and Matplotlib. It requires no remote cloud dependencies, external database servers, or subscription keys. Built-in quality modules include Failure Mode and Effects Analysis (FMEA), SIPOC Process Mapping, Critical to Quality (CTQ) Trees, Defect Checksheets, Pareto 80/20 Analysis, Ishikawa (Fishbone) Root-Cause Modeling, and Deming Plan-Do-Check-Act (PDCA) Continuous Improvement tracking.

### 1.3 Definitions, Acronyms, and Abbreviations
- **TQM:** Total Quality Management
- **SQC:** Statistical Quality Control
- **FMEA:** Failure Mode and Effects Analysis
- **RPN:** Risk Priority Number ($RPN = \text{Severity} \times \text{Occurrence} \times \text{Detection}$)
- **SIPOC:** Suppliers, Inputs, Process, Outputs, Customers
- **CTQ:** Critical to Quality
- **PDCA:** Plan – Do – Check – Act (Deming Cycle)
- **Poka-Yoke:** Japanese term for mistake-proofing or error prevention
- **ACID:** Atomicity, Consistency, Isolation, Durability
- **WAL:** Write-Ahead Logging (SQLite journal mode)

---

## 2. Overall Description

### 2.1 Product Perspective
The system operates as an autonomous desktop client with a local embedded SQLite database. It is partitioned into five distinct architectural tiers:
- **Presentation Tier:** CustomTkinter desktop UI with responsive dark/light theme switching, data tables, and embedded Matplotlib canvases.
- **Service / Business Logic Tier:** Manages employee operations, validation rules, TQM calculations, and report pipelines.
- **Analytics & SQC Tier:** Dual-axis Pareto chart generators, Ishikawa fishbone renderers, and checksheet aggregators.
- **Persistence Tier:** SQLite3 database configured with Write-Ahead Logging (WAL) and foreign key enforcement.
- **Configuration & Logging Tier:** `config.json` configuration manager and `RotatingFileHandler` activity audit trail.

### 2.2 User Characteristics
- **HR Operators:** Perform employee onboarding, record updates, and status toggles.
- **Quality Assurance Leads / Auditors:** Track defect occurrences, conduct FMEA reviews, and monitor PDCA cycles.
- **Academic Evaluators:** Review software architecture, verify Q11 maintainability features, inspect test coverage, and assess viva readiness.

---

## 3. Functional Requirements

### 3.1 Employee Management Module
- **FR-EMP-01 (Create):** The system shall provide an employee registration form validating code uniqueness, non-empty full name, controlled department vocabulary, designation, RFC-compliant email, 10–15 digit phone number, ISO 8601 joining date (`YYYY-MM-DD`), and status (`Active`/`Inactive`).
- **FR-EMP-02 (Read & Pagination):** The system shall display employee records in a paginated, sortable table supporting configurable records-per-page limits (5, 10, 20, 50, 100).
- **FR-EMP-03 (Update):** The system shall allow selecting an existing employee, populating the form with current values, validating modifications, and persisting updates with audit logging.
- **FR-EMP-04 (Delete with Confirmation):** The system shall require explicit confirmation prior to permanent record deletion.
- **FR-EMP-05 (Search & Filter):** The system shall perform real-time parameterized searches across employee code, name, designation, department, and email, combined with department and status dropdown filters.

### 3.2 Mandatory Q11 Maintainability Features
- **FR-Q11-01 (Modular Structure):** The system shall be structured into strictly decoupled packages: `database`, `models`, `services`, `analytics`, `ui`, and `tests`.
- **FR-Q11-02 (Configuration Files):** The system shall externalize application parameters to `config.json` and automatically recover with safe defaults if the file is absent or malformed.
- **FR-Q11-03 (System Settings):** The system shall provide a dedicated settings screen allowing users to dynamically modify themes, UI scaling, pagination limits, and backup preferences.
- **FR-Q11-04 (Activity Logs):** The system shall log all startup, CRUD, validation error, backup, and shutdown events using a rotating log file with a dedicated UI Log Viewer.
- **FR-Q11-05 (Documentation & Comments):** The codebase shall maintain descriptive docstrings, type annotations, architectural diagrams, and user manuals.

### 3.3 TQM & Statistical Quality Control Modules
- **FR-TQM-01 (FMEA Risk Register):** The system shall calculate RPN ($S \times O \times D$) on a 1–10 scale and automatically highlight high-risk failure modes ($RPN \ge 120$).
- **FR-TQM-02 (Defect Log & Checksheet):** The system shall track defects across Module, Category, Severity, and Occurrence Count, aggregating observations into checksheet summaries without double counting.
- **FR-TQM-03 (Pareto 80/20 Analysis):** The system shall render a dual-axis Pareto chart displaying defect category frequencies descending, cumulative percentage curves, and the 80% vital few threshold.
- **FR-TQM-04 (Ishikawa Fishbone Diagram):** The system shall generate cause-and-effect diagrams organizing root causes across People, Process, Software Code, and Infrastructure.
- **FR-TQM-05 (SIPOC & CTQ):** The system shall provide visual mapping for the 5-stage SIPOC employee lifecycle and CTQ quality driver decomposition.
- **FR-TQM-06 (PDCA Continuous Improvement):** The system shall track Deming improvement cycles across Plan, Do, Check, and Act stages with before-and-after empirical verification metrics.

### 3.4 Reporting and Backup Modules
- **FR-REP-01:** Export employee directories to CSV, Excel (`.xlsx`), and ReportLab PDF.
- **FR-REP-02:** Export Defect Logs, FMEA Registers, and PDCA Improvement records to formatted PDF audit reports.
- **FR-BAK-01:** Generate atomic SQLite database snapshots using the SQLite Online Backup API.
- **FR-BAK-02:** Provide single-click backup restoration with integrity check verification and pre-restore safety copies.

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **NFR-PERF-01:** Local search query execution time shall be under 50 ms for datasets up to 5,000 records.
- **NFR-PERF-02:** Application cold startup time shall be under 3.0 seconds on standard Windows desktop hardware.
- **NFR-PERF-03:** Report generation shall complete in under 2.5 seconds for standard employee rosters.

### 4.2 Reliability & Fault Tolerance
- **NFR-REL-01:** Database transactions shall enforce ACID properties using SQLite WAL mode.
- **NFR-REL-02:** The system shall prevent data corruption upon sudden termination or power failure.
- **NFR-REL-03:** Corrupted configuration files shall trigger transparent recovery to default settings without crashing.

### 4.3 Maintainability (Q11 Specifics)
- **NFR-MAIN-01:** Cyclomatic complexity for individual methods shall not exceed 15.
- **NFR-MAIN-02:** Automated test coverage shall exceed 85% across core service, validation, and analytics modules.
- **NFR-MAIN-03:** Separation of concerns: UI components shall contain zero direct SQL statements.

### 4.4 Usability & Accessibility
- **NFR-USE-01:** The graphical interface shall support Dark and Light themes with dynamic interface scaling (90% to 120%).
- **NFR-USE-02:** All interactive buttons and inputs shall have descriptive labels and visual hover states.

---

## 5. Acceptance Criteria
The system is accepted when:
1. `python main.py` launches the desktop application without errors.
2. All 28 automated pytest test cases pass cleanly.
3. Employee records persist across complete application restart.
4. Duplicate employee codes and malformed emails are blocked with friendly error dialogs.
5. FMEA RPN calculations and Pareto cumulative percentages match exact statistical standards.
6. System settings modifications immediately alter application behavior and persist to `config.json`.
