"""
Executive Dashboard View for Employee Management System (TQM Edition).
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Displays real-time KPIs, department distributions, active defect counts,
and recent employee records derived directly from the SQLite database.
"""

import customtkinter as ctk
from typing import Callable, Optional

from ui.components.stat_card import StatCard
from services.employee_service import EmployeeService
from services.tqm_service import TQMService


class DashboardView(ctk.CTkScrollableFrame):
    """Main executive dashboard presenting operational and quality metrics."""

    def __init__(
        self,
        master,
        employee_service: EmployeeService,
        tqm_service: TQMService,
        navigate_callback: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.employee_service = employee_service
        self.tqm_service = tqm_service
        self.navigate_callback = navigate_callback

        self.grid_columnconfigure((0, 1, 2), weight=1)

        self._build_header()
        self._build_kpi_cards()
        self._build_quick_actions()
        self._build_distribution_and_recent()

    def _build_header(self) -> None:
        """Renders header banner with student credentials and project scope."""
        header_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(10, 15))
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="Employee Management System — TQM Quality Audit Dashboard",
            font=("Segoe UI", 16, "bold"),
            text_color=("#0f172a", "#f8fafc"),
            anchor="w"
        )
        title.grid(row=0, column=0, sticky="w", padx=20, pady=(12, 2))

        sub = ctk.CTkLabel(
            header_frame,
            text="Student: Prabhat Singh Bhainsora  |  Roll No: 2410302046  |  CSE-B  |  Course: BBAT104 (Session 2026–27)  |  Assigned Quality Goal: Q11 (Improve Maintainability)",
            font=("Segoe UI", 10),
            text_color=("#475569", "#94a3b8"),
            anchor="w"
        )
        sub.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 12))

    def _build_kpi_cards(self) -> None:
        """Instantiates real-time KPI metric cards."""
        emp_summary = self.employee_service.get_dashboard_summary()
        defects = self.tqm_service.get_all_defects()
        open_defects = sum(1 for d in defects if d.status in ["Open", "In Progress"])
        fmea_items = self.tqm_service.get_all_fmea_records()
        high_risk_fmea = sum(1 for f in fmea_items if (f.rpn or 0) >= 120)
        pdca_items = self.tqm_service.get_all_pdca_records()

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=6, pady=5)
        cards_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.card_total = StatCard(cards_frame, "Total Employees", str(emp_summary["total_employees"]), "All registered", accent_color="#3b82f6")
        self.card_total.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        self.card_active = StatCard(cards_frame, "Active Staff", str(emp_summary["active_employees"]), "In active service", accent_color="#10b981")
        self.card_active.grid(row=0, column=1, padx=4, pady=4, sticky="nsew")

        self.card_inactive = StatCard(cards_frame, "Inactive Staff", str(emp_summary["inactive_employees"]), "On leave / resigned", accent_color="#f59e0b")
        self.card_inactive.grid(row=0, column=2, padx=4, pady=4, sticky="nsew")

        self.card_defects = StatCard(cards_frame, "Open Defects", str(open_defects), f"Total: {len(defects)} recorded", accent_color="#ef4444")
        self.card_defects.grid(row=0, column=3, padx=4, pady=4, sticky="nsew")

        self.card_fmea = StatCard(cards_frame, "High Risk FMEA", str(high_risk_fmea), "RPN >= 120 threshold", accent_color="#dc2626")
        self.card_fmea.grid(row=0, column=4, padx=4, pady=4, sticky="nsew")

        self.card_pdca = StatCard(cards_frame, "PDCA Cycles", str(len(pdca_items)), "Kaizen improvements", accent_color="#8b5cf6")
        self.card_pdca.grid(row=0, column=5, padx=4, pady=4, sticky="nsew")

    def _build_quick_actions(self) -> None:
        """Renders quick-action navigation shortcuts."""
        actions_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        actions_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        lbl = ctk.CTkLabel(actions_frame, text="Quick Shortcuts:", font=("Segoe UI", 11, "bold"), text_color=("#475569", "#94a3b8"))
        lbl.pack(side="left", padx=15, pady=8)

        btn_add = ctk.CTkButton(
            actions_frame, text="+ Add Employee", width=120, height=30,
            command=lambda: self._navigate("Add Employee")
        )
        btn_add.pack(side="left", padx=6, pady=8)

        btn_defect = ctk.CTkButton(
            actions_frame, text="Log Quality Defect", width=130, height=30, fg_color="#ef4444", hover_color="#dc2626",
            command=lambda: self._navigate("Defect Log")
        )
        btn_defect.pack(side="left", padx=6, pady=8)

        btn_pareto = ctk.CTkButton(
            actions_frame, text="View Pareto (80/20)", width=140, height=30, fg_color="#6366f1", hover_color="#4f46e5",
            command=lambda: self._navigate("SQC Charts")
        )
        btn_pareto.pack(side="left", padx=6, pady=8)

        btn_rep = ctk.CTkButton(
            actions_frame, text="Generate Reports", width=130, height=30, fg_color="#0d9488", hover_color="#0f766e",
            command=lambda: self._navigate("Reports")
        )
        btn_rep.pack(side="left", padx=6, pady=8)

        btn_refresh = ctk.CTkButton(
            actions_frame, text="Refresh Data", width=100, height=30, fg_color="#475569", hover_color="#334155",
            command=self.refresh
        )
        btn_refresh.pack(side="right", padx=15, pady=8)

    def _build_distribution_and_recent(self) -> None:
        """Displays department distribution on the left and recent employee records on the right."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=6, pady=5)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=2)

        # Left Card: Department Distribution
        dept_frame = ctk.CTkFrame(container, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        dept_frame.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        ctk.CTkLabel(dept_frame, text="DEPARTMENT DISTRIBUTION", font=("Segoe UI", 11, "bold"), text_color=("#475569", "#94a3b8")).pack(anchor="w", padx=15, pady=(12, 8))

        dept_counts = self.employee_service.get_department_counts()
        if not dept_counts:
            ctk.CTkLabel(dept_frame, text="No department data found.", font=("Segoe UI", 10), text_color="#94a3b8").pack(padx=15, pady=20)
        else:
            for dept, count in list(dept_counts.items())[:7]:
                row = ctk.CTkFrame(dept_frame, fg_color="transparent")
                row.pack(fill="x", padx=15, pady=3)
                ctk.CTkLabel(row, text=dept, font=("Segoe UI", 10)).pack(side="left")
                ctk.CTkLabel(row, text=str(count), font=("Segoe UI", 10, "bold"), text_color="#3b82f6").pack(side="right")

        # Right Card: Recently Registered / Updated Employees
        recent_frame = ctk.CTkFrame(container, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        recent_frame.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)

        ctk.CTkLabel(recent_frame, text="RECENT EMPLOYEE ACTIVITY", font=("Segoe UI", 11, "bold"), text_color=("#475569", "#94a3b8")).pack(anchor="w", padx=15, pady=(12, 8))

        summary = self.employee_service.get_dashboard_summary()
        recent_list = summary.get("recent_employees", [])

        if not recent_list:
            ctk.CTkLabel(recent_frame, text="No employees recorded yet.", font=("Segoe UI", 10), text_color="#94a3b8").pack(padx=15, pady=20)
        else:
            # Header row
            tbl_head = ctk.CTkFrame(recent_frame, fg_color=("#f1f5f9", "#0f172a"))
            tbl_head.pack(fill="x", padx=15, pady=(2, 4))
            ctk.CTkLabel(tbl_head, text="Code", width=80, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=4)
            ctk.CTkLabel(tbl_head, text="Full Name", width=140, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=4)
            ctk.CTkLabel(tbl_head, text="Department", width=120, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=4)
            ctk.CTkLabel(tbl_head, text="Status", width=60, font=("Segoe UI", 9, "bold"), anchor="center").pack(side="right", padx=4)

            for emp in recent_list:
                item_row = ctk.CTkFrame(recent_frame, fg_color="transparent")
                item_row.pack(fill="x", padx=15, pady=2)
                ctk.CTkLabel(item_row, text=emp.employee_code, width=80, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=4)
                ctk.CTkLabel(item_row, text=emp.full_name, width=140, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=4)
                ctk.CTkLabel(item_row, text=emp.department, width=120, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=4)

                status_color = "#10b981" if emp.status == "Active" else "#94a3b8"
                ctk.CTkLabel(item_row, text=emp.status, width=60, font=("Segoe UI", 9, "bold"), text_color=status_color, anchor="center").pack(side="right", padx=4)

    def _navigate(self, target: str) -> None:
        if self.navigate_callback:
            self.navigate_callback(target)

    def refresh(self) -> None:
        """Refreshes all dashboard statistics."""
        for child in self.winfo_children():
            child.destroy()
        self._build_header()
        self._build_kpi_cards()
        self._build_quick_actions()
        self._build_distribution_and_recent()
