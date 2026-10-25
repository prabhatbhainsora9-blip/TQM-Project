# Comprehensive Academic Viva Voce Preparation Guide
## Employee Management System with Maintainability Enhancement and TQM Quality Analysis

**Course Code:** BBAT104 — Fundamentals of Total Quality Management  
**Academic Session:** 2026–27  
**Student Name:** Prabhat Singh Bhainsora  
**Registration / Roll Number:** 2410302046  
**Branch & Section:** Computer Science & Engineering (CSE) — Section B  
**Assigned Quality Goal:** Q11 — Improve Maintainability  
**Baseline Software System:** Employee Management System  
**Project Title:** “Employee Management System with Maintainability Enhancement and TQM-Based Quality Analysis”  
**Target Repository:** `BBAT104_TQM_2410302046`

---

## Section 1: Candidate & Project Credentials

### Q1: Introduce yourself and state your assigned project topic and quality goal.
**Answer:**  
Good morning / afternoon, respected examiners. My name is **Prabhat Singh Bhainsora**, roll number **2410302046**, CSE Section B.  
Under Course **BBAT104: Fundamentals of Total Quality Management**, my assigned baseline software system is the **Employee Management System**, and my assigned quality goal is **Q11 — Improve Maintainability**.  
My project title is **“Employee Management System with Maintainability Enhancement and TQM-Based Quality Analysis”**.

### Q2: What is the primary objective of this project?
**Answer:**  
The objective is twofold:
1. To build a robust, fully functional, locally executable desktop Employee Management System supporting full CRUD operations, pagination, search/filtering, and multi-format reporting.
2. To demonstrate how **Total Quality Management (TQM)** principles and **Statistical Quality Control (SQC)** instruments (FMEA, SIPOC, CTQ, Checksheets, Pareto 80/20, Ishikawa Fishbone, PDCA) can be applied to software engineering to satisfy **Quality Goal Q11 (Improve Maintainability)**.

---

## Section 2: Quality Goal Q11 (Improve Maintainability)

### Q3: What is "Software Maintainability" and why is it a critical quality attribute?
**Answer:**  
According to ISO/IEC 25010, **maintainability** is the degree of effectiveness and efficiency with which a software product can be modified by intended maintainers. Over 70% of software lifecycle costs occur during post-release maintenance (bug fixing, adapting to environment changes, adding new features). High maintainability reduces Mean Time to Repair (MTTR), prevents technical debt, and improves software longevity.

### Q4: Explain the Five Mandatory Q11 Features implemented in your project.
**Answer:**  
Our system implements five distinct maintainability features:
1. **Feature 1: Modular Architecture:** The codebase is partitioned into 7 decoupled packages (`app`, `database`, `models`, `services`, `ui`, `analytics`, `tests`). No business logic resides inside GUI event handlers, and no SQL is scattered across the UI.
2. **Feature 2: External Configuration Files:** Configuration settings (paths, log levels, theme, pagination) are stored externally in `config.json`. The system has self-healing recovery: if `config.json` is missing or corrupted, it automatically restores factory defaults without crashing.
3. **Feature 3: Dynamic System Settings Screen:** A fully functional GUI screen enables operators to modify themes, UI scaling, records per page, and log levels. These changes persist across restarts and directly alter application behavior.
4. **Feature 4: Rotating Activity Logs & Log Viewer:** Using Python’s `logging` module with `RotatingFileHandler`, logs are capped at 1 MB with 5 rolling backup files to prevent disk exhaustion. An in-app Log Viewer allows filtering by level, date, and keyword.
5. **Feature 5: Code Documentation & Comments:** Comprehensive docstrings, clean type annotations, Mermaid architecture flowcharts, SRS, user manual, and viva guides are provided to ensure any future developer can maintain the application.

---

## Section 3: Total Quality Management (TQM) Principles

### Q5: How did you apply the five core TQM principles to this software?
**Answer:**  
1. **Customer Focus:** Internal users (HR operators, auditors) receive an intuitive desktop GUI with responsive light/dark themes, clear error dialogs, and instant search feedback.
2. **Continuous Improvement (Kaizen):** We implemented the Deming Plan-Do-Check-Act (PDCA) cycle, recording baseline metrics, root causes, corrective actions, and verifiable post-action evidence.
3. **Process-Centric Approach:** The employee records lifecycle is mapped using a SIPOC diagram (Suppliers, Inputs, Process, Outputs, Customers) ensuring standardized process boundaries.
4. **Fact-Based Decision Making:** Architectural decisions are driven by quantitative data: Pareto 80/20 analysis, defect checksheets, and FMEA Risk Priority Numbers (RPN).
5. **Error Prevention (Poka-Yoke):** Instead of allowing errors to reach the database, the system enforces pre-commit regular expressions, phone digit bounds, uniqueness checks, and dropdown selectors.

### Q6: What is Poka-Yoke and where is it found in your code?
**Answer:**  
*Poka-Yoke* is a Japanese term meaning "mistake-proofing" or "inadvertent error prevention". In our software:
- `services/validation_service.py` evaluates emails with RFC 5322 regex and phones with $10 \le \text{digits} \le 15$ bounds.
- Forms use non-editable dropdowns (`CTkComboBox`) for departments and status, preventing spelling typos.
- The system checks Employee Code and Email uniqueness before attempting an SQL `INSERT`.
- Deletions require explicit confirmation dialogs.

