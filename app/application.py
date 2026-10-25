"""
Application Bootstrap and Lifecycle Coordinator.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Orchestrates startup directory checks, database migration initialization,
service container instantiation, and GUI main loop execution.
"""

import os
import sys

from services.configuration_service import ConfigurationService
from services.logging_service import setup_logging, log_activity, get_logger
from services.employee_service import EmployeeService
from services.tqm_service import TQMService
from services.backup_service import BackupService
from services.report_service import ReportService
from database.connection import DatabaseConnection
from database.schema import initialize_database, seed_sample_data
from ui.main_window import MainWindow


class Application:
    """Central lifecycle orchestrator managing dependencies and window lifecycle."""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path

        # 1. Load Configuration (Feature 2: Configuration Files)
        self.config_service = ConfigurationService(self.config_path)

        # 2. Ensure Required Directories Exist
        self._ensure_directories()

        # 3. Setup Activity Logging (Feature 4: Activity Logs)
        log_cfg = self.config_service.get("logging", {})
        self.logger = setup_logging(
            log_dir=log_cfg.get("log_dir", "logs"),
            log_file=log_cfg.get("log_file", "logs/application.log"),
            log_level=log_cfg.get("log_level", "INFO"),
            max_bytes=log_cfg.get("max_bytes", 1048576),
            backup_count=log_cfg.get("backup_count", 5)
        )

        self.logger.info("=" * 60)
        self.logger.info("Initializing Employee Management System (TQM Maintainability Edition)")
        self.logger.info(f"Student: {self.config_service.get('academic_info.student_name')} | Roll: {self.config_service.get('academic_info.roll_number')}")
        self.logger.info("Quality Goal: Q11 - Improve Maintainability | Course: BBAT104")
        self.logger.info("=" * 60)

        # 4. Database Setup & Schema Initialization
        db_cfg = self.config_service.get("database", {})
        db_path = db_cfg.get("db_path", "data/employee_tqm.db")
        timeout = db_cfg.get("connection_timeout", 10.0)

        self.db_manager = DatabaseConnection(db_path=db_path, timeout=timeout)
        self.db_conn = self.db_manager.get_connection()
        initialize_database(self.db_conn)

        # 5. Seed Demonstration Data if newly created
        seed_sample_data(self.db_conn, clear_existing=False)

        # 6. Instantiate Domain Services
        self.employee_service = EmployeeService(self.db_conn)
        self.tqm_service = TQMService(self.db_conn)

        backup_cfg = self.config_service.get("backup", {})
        self.backup_service = BackupService(
            db_path=db_path,
            backup_dir=backup_cfg.get("backup_dir", "backups"),
            max_backups=backup_cfg.get("max_backups", 10)
        )

        reports_cfg = self.config_service.get("reports", {})
        self.report_service = ReportService(
            db_conn=self.db_conn,
            output_dir=reports_cfg.get("output_dir", "reports")
        )

        # Auto backup on startup if configured
        if backup_cfg.get("auto_backup_on_startup", False):
            self.backup_service.create_backup(note="startup_auto")

    def _ensure_directories(self) -> None:
        """Guarantees runtime workspace directories exist without throwing errors."""
        dirs = ["data", "logs", "backups", "reports"]
        for d in dirs:
            os.makedirs(os.path.abspath(d), exist_ok=True)

    def run(self) -> None:
        """Launches the primary graphical user interface."""
        try:
            self.main_window = MainWindow(
                config_service=self.config_service,
                employee_service=self.employee_service,
                tqm_service=self.tqm_service,
                backup_service=self.backup_service,
                report_service=self.report_service
            )
            # Bind shutdown protocol
            self.main_window.protocol("WM_DELETE_WINDOW", self._on_close)
            self.main_window.mainloop()
        except Exception as e:
            self.logger.critical(f"Unhandled exception during GUI execution: {e}", exc_info=True)
            raise e

    def _on_close(self) -> None:
        """Gracefully releases resources and records shutdown event."""
        log_activity("APPLICATION_SHUTDOWN", "Application shutting down gracefully.", module="SYSTEM", db_conn=self.db_conn)
        self.logger.info("Application closed by user.")
        try:
            self.db_manager.close()
        except Exception:
            pass
        if hasattr(self, "main_window"):
            self.main_window.destroy()
        sys.exit(0)
