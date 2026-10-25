# GitHub Repository Readiness & Commit Milestones Guide
## Repository: BBAT104_TQM_2410302046

**Course Code:** BBAT104 — Fundamentals of Total Quality Management  
**Academic Session:** 2026–27  
**Student Name:** Prabhat Singh Bhainsora  
**Registration / Roll Number:** 2410302046  
**Branch & Section:** Computer Science & Engineering (CSE) — Section B  
**Assigned Quality Goal:** Q11 — Improve Maintainability  
**Baseline System:** Employee Management System  

---

## 1. Local Git Setup Instructions

Follow these exact commands in PowerShell or Git Bash to initialize your local repository and link it to GitHub:

```powershell
# 1. Navigate to the project root directory
cd c:\Users\bhain\TQM-Project

# 2. Initialize a local Git repository (if not already initialized)
git init

# 3. Configure your local Git identity
git config user.name "Prabhat Singh Bhainsora"
git config user.email "bhainsoraprabhat@gmail.com"

# 4. Check staging status (notice .gitignore protects sensitive databases and logs)
git status

# 5. Add all files to the initial commit
git add .
git commit -m "feat(init): baseline employee management system with Q11 maintainability architecture"

# 6. Set main as the default branch
git branch -M main

# 7. Add your remote GitHub repository
git remote add origin https://github.com/PrabhatBhainsora/BBAT104_TQM_2410302046.git

# 8. Push to GitHub (requires GitHub authentication or Personal Access Token)
git push -u origin main
```

---

## 2. Recommended 30+ Meaningful Commit Milestones

Academic project guidelines require at least 30 meaningful commits covering logical development milestones. Use the structured commit list below if staging incremental changes:

### Phase 1: Environment & Project Scaffolding
1. `feat(scaffold): initialize project structure, requirements.txt, and .gitignore`
2. `feat(config): implement external config.json with factory default fallback (Q11 Feature 2)`
3. `feat(logging): configure centralized RotatingFileHandler with 1MB limit (Q11 Feature 4)`

### Phase 2: Database Layer & Persistence Tier
4. `feat(db): establish SQLite3 database connection with WAL mode and foreign key pragmas`
5. `feat(db): implement schema DDL for employees, defects, fmea, and pdca tables`
6. `feat(db): add database schema migration tracking and index definitions`
7. `feat(db): add realistic demonstration seed data for academic evaluation`

### Phase 3: Domain Models & Business Logic
8. `feat(models): create Employee dataclass model with serialization helpers`
9. `feat(models): create Defect, FMEARecord, and PDCARecord dataclass entities`
10. `feat(validation): implement Poka-Yoke validation rules for emails, phones, and dates`
11. `feat(service): implement EmployeeService for CRUD operations with uniqueness checks`

### Phase 4: Q11 Maintainability Services
12. `feat(service): implement ConfigurationService with dot-notation and self-healing recovery`
13. `feat(service): create BackupService with online backup API and restore verification`
14. `feat(service): create ReportService supporting CSV, Excel (OpenPyXL), and PDF (ReportLab)`

### Phase 5: TQM & SQC Modules
15. `feat(tqm): implement TQMService for defect logging, checksheet, and RPN calculation`
16. `feat(fmea): implement FMEA risk register with automatic RPN and high-risk threshold`
17. `feat(pdca): implement PDCA continuous improvement tracker across Plan, Do, Check, Act`
18. `feat(analytics): create ParetoAnalyzer with dual-axis 80/20 frequency calculation`
19. `feat(analytics): implement FishboneGenerator for People, Process, Code, Infrastructure causes`
20. `feat(analytics): create SIPOCMapper and CTQTree visual diagram generators`

