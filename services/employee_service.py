"""
Employee Service for CRUD Operations, Searching, and Filtering.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements business logic for managing employees with parameterized queries,
data integrity validation, and operational activity logging.
"""

from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
import sqlite3

from models.employee import Employee
from services.validation_service import ValidationService
from services.logging_service import log_activity, get_logger


class EmployeeService:
    """Handles all employee database operations and business logic."""

    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn
        self.logger = get_logger()

    def create_employee(self, data: Dict[str, Any], operator: str = "Admin") -> Tuple[bool, str, Optional[int]]:
        """
        Validates and creates a new employee record.
        Returns: (success: bool, message: str, new_id: Optional[int])
        """
        # 1. Poka-Yoke Validation
        valid, err_msg = ValidationService.validate_employee(data)
        if not valid:
            log_activity("VALIDATION_FAILED", f"Employee creation failed: {err_msg}", module="EMPLOYEE", level="WARNING", user=operator, db_conn=self.conn)
            return False, err_msg, None

        code = str(data["employee_code"]).strip()
        email = str(data["email"]).strip()

        # 2. Duplicate code check
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM employees WHERE employee_code = ?", (code,))
        if cursor.fetchone():
            msg = f"Employee code '{code}' already exists. Please use a unique code."
            log_activity("DUPLICATE_CODE", msg, module="EMPLOYEE", level="WARNING", user=operator, db_conn=self.conn)
            return False, msg, None

        # 3. Duplicate email check
        cursor.execute("SELECT id FROM employees WHERE email = ?", (email,))
        if cursor.fetchone():
            msg = f"Email '{email}' is already registered to another employee."
            log_activity("DUPLICATE_EMAIL", msg, module="EMPLOYEE", level="WARNING", user=operator, db_conn=self.conn)
            return False, msg, None

        # 4. Insert into database
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute(
                """
                INSERT INTO employees 
                (employee_code, full_name, department, designation, email, phone, date_of_joining, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    code,
                    str(data["full_name"]).strip(),
                    str(data["department"]).strip(),
                    str(data["designation"]).strip(),
                    email,
                    str(data["phone"]).strip(),
                    str(data["date_of_joining"]).strip(),
                    str(data.get("status", "Active")).strip(),
                    now_str,
                    now_str
                )
            )
            self.conn.commit()
            new_id = cursor.lastrowid
            log_activity("EMPLOYEE_CREATED", f"Created employee {code} ({data['full_name']})", module="EMPLOYEE", level="INFO", user=operator, db_conn=self.conn)
            return True, f"Employee '{code}' created successfully.", new_id
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            msg = f"Database integrity error: {e}"
            log_activity("DB_ERROR", msg, module="EMPLOYEE", level="ERROR", user=operator, db_conn=self.conn)
            return False, msg, None
        except Exception as e:
            self.conn.rollback()
            msg = f"Unexpected error creating employee: {e}"
            log_activity("SYSTEM_ERROR", msg, module="EMPLOYEE", level="ERROR", user=operator, db_conn=self.conn)
            return False, msg, None

    def update_employee(self, emp_id: int, data: Dict[str, Any], operator: str = "Admin") -> Tuple[bool, str]:
        """Validates and updates an existing employee record."""
        valid, err_msg = ValidationService.validate_employee(data)
        if not valid:
            log_activity("VALIDATION_FAILED", f"Employee update failed for ID {emp_id}: {err_msg}", module="EMPLOYEE", level="WARNING", user=operator, db_conn=self.conn)
            return False, err_msg

        cursor = self.conn.cursor()
        cursor.execute("SELECT id, employee_code, email FROM employees WHERE id = ?", (emp_id,))
        existing = cursor.fetchone()
        if not existing:
            return False, f"Employee with ID {emp_id} does not exist."

        code = str(data["employee_code"]).strip()
        email = str(data["email"]).strip()

        # Check code uniqueness if changed
        if code != existing["employee_code"]:
            cursor.execute("SELECT id FROM employees WHERE employee_code = ? AND id != ?", (code, emp_id))
            if cursor.fetchone():
                return False, f"Employee code '{code}' is already in use by another record."

        # Check email uniqueness if changed
        if email != existing["email"]:
            cursor.execute("SELECT id FROM employees WHERE email = ? AND id != ?", (email, emp_id))
            if cursor.fetchone():
                return False, f"Email '{email}' is already in use by another employee."

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute(
                """
                UPDATE employees
                SET employee_code = ?, full_name = ?, department = ?, designation = ?, email = ?,
                    phone = ?, date_of_joining = ?, status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    code,
                    str(data["full_name"]).strip(),
                    str(data["department"]).strip(),
                    str(data["designation"]).strip(),
                    email,
                    str(data["phone"]).strip(),
                    str(data["date_of_joining"]).strip(),
                    str(data.get("status", "Active")).strip(),
                    now_str,
                    emp_id
                )
            )
            self.conn.commit()
            log_activity("EMPLOYEE_UPDATED", f"Updated employee ID {emp_id} ({code})", module="EMPLOYEE", level="INFO", user=operator, db_conn=self.conn)
            return True, f"Employee '{code}' updated successfully."
        except Exception as e:
            self.conn.rollback()
            msg = f"Error updating employee: {e}"
            log_activity("DB_ERROR", msg, module="EMPLOYEE", level="ERROR", user=operator, db_conn=self.conn)
            return False, msg

    def delete_employee(self, emp_id: int, operator: str = "Admin") -> Tuple[bool, str]:
        """Safely deletes an employee record after verification."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT employee_code, full_name FROM employees WHERE id = ?", (emp_id,))
        emp = cursor.fetchone()
        if not emp:
            return False, f"Employee with ID {emp_id} does not exist."

        code = emp["employee_code"]
        name = emp["full_name"]
        try:
            cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
            self.conn.commit()
            log_activity("EMPLOYEE_DELETED", f"Deleted employee {code} ({name})", module="EMPLOYEE", level="INFO", user=operator, db_conn=self.conn)
            return True, f"Employee '{name}' ({code}) deleted successfully."
        except Exception as e:
            self.conn.rollback()
            msg = f"Error deleting employee: {e}"
            log_activity("DB_ERROR", msg, module="EMPLOYEE", level="ERROR", user=operator, db_conn=self.conn)
            return False, msg

    def get_employee_by_id(self, emp_id: int) -> Optional[Employee]:
        """Retrieves single employee by database ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
        row = cursor.fetchone()
        return Employee.from_row(row) if row else None

    def get_employee_by_code(self, code: str) -> Optional[Employee]:
        """Retrieves single employee by employee code."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE employee_code = ?", (code,))
        row = cursor.fetchone()
        return Employee.from_row(row) if row else None

    def search_employees(
        self,
        query: str = "",
        department: Optional[str] = None,
        status: Optional[str] = None,
        sort_by: str = "full_name",
        ascending: bool = True
    ) -> List[Employee]:
        """
        Searches and filters employees with SQL parameterization and sorting.
        Safe against SQL injection.
        """
        allowed_sort_fields = {
            "id": "id",
            "employee_code": "employee_code",
            "full_name": "full_name",
            "department": "department",
            "designation": "designation",
            "email": "email",
            "date_of_joining": "date_of_joining",
            "status": "status"
        }
        order_col = allowed_sort_fields.get(sort_by, "full_name")
        order_dir = "ASC" if ascending else "DESC"

        sql = "SELECT * FROM employees WHERE 1=1"
        params: List[Any] = []

        if query:
            clean_q = f"%{query.strip()}%"
            sql += """ AND (
                employee_code LIKE ? OR 
                full_name LIKE ? OR 
                email LIKE ? OR 
                designation LIKE ? OR 
                department LIKE ? OR
                phone LIKE ?
            )"""
            params.extend([clean_q] * 6)

        if department and department.upper() != "ALL":
            sql += " AND department = ?"
            params.append(department)

        if status and status.upper() != "ALL":
            sql += " AND status = ?"
            params.append(status)

        sql += f" ORDER BY {order_col} {order_dir}"

        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return [Employee.from_row(r) for r in rows]

    def get_department_counts(self) -> Dict[str, int]:
        """Returns distribution count of employees per department."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT department, COUNT(*) as cnt FROM employees GROUP BY department ORDER BY cnt DESC")
        return {row["department"]: row["cnt"] for row in cursor.fetchall()}

    def get_status_counts(self) -> Dict[str, int]:
        """Returns counts for Active and Inactive employees."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT status, COUNT(*) as cnt FROM employees GROUP BY status")
        res = {"Active": 0, "Inactive": 0}
        for row in cursor.fetchall():
            res[row["status"]] = row["cnt"]
        return res

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Aggregates metrics for the executive dashboard."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM employees")
        total = cursor.fetchone()[0]

        status_counts = self.get_status_counts()
        dept_counts = self.get_department_counts()

        cursor.execute("SELECT * FROM employees ORDER BY id DESC LIMIT 5")
        recent_employees = [Employee.from_row(r) for r in cursor.fetchall()]

        return {
            "total_employees": total,
            "active_employees": status_counts.get("Active", 0),
            "inactive_employees": status_counts.get("Inactive", 0),
            "department_counts": dept_counts,
            "recent_employees": recent_employees
        }
