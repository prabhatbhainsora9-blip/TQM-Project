# Automated Testing & Verification Report
## Employee Management System with Maintainability Enhancement and TQM Quality Analysis

**Document Version:** 1.0.0  
**Course Code:** BBAT104 — Fundamentals of Total Quality Management  
**Academic Session:** 2026–27  
**Student Name:** Prabhat Singh Bhainsora  
**Registration / Roll Number:** 2410302046  
**Branch & Section:** Computer Science & Engineering (CSE) — Section B  
**Assigned Quality Goal:** Q11 — Improve Maintainability  
**Baseline System:** Employee Management System  
**Target Repository:** `BBAT104_TQM_2410302046`

---

## 1. Test Execution Summary

The test suite was executed locally on the Windows development workstation using **Pytest**.

- **Test Framework:** Pytest 9.1.1
- **Python Environment:** Python 3.12.10 (64-bit)
- **Operating System:** Microsoft Windows 11
- **Total Test Cases:** **30**
- **Passed:** **30 (100%)**
- **Failed:** **0 (0%)**
- **Errors / Warnings:** **0 (0%)**
- **Execution Duration:** **2.63 seconds**
- **Overall Status:** **PASSED — ALL QUALITY ACCEPTANCE CRITERIA VERIFIED**

---

## 2. Test Isolation & Database Safety