### Phase 6: Presentation Tier & Modern Desktop GUI
21. `feat(ui): implement MainWindow container with responsive sidebar navigation`
22. `feat(ui): build Executive DashboardView with live KPI cards and department breakdown`
23. `feat(ui): build EmployeeView with sortable table, search filters, and pagination`
24. `feat(ui): implement EmployeeFormDialog with inline Poka-Yoke validation feedback`
25. `feat(ui): build DefectView and FMEAView risk register management tables`
26. `feat(ui): implement SQCChartsView with embedded Matplotlib canvas and PNG export`
27. `feat(ui): implement dedicated TQMView covering principles, checksheet, SIPOC, and CTQ`
28. `feat(ui): build System Settings screen with dynamic themes and persistence (Q11 Feature 3)`
29. `feat(ui): create LogsView with level filtering and Help/About view`

### Phase 7: Automated Testing & Verification
30. `test(employees): add pytest suite for CRUD, uniqueness rejection, and regex boundaries`
31. `test(q11): implement test cases for config auto-recovery, logging, and backup restore`
32. `test(sqc): add tests for Pareto cumulative calculations, checksheets, and diagrams`

### Phase 8: Comprehensive Documentation
33. `docs(srs): write Software Requirements Specification (SRS.md)`
34. `docs(arch): document Layered Architecture and Mermaid runtime flowcharts`
35. `docs(manual): write User Manual and Operator Guide`
36. `docs(tqm): compile FMEA matrix, SIPOC map, CTQ tree, SQC analysis, and PDCA logs`
37. `docs(viva): create viva voce preparation guide with Q&A on TQM and Q11 goals`
38. `docs(readme): create complete README.md with setup, architecture, and verification guide`

---

## 3. GitHub Issues Checklist for Tracking Progress

Copy and paste this Markdown checklist into your GitHub repository under **Issues** to track project deliverables:

```markdown
### Milestone 1: Core System Architecture & Employee CRUD
- [x] Design layered modular architecture separating UI, Services, Database, Analytics (Q11 Feature 1)
- [x] Configure external `config.json` with self-healing recovery (Q11 Feature 2)
- [x] Set up SQLite database with WAL mode and schema migration table
- [x] Implement Employee CRUD (Create, Read, Update, Delete) operations
- [x] Implement Poka-Yoke input validation (RFC email regex, phone length bounds)
- [x] Add multi-criteria employee search and department/status filtering
- [x] Build sortable employee table with responsive pagination

### Milestone 2: Q11 Maintainability Enhancements
- [x] Build dynamic System Settings screen with Light/Dark theme switching (Q11 Feature 3)
- [x] Implement interface scaling ($100\%, 110\%, 125\%$) and records per page adjustment
- [x] Configure rotating activity logs (`RotatingFileHandler`, 1MB cap, 5 backups) (Q11 Feature 4)
- [x] Build in-app Log Viewer with date, level, and keyword filtering
- [x] Implement database snapshot backup and non-destructive restore service
- [x] Add comprehensive docstrings and maintainability documentation (Q11 Feature 5)

### Milestone 3: TQM & Statistical Quality Control (SQC)
- [x] Implement Defect Tracking log with severity, status, and verification notes
- [x] Build empirical Defect Checksheet aggregating occurrences without double-counting
- [x] Implement Failure Mode and Effects Analysis (FMEA) with automatic RPN calculation
- [x] Create interactive Pareto Chart (80/20 rule) with dual-axis cumulative curve
- [x] Implement Ishikawa (Fishbone) diagram categorized into People, Process, Code, Infrastructure
- [x] Create SIPOC process map for the complete employee records lifecycle
- [x] Build Critical to Quality (CTQ) Tree with measurable project benchmarks
- [x] Implement Plan-Do-Check-Act (PDCA) continuous improvement tracker

### Milestone 4: Reporting, Testing & Final Delivery
- [x] Build multi-format report generator (CSV, Excel `.xlsx`, PDF `.pdf`)
- [x] Implement automated test suite covering all services (30 passing tests)
- [x] Compile complete documentation: SRS, Architecture, User Manual, FMEA, SIPOC, CTQ, SQC, PDCA, Viva Guide
- [x] Finalize README.md with full student details, installation guide, and verification steps
```
