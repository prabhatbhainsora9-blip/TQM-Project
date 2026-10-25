"""
Employee Directory and CRUD Management View.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements sortable, paginated employee table, real-time search,
multi-criteria filtering, and safe CRUD operations with confirmation modals.
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional, Callable

from models.employee import Employee
from services.employee_service import EmployeeService
from services.validation_service import ALLOWED_DEPARTMENTS
from ui.employee_form import EmployeeFormDialog
from ui.components.pagination import PaginationControl


class EmployeeView(ctk.CTkFrame):
    """Primary Employee Management CRUD interface."""

    def __init__(
        self,
        master,
        employee_service: EmployeeService,
        records_per_page: int = 10,
        confirm_delete: bool = True,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.employee_service = employee_service
        self.page_size = records_per_page
        self.confirm_delete = confirm_delete
        self.current_page = 1
        self.selected_employee: Optional[Employee] = None
        self.sort_by = "full_name"
        self.sort_asc = True

        self.employees_cache: List[Employee] = []

        self._build_toolbar()
        self._build_table_header()
        self._build_table_body()
        self._build_pagination_bar()

        self.reload_data()

    def _build_toolbar(self) -> None:
        """Constructs search, filter, and action toolbar."""
        bar = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        bar.pack(fill="x", padx=10, pady=(10, 6))

        # Search Box
        self.entry_search = ctk.CTkEntry(bar, placeholder_text="Search code, name, email...", width=220, height=32)
        self.entry_search.pack(side="left", padx=(12, 6), pady=8)
        self.entry_search.bind("<Return>", lambda e: self.reload_data())

        btn_search = ctk.CTkButton(bar, text="Search", width=70, height=32, command=self.reload_data)
        btn_search.pack(side="left", padx=2, pady=8)

        # Department Filter
        dept_options = ["All Departments"] + ALLOWED_DEPARTMENTS
        self.combo_dept = ctk.CTkComboBox(bar, values=dept_options, width=160, height=32, command=lambda v: self.reload_data())
        self.combo_dept.pack(side="left", padx=6, pady=8)
        self.combo_dept.set("All Departments")

        # Status Filter
        status_options = ["All Statuses", "Active", "Inactive"]
        self.combo_status = ctk.CTkComboBox(bar, values=status_options, width=120, height=32, command=lambda v: self.reload_data())
        self.combo_status.pack(side="left", padx=6, pady=8)
        self.combo_status.set("All Statuses")

        # Right Action Buttons
        btn_add = ctk.CTkButton(bar, text="+ New Employee", width=120, height=32, fg_color="#2563eb", hover_color="#1d4ed8", command=self._open_create_dialog)
        btn_add.pack(side="right", padx=(4, 12), pady=8)

        btn_sample = ctk.CTkButton(bar, text="Seed Demo Data", width=120, height=32, fg_color="#475569", hover_color="#334155", command=self._seed_demo_data)
        btn_sample.pack(side="right", padx=4, pady=8)

    def _build_table_header(self) -> None:
        """Renders column headers with sorting triggers."""
        self.header_frame = ctk.CTkFrame(self, height=36, fg_color=("#e2e8f0", "#0f172a"), corner_radius=6)
        self.header_frame.pack(fill="x", padx=10, pady=(4, 2))

        cols = [
            ("Code", 80, "employee_code"),
            ("Full Name", 160, "full_name"),
            ("Department", 140, "department"),
            ("Designation", 140, "designation"),
            ("Email", 170, "email"),
            ("Phone", 110, "phone"),
            ("Joined", 90, "date_of_joining"),
            ("Status", 75, "status"),
            ("Actions", 130, None)
        ]

        for text, width, sort_field in cols:
            if sort_field:
                btn = ctk.CTkButton(
                    self.header_frame,
                    text=f"{text} ↕",
                    width=width,
                    height=28,
                    fg_color="transparent",
                    text_color=("#0f172a", "#f8fafc"),
                    font=("Segoe UI", 9, "bold"),
                    anchor="w" if text != "Status" else "center",
                    hover_color=("#cbd5e1", "#1e293b"),
                    command=lambda f=sort_field: self._sort_by(f)
                )
                btn.pack(side="left", padx=2)
            else:
                lbl = ctk.CTkLabel(
                    self.header_frame,
                    text=text,
                    width=width,
                    font=("Segoe UI", 9, "bold"),
                    anchor="center"
                )
                lbl.pack(side="left", padx=2)

    def _build_table_body(self) -> None:
        """Scrollable container for employee table rows."""
        self.table_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.table_scroll.pack(fill="both", expand=True, padx=10, pady=2)

    def _build_pagination_bar(self) -> None:
        """Footer pagination control."""
        footer_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        footer_frame.pack(fill="x", padx=10, pady=(4, 10))

        self.pagination = PaginationControl(
            footer_frame,
            total_items=0,
            page_size=self.page_size,
            on_page_changed=self._on_page_changed
        )
        self.pagination.pack(side="right", padx=12, pady=6)

        self.lbl_summary = ctk.CTkLabel(footer_frame, text="", font=("Segoe UI", 10), text_color=("#64748b", "#94a3b8"))
        self.lbl_summary.pack(side="left", padx=15, pady=6)

    def reload_data(self) -> None:
        """Fetches fresh data based on current search and filter settings."""
        query = self.entry_search.get().strip()
        dept = self.combo_dept.get().strip()
        if dept == "All Departments":
            dept = None
        status = self.combo_status.get().strip()
        if status == "All Statuses":
            status = None

        self.employees_cache = self.employee_service.search_employees(
            query=query,
            department=dept,
            status=status,
            sort_by=self.sort_by,
            ascending=self.sort_asc
        )

        total = len(self.employees_cache)
        active_count = sum(1 for e in self.employees_cache if e.status == "Active")
        self.lbl_summary.configure(text=f"Showing {total} employee(s) | Active: {active_count} | Inactive: {total - active_count}")

        self.pagination.update_counts(total, self.page_size)
        self._render_current_page()

    def _sort_by(self, field: str) -> None:
        """Toggles sort order for chosen field."""
        if self.sort_by == field:
            self.sort_asc = not self.sort_asc
        else:
            self.sort_by = field
            self.sort_asc = True
        self.reload_data()

    def _on_page_changed(self, page_num: int) -> None:
        self.current_page = page_num
        self._render_current_page()

    def _render_current_page(self) -> None:
        """Populates table rows for the active page window."""
        for child in self.table_scroll.winfo_children():
            child.destroy()

        if not self.employees_cache:
            empty_lbl = ctk.CTkLabel(
                self.table_scroll,
                text="No employee records found.\nClick '+ New Employee' to register or 'Seed Demo Data' to load sample records.",
                font=("Segoe UI", 11),
                text_color="#94a3b8"
            )
            empty_lbl.pack(pady=40)
            return

        start_idx = (self.current_page - 1) * self.page_size
        end_idx = start_idx + self.page_size
        page_records = self.employees_cache[start_idx:end_idx]

        for i, emp in enumerate(page_records):
            bg = ("#ffffff", "#1e293b") if i % 2 == 0 else ("#f8fafc", "#0f172a")
            row = ctk.CTkFrame(self.table_scroll, fg_color=bg, corner_radius=4, height=36)
            row.pack(fill="x", pady=1)

            ctk.CTkLabel(row, text=emp.employee_code, width=80, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=emp.full_name, width=160, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=emp.department, width=140, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=emp.designation, width=140, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=emp.email, width=170, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=emp.phone, width=110, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=emp.date_of_joining, width=90, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)

            status_color = "#10b981" if emp.status == "Active" else "#ef4444"
            ctk.CTkLabel(row, text=emp.status, width=75, font=("Segoe UI", 9, "bold"), text_color=status_color, anchor="center").pack(side="left", padx=2)

            # Actions buttons
            action_frame = ctk.CTkFrame(row, fg_color="transparent", width=130)
            action_frame.pack(side="left", padx=2)

            btn_edit = ctk.CTkButton(
                action_frame, text="Edit", width=55, height=24, fg_color="#3b82f6", hover_color="#2563eb",
                command=lambda e=emp: self._open_edit_dialog(e)
            )
            btn_edit.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(
                action_frame, text="Delete", width=55, height=24, fg_color="#ef4444", hover_color="#dc2626",
                command=lambda e=emp: self._delete_employee(e)
            )
            btn_del.pack(side="left", padx=2)

    def _open_create_dialog(self) -> None:
        EmployeeFormDialog(self, self.employee_service, employee=None, on_success=self.reload_data)

    def _open_edit_dialog(self, employee: Employee) -> None:
        EmployeeFormDialog(self, self.employee_service, employee=employee, on_success=self.reload_data)

    def _delete_employee(self, employee: Employee) -> None:
        """Prompts confirmation dialog before performing deletion."""
        if self.confirm_delete:
            ans = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to permanently delete employee '{employee.full_name}' ({employee.employee_code})?\nThis action cannot be undone."
            )
            if not ans:
                return

        if employee.id:
            success, msg = self.employee_service.delete_employee(employee.id)
            if success:
                messagebox.showinfo("Deleted", msg)
                self.reload_data()
            else:
                messagebox.showerror("Error", msg)

    def _seed_demo_data(self) -> None:
        """Seeds realistic demonstration records with clear disclosure."""
        ans = messagebox.askyesno(
            "Load Sample Demonstration Data",
            "This will seed 12 realistic demonstration employee records for academic evaluation and chart demonstration.\nDo you want to proceed?"
        )
        if ans:
            from database.schema import seed_sample_data
            seed_sample_data(self.employee_service.conn, clear_existing=False)
            messagebox.showinfo("Demo Data Loaded", "Sample demonstration employee records loaded successfully.")
            self.reload_data()
