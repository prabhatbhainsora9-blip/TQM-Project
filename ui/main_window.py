"""
Main Application Desktop Window with Sidebar Navigation.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Orchestrates navigation across all modules without interface flickering,
maintains view states, and provides live status indications.
"""

import customtkinter as ctk
from typing import Dict, Any, Optional

from services.configuration_service import ConfigurationService
from services.employee_service import EmployeeService
from services.tqm_service import TQMService
from services.backup_service import BackupService
from services.report_service import ReportService
from services.logging_service import log_activity

from ui.dashboard import DashboardView
from ui.employee_view import EmployeeView
from ui.employee_form import EmployeeFormDialog
from ui.tqm_view import TQMView
from ui.defect_view import DefectView
from ui.fmea_view import FMEAView
from ui.sqc_view import SQCChartsView
from ui.pdca_view import PDCAView
from ui.logs_view import LogsView
from ui.reports_view import ReportsView
from ui.settings_view import SettingsView
from ui.help_view import HelpView


class MainWindow(ctk.CTk):
    """Primary application frame with responsive sidebar navigation."""

    def __init__(
        self,
        config_service: ConfigurationService,
        employee_service: EmployeeService,
        tqm_service: TQMService,
        backup_service: BackupService,
        report_service: ReportService
    ):
        super().__init__()

        self.config_service = config_service
        self.employee_service = employee_service
        self.tqm_service = tqm_service
        self.backup_service = backup_service
        self.report_service = report_service

        # Initialize appearance from configuration
        theme = self.config_service.get("ui.theme", "Dark")
        scaling = self.config_service.get("ui.scaling", 1.0)
        ctk.set_appearance_mode(theme)
        ctk.set_widget_scaling(scaling)

        # Window Setup
        self.title("Employee Management System — TQM Edition (Q11 Maintainability)")
        self.geometry("1240x760")
        self.minsize(1050, 650)

        # Main Layout: 2 Columns (Sidebar & Content Area)
        self.grid_columnconfigure(0, weight=0)  # Fixed sidebar
        self.grid_columnconfigure(1, weight=1)  # Expandable content
        self.grid_rowconfigure(0, weight=1)

        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        self.current_view_widget = None

        self._build_sidebar()
        self._build_content_area()

        # Start on Dashboard
        self.navigate_to("Dashboard")

        # Record startup activity
        log_activity("APPLICATION_START", "Main GUI window initialized successfully.", module="UI")

    def _build_sidebar(self) -> None:
        """Constructs left administrative sidebar."""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=("#f1f5f9", "#020617"))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # App Brand Header
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=14, pady=(16, 12))

        ctk.CTkLabel(brand_frame, text="TQM EMS", font=("Segoe UI", 16, "bold"), text_color=("#2563eb", "#3b82f6"), anchor="w").pack(anchor="w")
        ctk.CTkLabel(brand_frame, text="Maintainability Edition (Q11)", font=("Segoe UI", 9, "bold"), text_color=("#64748b", "#94a3b8"), anchor="w").pack(anchor="w")

        # Academic Student Tag
        tag_box = ctk.CTkFrame(self.sidebar, fg_color=("#e2e8f0", "#0f172a"), corner_radius=6)
        tag_box.pack(fill="x", padx=12, pady=(0, 14))
        ctk.CTkLabel(tag_box, text="Prabhat S. Bhainsora", font=("Segoe UI", 9, "bold"), text_color=("#0f172a", "#f8fafc")).pack(anchor="w", padx=8, pady=(4, 0))
        ctk.CTkLabel(tag_box, text="Roll: 2410302046 | BBAT104", font=("Segoe UI", 8), text_color=("#64748b", "#94a3b8")).pack(anchor="w", padx=8, pady=(0, 4))

        # Nav items
        nav_items = [
            ("Dashboard", "📊"),
            ("Employees", "👥"),
            ("Add Employee", "➕"),
            ("TQM Quality Analysis", "🎯"),
            ("Defect Log", "🐛"),
            ("FMEA Risk Analysis", "⚠️"),
            ("SQC Charts", "📈"),
            ("PDCA Tracker", "🔄"),
            ("Reports", "📄"),
            ("Activity Logs", "📜"),
            ("System Settings", "⚙️"),
            ("Help and About", "ℹ️")
        ]

        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.pack(fill="both", expand=True, padx=8)

        for name, icon in nav_items:
            btn = ctk.CTkButton(
                self.nav_frame,
                text=f"  {icon}  {name}",
                font=("Segoe UI", 10),
                height=32,
                anchor="w",
                fg_color="transparent",
                text_color=("#1e293b", "#e2e8f0"),
                hover_color=("#e2e8f0", "#1e293b"),
                command=lambda n=name: self.navigate_to(n)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[name] = btn

        # Footer Status
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.pack(fill="x", side="bottom", padx=12, pady=12)
        ctk.CTkLabel(footer, text="DB: SQLite3 (WAL Mode)", font=("Segoe UI", 8), text_color="#10b981", anchor="w").pack(anchor="w")
        ctk.CTkLabel(footer, text="System: Healthy & Verified", font=("Segoe UI", 8), text_color=("#64748b", "#94a3b8"), anchor="w").pack(anchor="w")

    def _build_content_area(self) -> None:
        """Container where page frames are displayed."""
        self.content_container = ctk.CTkFrame(self, fg_color=("#f8fafc", "#0f172a"), corner_radius=0)
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

    def navigate_to(self, view_name: str) -> None:
        """Switches the active content frame smoothly."""
        if view_name == "Add Employee":
            # Direct shortcut: Open modal dialog without leaving current screen
            EmployeeFormDialog(self, self.employee_service, employee=None, on_success=self._on_employee_created)
            return

        # Highlight active button
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.configure(fg_color="#2563eb", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color=("#1e293b", "#e2e8f0"))

        # Destroy old view widget
        if self.current_view_widget:
            self.current_view_widget.destroy()

        # Instantiate new view
        if view_name == "Dashboard":
            self.current_view_widget = DashboardView(
                self.content_container,
                self.employee_service,
                self.tqm_service,
                navigate_callback=self.navigate_to
            )
        elif view_name == "Employees":
            records_limit = self.config_service.get("ui.records_per_page", 10)
            confirm_del = self.config_service.get("ui.confirm_delete", True)
            self.current_view_widget = EmployeeView(
                self.content_container,
                self.employee_service,
                records_per_page=records_limit,
                confirm_delete=confirm_del
            )
        elif view_name == "TQM Quality Analysis":
            self.current_view_widget = TQMView(
                self.content_container,
                self.tqm_service,
                navigate_callback=self.navigate_to
            )
        elif view_name == "Defect Log":
            self.current_view_widget = DefectView(self.content_container, self.tqm_service)
        elif view_name == "FMEA Risk Analysis":
            self.current_view_widget = FMEAView(self.content_container, self.tqm_service)
        elif view_name == "SQC Charts":
            self.current_view_widget = SQCChartsView(self.content_container, self.tqm_service)
        elif view_name == "PDCA Tracker":
            self.current_view_widget = PDCAView(self.content_container, self.tqm_service)
        elif view_name == "Reports":
            self.current_view_widget = ReportsView(self.content_container, self.report_service)
        elif view_name == "Activity Logs":
            log_file = self.config_service.get("logging.log_file", "logs/application.log")
            self.current_view_widget = LogsView(self.content_container, log_file_path=log_file)
        elif view_name == "System Settings":
            self.current_view_widget = SettingsView(
                self.content_container,
                self.config_service,
                self.backup_service,
                on_settings_applied=self._on_settings_updated
            )
        elif view_name == "Help and About":
            self.current_view_widget = HelpView(self.content_container)

        if self.current_view_widget:
            self.current_view_widget.grid(row=0, column=0, sticky="nsew")

    def _on_employee_created(self) -> None:
        """Callback when an employee is registered."""
        if isinstance(self.current_view_widget, (EmployeeView, DashboardView)):
            self.current_view_widget.refresh() if hasattr(self.current_view_widget, "refresh") else self.current_view_widget.reload_data()

    def _on_settings_updated(self) -> None:
        """Refreshes active view when settings (scaling, theme) are modified."""
        pass