> [!IMPORTANT]
> **Zero Database Contamination Guarantee:**  
> All tests utilize isolated fixtures defined in [conftest.py](file:///c:/Users/bhain/TQM-Project/tests/conftest.py). Temporary SQLite databases and temporary directories are dynamically generated inside pytest's isolated `tmp_path` environment.  
> Under no circumstances do test runs read, write, or pollute the real application database file (`data/employee_tqm.db`) or user logs (`logs/application.log`).

---

## 3. Comprehensive Test Results Inventory

| Test Module | Test Function Name | Architectural Requirement Tested | Verification Criterion | Status |
|:---|:---|:---|:---|:---:|
| **test_analytics.py** | `test_pareto_cumulative_percentage_calculation` | Pareto 80/20 Math | Sorted descending frequencies; final cumulative percentage equals exactly 100.0%. | **PASSED** |
| **test_analytics.py** | `test_pareto_handles_empty_dataset` | Boundary Handling | Gracefully handles empty dictionary without zero-division exceptions. | **PASSED** |
| **test_analytics.py** | `test_tqm_checksheet_aggregation_avoids_double_counting` | TQM SQC Metric | Sums `occurrence_count` per category without double-counting distinct defect IDs. | **PASSED** |
| **test_analytics.py** | `test_fishbone_diagram_generation` | Ishikawa SQC Tool | Generates valid Matplotlib figure across People, Process, Code, Infrastructure. | **PASSED** |
| **test_analytics.py** | `test_sipoc_and_ctq_diagram_generation` | SIPOC & CTQ Tools | Verifies generation of visual SIPOC and CTQ diagrams without plotting errors. | **PASSED** |
| **test_backup.py** | `test_backup_creation_and_integrity` | Disaster Recovery | Online SQLite backup API produces valid snapshot with matching record count. | **PASSED** |
| **test_backup.py** | `test_backup_restore_recovers_data` | System Resilience | Deleting live records and executing restore recovers 100% of employee data. | **PASSED** |
| **test_configuration.py** | `test_config_loads_defaults_when_file_missing` | Self-Healing (Q11) | Safely restores factory defaults if `config.json` is deleted. | **PASSED** |
| **test_configuration.py** | `test_config_recovers_from_corrupted_json` | Self-Healing (Q11) | Recovers from malformed syntax with warning and re-writes safe defaults. | **PASSED** |
| **test_configuration.py** | `test_config_get_and_set_dot_notation` | Configuration (Q11) | Dot notation keys (e.g., `ui.theme`, `ui.records_per_page`) resolve cleanly. | **PASSED** |
| **test_configuration.py** | `test_config_reset_to_defaults` | User Settings (Q11) | Reverts all user settings back to initial factory baseline. | **PASSED** |
| **test_database.py** | `test_database_initialization_creates_all_tables` | Persistence Tier | All 7 tables created: employees, defects, fmea, pdca, fishbone, audit, schema. | **PASSED** |
| **test_database.py** | `test_schema_migration_version_recorded` | Schema Versioning | Migration version 1 recorded with timestamp in `schema_migrations`. | **PASSED** |
| **test_database.py** | `test_foreign_keys_are_enabled` | ACID Enforcement | `PRAGMA foreign_keys` returns 1 (ON) upon connection establishment. | **PASSED** |
| **test_employees.py** | `test_create_employee_success` | CRUD — Create | Valid employee dictionary persists into SQLite and generates positive row ID. | **PASSED** |
| **test_employees.py** | `test_duplicate_employee_code_rejected` | Poka-Yoke / Uniqueness | Rejects duplicate employee code with user-friendly error message. | **PASSED** |
| **test_employees.py** | `test_invalid_email_format_rejected` | Poka-Yoke Validation | Rejects malformed email string (missing `@` or domain) before database write. | **PASSED** |
| **test_employees.py** | `test_short_phone_number_rejected` | Poka-Yoke Validation | Rejects phone number shorter than 10 digits. | **PASSED** |
| **test_employees.py** | `test_invalid_date_format_rejected` | Poka-Yoke Validation | Rejects non-ISO dates (e.g., `31-12-2023`) and accepts `YYYY-MM-DD`. | **PASSED** |
| **test_employees.py** | `test_update_employee_success` | CRUD — Update | Modifies employee designation and department; updates `updated_at` stamp. | **PASSED** |
| **test_employees.py** | `test_delete_employee_success` | CRUD — Delete | Safely removes target employee record while leaving others intact. | **PASSED** |
| **test_employees.py** | `test_search_and_filter_employees` | CRUD — Search/Filter | Filters correctly by department, active status, and search substring. | **PASSED** |
| **test_fmea.py** | `test_fmea_rpn_calculation_formula` | FMEA Math | Formula $RPN = S \times O \times D$ verified ($7 \times 5 \times 3 = 105$). | **PASSED** |
| **test_fmea.py** | `test_create_fmea_record_calculates_rpn_automatically` | TQM Automation | Inserts FMEA record and automatically computes and persists RPN in database. | **PASSED** |
| **test_fmea.py** | `test_fmea_score_out_of_bounds_rejected` | FMEA Score Validation | Scores $< 1$ or $> 10$ rejected with clear validation notice. | **PASSED** |
| **test_fmea.py** | `test_fmea_records_sorted_by_rpn_descending` | Risk Prioritization | Query orders failure modes from highest RPN to lowest. | **PASSED** |
| **test_logging.py** | `test_activity_logging_records_event` | Activity Logs (Q11) | Records event with timestamp, user, module, level in log file and audit table. | **PASSED** |
| **test_logging.py** | `test_log_filtering_by_level_and_search` | Log Viewer (Q11) | Filters logs accurately by level (`INFO`, `ERROR`) and keyword search. | **PASSED** |
| **test_pdca.py** | `test_pdca_lifecycle_creation_and_update` | Kaizen Continuous Impr. | Transitions through Plan -> Do -> Check -> Act stages with persistent evidence. | **PASSED** |
| **test_reports.py** | `test_reports_export_csv_excel_pdf` | Reporting & Exports | Generates valid non-empty `.csv`, `.xlsx` (OpenPyXL), and `.pdf` (ReportLab). | **PASSED** |

---

## 4. How to Run the Automated Tests

To execute the full test suite in your local terminal:

```powershell
# Run all tests with verbose output
pytest -v

# Run with test printouts and summary statistics
pytest -v -s tests/

# Alternative: Double click run_tests.bat in the project root
```