---

## Section 4: Statistical Quality Control (SQC) Tools

### Q7: Explain Pareto Analysis and how the 80/20 rule applies to software defects.
**Answer:**  
Pareto Analysis orders defect categories by descending frequency to isolate the "vital few" from the "trivial many". The mathematical formula for cumulative percentage is:
$$\text{Cumulative \%}_k = \left( \frac{\sum_{i=1}^k f_i}{\text{Total Defects}} \right) \times 100\%$$
In our system, Pareto Analysis revealed that **Validation Errors** ($45.7\%$) and **UI Glitches** ($15.7\%$) accounted for over **61.4%** of all defect occurrences. Addressing these two vital categories eliminated the vast majority of operational failures. Importantly, we do not assume every dataset strictly hits exactly $80/20$, but use it as an empirical prioritization guide.

### Q8: What is an Ishikawa (Fishbone) diagram and what four categories did you use?
**Answer:**  
An Ishikawa or Fishbone diagram is a cause-and-effect tool that maps potential root causes of a problem statement. For our problem statement—*“High Employee Registration Data Errors”*—we organized root causes into four required categories:
1. **People:** Lack of date format training, operator typing fatigue.
2. **Process:** Absence of real-time Poka-Yoke feedback before submission, manual paper transcription.
3. **Software Code:** Missing RFC email regex, unhandled duplicate code exceptions.
4. **Infrastructure:** Unregulated Windows high-DPI display scaling, disk latency.
We distinguished **investigated causes** (empirically confirmed by logs) from **suspected causes** (hypothesized).

### Q9: What is a TQM Checksheet and how did you prevent double-counting?
**Answer:**  
A checksheet is a structured form for gathering real-time empirical defect counts. To avoid double-counting, each distinct defect item in our database stores an `occurrence_count` representing repeated observations. The checksheet groups records strictly by category and severity, summing occurrences (`SUM(occurrence_count)`) while reporting distinct defect counts (`COUNT(id)`).

---

## Section 5: Failure Mode and Effects Analysis (FMEA)

### Q10: What is FMEA and how is the Risk Priority Number (RPN) calculated?
**Answer:**  
FMEA is a prospective risk assessment tool. The Risk Priority Number is calculated as:
$$\text{RPN} = \text{Severity (S)} \times \text{Occurrence (O)} \times \text{Detection (D)}$$
Each parameter is rated on a documented 1 to 10 integer scale:
- **Severity (S):** 1 (negligible) to 10 (total irrecoverable database loss).
- **Occurrence (O):** 1 (extremely unlikely) to 10 (almost inevitable).
- **Detection (D):** 1 (almost certain detection before user impact) to 10 (undetectable silent failure).
The theoretical range is $1$ to $1,000$. Our project established an action threshold of $\text{RPN} \ge 120$.

### Q11: Give an example of an FMEA item and how Q11 maintainability reduced its RPN.
**Answer:**  
In item **FMEA-01 (Database persistence corruption or write-lock during ungraceful exit)**:
- **Initial:** $\text{Severity} = 9$, $\text{Occurrence} = 4$, $\text{Detection} = 4 \implies \text{RPN} = 144$ (HIGH RISK).
- **Mitigation:** We implemented SQLite Write-Ahead Logging (`WAL` mode), synchronous NORMAL, and an automated `BackupService` with single-click restore.
- **Revised:** $\text{Severity} = 9$, $\text{Occurrence} = 1$, $\text{Detection} = 2 \implies \text{Revised RPN} = 18$ (**87.5% risk reduction**).

---

## Section 6: Architecture and Database Engineering

### Q12: Why did you use SQLite3 with WAL mode rather than an external client-server database?
**Answer:**  
1. **Desktop Autonomy:** SQLite is serverless, zero-configuration, and runs entirely in-process on the user's local machine without requiring external network ports, credentials, or daemon setup.
2. **Write-Ahead Logging (WAL):** Default SQLite rollback journals block concurrent readers during write transactions. WAL mode writes changes to a separate `-wal` file, allowing concurrent read queries (such as background report generation) to run simultaneously without locking errors.

### Q13: How does the application prevent SQL injection?
**Answer:**  
All database interactions use **parameterized queries** (e.g., `cursor.execute("SELECT * FROM employees WHERE employee_code = ?", (code,))`). User input is never concatenated or formatted directly into raw SQL strings.

---

## Section 7: Testing and Verification

### Q14: How are your automated tests structured and how many tests did you execute?
**Answer:**  
We implemented **30 automated tests** using **Pytest** across 9 test files covering employee CRUD, duplicate rejection, regex validation, config recovery, backup/restore, activity logging, FMEA calculations, Pareto statistics, and report generation.  
All 30 tests pass cleanly in under 3 seconds. To prevent data corruption, tests use isolated `tmp_path` fixtures in [conftest.py](file:///c:/Users/bhain/TQM-Project/tests/conftest.py), completely isolating tests from the production database.
