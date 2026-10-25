"""
Employee Form Dialog for Create and Edit Operations.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements Poka-Yoke input controls with immediate visual validation guidance.
"""

from datetime import datetime
import customtkinter as ctk
from typing import Optional, Callable, Dict, Any
from tkinter import messagebox

from models.employee import Employee
from services.employee_service import EmployeeService
from services.validation_service import ALLOWED_DEPARTMENTS, ALLOWED_STATUSES


class EmployeeFormDialog(ctk.CTkToplevel):
    """Modal dialog for creating and editing employee records."""

    def __init__(
        self,
        parent,
        employee_service: EmployeeService,
        employee: Optional[Employee] = None,
        on_success: Optional[Callable[[], None]] = None
    ):
        super().__init__(parent)

        self.employee_service = employee_service
        self.employee = employee
        self.on_success = on_success
        self.is_edit = employee is not None

        title_text = "Edit Employee Record" if self.is_edit else "Register New Employee"
        self.title(title_text)
        self.geometry("520x620")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        if self.is_edit:
            self._populate_fields()

    def _build_ui(self) -> None:
        """Constructs form layout and input widgets."""
        self.grid_columnconfigure(0, weight=1)

        # Title
        header = "EDIT EMPLOYEE" if self.is_edit else "NEW EMPLOYEE REGISTRATION"
        ctk.CTkLabel(self, text=header, font=("Segoe UI", 14, "bold"), text_color=("#0f172a", "#f8fafc")).pack(pady=(16, 4))
        ctk.CTkLabel(self, text="All fields are required. Poka-Yoke validation is active.", font=("Segoe UI", 9), text_color=("#64748b", "#94a3b8")).pack(pady=(0, 10))

        # Error banner
        self.lbl_error = ctk.CTkLabel(self, text="", font=("Segoe UI", 10, "bold"), text_color="#ef4444")
        self.lbl_error.pack(pady=(0, 6))

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=5)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        row = 0

        # 1. Employee Code
        ctk.CTkLabel(form_frame, text="Employee Code *", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(4, 1))
        ctk.CTkLabel(form_frame, text="Full Name *", font=("Segoe UI", 10, "bold")).grid(row=row, column=1, sticky="w", pady=(4, 1), padx=(10, 0))
        row += 1

        self.entry_code = ctk.CTkEntry(form_frame, placeholder_text="e.g. EMP-1050", height=32)
        self.entry_code.grid(row=row, column=0, sticky="ew", pady=(0, 8))

        self.entry_name = ctk.CTkEntry(form_frame, placeholder_text="Full Name", height=32)
        self.entry_name.grid(row=row, column=1, sticky="ew", pady=(0, 8), padx=(10, 0))
        row += 1

        # 2. Department & Designation
        ctk.CTkLabel(form_frame, text="Department *", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(4, 1))
        ctk.CTkLabel(form_frame, text="Job Designation *", font=("Segoe UI", 10, "bold")).grid(row=row, column=1, sticky="w", pady=(4, 1), padx=(10, 0))
        row += 1

        self.combo_dept = ctk.CTkComboBox(form_frame, values=ALLOWED_DEPARTMENTS, height=32)
        self.combo_dept.grid(row=row, column=0, sticky="ew", pady=(0, 8))
        self.combo_dept.set(ALLOWED_DEPARTMENTS[0])

        self.entry_desig = ctk.CTkEntry(form_frame, placeholder_text="e.g. Software Engineer", height=32)
        self.entry_desig.grid(row=row, column=1, sticky="ew", pady=(0, 8), padx=(10, 0))
        row += 1

        # 3. Email & Phone
        ctk.CTkLabel(form_frame, text="Email Address *", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(4, 1))
        ctk.CTkLabel(form_frame, text="Phone Number *", font=("Segoe UI", 10, "bold")).grid(row=row, column=1, sticky="w", pady=(4, 1), padx=(10, 0))
        row += 1

        self.entry_email = ctk.CTkEntry(form_frame, placeholder_text="user@company.com", height=32)
        self.entry_email.grid(row=row, column=0, sticky="ew", pady=(0, 8))

        self.entry_phone = ctk.CTkEntry(form_frame, placeholder_text="+91 9876543210", height=32)
        self.entry_phone.grid(row=row, column=1, sticky="ew", pady=(0, 8), padx=(10, 0))
        row += 1

        # 4. Date of Joining & Status
        ctk.CTkLabel(form_frame, text="Date of Joining (YYYY-MM-DD) *", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(4, 1))
        ctk.CTkLabel(form_frame, text="Employment Status *", font=("Segoe UI", 10, "bold")).grid(row=row, column=1, sticky="w", pady=(4, 1), padx=(10, 0))
        row += 1

        self.entry_doj = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", height=32)
        self.entry_doj.grid(row=row, column=0, sticky="ew", pady=(0, 8))
        if not self.is_edit:
            self.entry_doj.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.combo_status = ctk.CTkComboBox(form_frame, values=ALLOWED_STATUSES, height=32)
        self.combo_status.grid(row=row, column=1, sticky="ew", pady=(0, 8), padx=(10, 0))
        self.combo_status.set("Active")

        # Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(15, 20))

        btn_cancel = ctk.CTkButton(btn_frame, text="Cancel", fg_color="#64748b", hover_color="#475569", width=100, height=34, command=self.destroy)
        btn_cancel.pack(side="left")

        save_text = "Save Changes" if self.is_edit else "Create Employee"
        btn_save = ctk.CTkButton(btn_frame, text=save_text, fg_color="#2563eb", hover_color="#1d4ed8", width=140, height=34, command=self._on_save)
        btn_save.pack(side="right")

    def _populate_fields(self) -> None:
        """Loads existing employee data into the form."""
        if not self.employee:
            return
        self.entry_code.insert(0, self.employee.employee_code)
        self.entry_name.insert(0, self.employee.full_name)
        if self.employee.department in ALLOWED_DEPARTMENTS:
            self.combo_dept.set(self.employee.department)
        self.entry_desig.insert(0, self.employee.designation)
        self.entry_email.insert(0, self.employee.email)
        self.entry_phone.insert(0, self.employee.phone)
        self.entry_doj.delete(0, "end")
        self.entry_doj.insert(0, self.employee.date_of_joining)
        self.combo_status.set(self.employee.status)

    def _on_save(self) -> None:
        """Validates inputs and commits to SQLite database."""
        data = {
            "employee_code": self.entry_code.get().strip(),
            "full_name": self.entry_name.get().strip(),
            "department": self.combo_dept.get().strip(),
            "designation": self.entry_desig.get().strip(),
            "email": self.entry_email.get().strip(),
            "phone": self.entry_phone.get().strip(),
            "date_of_joining": self.entry_doj.get().strip(),
            "status": self.combo_status.get().strip()
        }

        if self.is_edit and self.employee and self.employee.id:
            success, msg = self.employee_service.update_employee(self.employee.id, data)
        else:
            success, msg, _ = self.employee_service.create_employee(data)

        if success:
            messagebox.showinfo("Success", msg)
            if self.on_success:
                self.on_success()
            self.destroy()
        else:
            self.lbl_error.configure(text=msg)
