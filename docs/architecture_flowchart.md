# Application Execution Flowchart (Runtime Architecture)
## Employee Management System with Maintainability Enhancement (Q11)

**Student:** Prabhat Singh Bhainsora (2410302046)  
**Course:** BBAT104 — Fundamentals of Total Quality Management  

---

## 1. Complete Application Lifecycle Flowchart

```mermaid
flowchart TD
    Start([Application Launch: python main.py]) --> Step1[Anchor sys.path to Project Directory]
    Step1 --> Step2[Instantiate Application Container]
    
    %% Configuration & Fallback
    Step2 --> Step3{Load config.json}
    Step3 -- File Exists & Valid --> Step4[Parse Settings Dictionary]
    Step3 -- Missing or Corrupted --> Step3Fallback[Restore Safe Factory Defaults & Resave]
    Step3Fallback --> Step4
    
    %% Directory & Logger Setup
    Step4 --> Step5[Ensure Directories Exist: data/, logs/, backups/, reports/]
    Step5 --> Step6[Setup RotatingFileHandler & Console Logging]
    Step6 --> LogStartup[Log Startup Event to logs/application.log]
    
    %% Database Initialization
    LogStartup --> Step7[Establish SQLite3 Connection]
    Step7 --> Step8[Execute PRAGMA foreign_keys = ON & journal_mode = WAL]
    Step8 --> Step9[Run Database Schema DDL & Create Tables]
    Step9 --> Step10{Check Database Seed Status}
    Step10 -- Empty Database --> Step10Seed[Seed Demonstration Records for Evaluation]
    Step10 -- Existing Data Found --> Step11[Skip Seeding & Preserve User Records]
    Step10Seed --> Step11
    
    %% Service Container & UI
    Step11 --> Step12[Instantiate Domain Services: EmployeeService, TQMService, BackupService, ReportService]
    Step12 --> Step13[Instantiate MainWindow: CustomTkinter GUI]
    Step13 --> Step14[Render Sidebar & Mount DashboardView as Default]
    Step14 --> MainLoop([Enter CustomTkinter GUI MainLoop])
    
    %% Interactive Operations Subgraph
    subgraph User_Interactions ["User Action Event Handling"]
        MainLoop --> UserAction{Select Action}
        
        %% Employee CRUD
        UserAction -- Register / Edit Employee --> FormInput[Open EmployeeFormDialog]
        FormInput --> ValCheck{Poka-Yoke ValidationService}
        ValCheck -- Fails (Regex/Duplicate) --> ShowError[Display Inline Error Banner on Dialog]
        ShowError --> FormInput
        ValCheck -- Passes --> DBWrite[Execute Parameterized SQL Transaction]
        DBWrite --> DBCommit[Commit Transaction & Write Audit Log]
        DBCommit --> RefreshUI[Refresh Table & KPI Cards]
        
        %% TQM SQC Operations
        UserAction -- SQC Charts --> RenderSQC[Fetch Defect Frequencies & Generate Pareto / Fishbone]
        RenderSQC --> CanvasMount[Mount Matplotlib Figure via FigureCanvasTkAgg]
        
        %% Reporting
        UserAction -- Generate Report --> GenDoc[Export PDF/Excel/CSV via ReportLab/Pandas]
        GenDoc --> NotifyUser[Notify User with File Location & Open Folder Option]
        
        %% Settings
        UserAction -- Change Settings --> ApplySettings[Persist to config.json & Live Update UI Theme/Scaling]
        
        %% Backup
        UserAction -- Take Backup --> BackupSnapshot[Execute SQLite Native Online Backup API & Integrity Check]
    end
    
    RefreshUI --> MainLoop
    CanvasMount --> MainLoop
    NotifyUser --> MainLoop
    ApplySettings --> MainLoop
    BackupSnapshot --> MainLoop
    
    %% Shutdown
    MainLoop -- User Closes Window --> GracefulShutdown[Close SQLite Connections, Flush Log Handlers]
    GracefulShutdown --> End([Exit Process with Code 0])
```

---

## 2. Key Architectural Guarantees

1. **Zero Data Loss on Crash:** With SQLite WAL mode and atomic commits, partial transactions roll back automatically.
2. **Deterministic Startup:** Even with deleted directories or corrupted config files, self-healing bootstrapping ensures the application always starts.
3. **No Thread Freezing:** Heavy PDF exports and chart rendering write directly to separate canvas structures without locking the application window.
