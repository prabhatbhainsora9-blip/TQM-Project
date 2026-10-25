"""
Validation Service for Employee Management System (TQM Edition).
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements Poka-Yoke (Error-Proofing) principles to validate user inputs
prior to database transactions, providing explicit, human-friendly error messages.
"""

import re
from datetime import datetime
from typing import Tuple, Dict, Any, List

# Standard valid email regex (RFC 5322 compatible simplified)
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Standard phone regex (allowing digits, optional +, -, spaces, parentheses, minimum 10 digits)
PHONE_DIGITS_REGEX = re.compile(r"\d")

# Allowed controlled vocabulary
ALLOWED_DEPARTMENTS = [
    "Human Resources",
    "Engineering",
    "Quality Assurance",
    "Operations",
    "Finance",
    "Marketing",
    "Information Technology",
    "Research & Development"
]

ALLOWED_STATUSES = ["Active", "Inactive"]

DEFECT_CATEGORIES = [
    "Validation Error",
    "Database Error",
    "UI Glitch",
    "Report Formatting",
    "Data Inconsistency",
    "Performance Lag",
    "Security/Permission",
    "Documentation"
]

DEFECT_SEVERITIES = ["Low", "Medium", "High", "Critical"]
DEFECT_STATUSES = ["Open", "In Progress", "Resolved", "Closed"]


class ValidationService:
    """Provides centralized validation functions for all system entities."""

    @staticmethod
    def validate_employee(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates an employee record according to business constraints.
        Returns: (True, "") on success, or (False, "Reason") on failure.
        """
        # 1. Employee Code
        code = str(data.get("employee_code", "")).strip()
        if not code:
            return False, "Employee Code is required (e.g., EMP-1001)."
        if len(code) < 3 or len(code) > 20:
            return False, "Employee Code must be between 3 and 20 characters."

        # 2. Full Name
        name = str(data.get("full_name", "")).strip()
        if not name:
            return False, "Full Name is required."
        if len(name) < 2 or len(name) > 100:
            return False, "Full Name must be between 2 and 100 characters."
        if not any(c.isalpha() for c in name):
            return False, "Full Name must contain alphabetic characters."

        # 3. Department
        dept = str(data.get("department", "")).strip()
        if not dept:
            return False, "Department is required."

        # 4. Designation
        designation = str(data.get("designation", "")).strip()
        if not designation:
            return False, "Job Designation is required."

        # 5. Email
        email = str(data.get("email", "")).strip()
        if not email:
            return False, "Email address is required."
        if not EMAIL_REGEX.match(email):
            return False, f"Invalid email format: '{email}'. Example: user@organization.com"

        # 6. Phone Number
        phone = str(data.get("phone", "")).strip()
        if not phone:
            return False, "Phone Number is required."
        digits = PHONE_DIGITS_REGEX.findall(phone)
        if len(digits) < 10 or len(digits) > 15:
            return False, f"Phone Number must contain between 10 and 15 digits (found {len(digits)})."

        # 7. Date of Joining
        doj = str(data.get("date_of_joining", "")).strip()
        if not doj:
            return False, "Date of Joining is required."
        try:
            parsed_date = datetime.strptime(doj, "%Y-%m-%d").date()
            if parsed_date.year < 1970 or parsed_date.year > 2050:
                return False, "Date of Joining year must be between 1970 and 2050."
        except ValueError:
            return False, f"Invalid date format for '{doj}'. Expected format is YYYY-MM-DD (e.g., 2026-05-15)."

        # 8. Status
        status = str(data.get("status", "")).strip()
        if status not in ALLOWED_STATUSES:
            return False, f"Status must be one of: {', '.join(ALLOWED_STATUSES)}."

        return True, ""

    @staticmethod
    def validate_fmea_item(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates an FMEA record.
        Severity (S), Occurrence (O), Detection (D) must be integers between 1 and 10.
        """
        process_comp = str(data.get("process_component", "")).strip()
        if not process_comp:
            return False, "Process or Component description is required."

        failure_mode = str(data.get("potential_failure_mode", "")).strip()
        if not failure_mode:
            return False, "Potential Failure Mode is required."

        # Validate numeric ratings (1-10)
        for field, name in [
            ("severity", "Severity (S)"),
            ("occurrence", "Occurrence (O)"),
            ("detection", "Detection (D)")
        ]:
            val = data.get(field)
            try:
                num = int(val)
                if num < 1 or num > 10:
                    return False, f"{name} rating must be an integer between 1 and 10."
            except (ValueError, TypeError):
                return False, f"{name} must be a valid integer between 1 and 10."

        return True, ""

    @staticmethod
    def validate_defect(data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates a defect entry for the TQM Defect Log."""
        desc = str(data.get("description", "")).strip()
        if not desc:
            return False, "Defect description is required."

        module = str(data.get("module", "")).strip()
        if not module:
            return False, "Module name is required."

        category = str(data.get("category", "")).strip()
        if category not in DEFECT_CATEGORIES:
            return False, f"Category must be one of: {', '.join(DEFECT_CATEGORIES)}."

        severity = str(data.get("severity", "")).strip()
        if severity not in DEFECT_SEVERITIES:
            return False, f"Severity must be one of: {', '.join(DEFECT_SEVERITIES)}."

        status = str(data.get("status", "Open")).strip()
        if not status:
            status = "Open"
        if status not in DEFECT_STATUSES:
            return False, f"Status must be one of: {', '.join(DEFECT_STATUSES)}."

        occ = data.get("occurrence_count", 1)
        try:
            occ_num = int(occ)
            if occ_num < 1:
                return False, "Occurrence count must be at least 1."
        except (ValueError, TypeError):
            return False, "Occurrence count must be an integer."

        return True, ""

    @staticmethod
    def validate_pdca(data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates a PDCA improvement cycle entry."""
        title = str(data.get("title", "")).strip()
        if not title:
            return False, "Cycle Title is required."

        problem = str(data.get("plan_problem", "")).strip()
        if not problem:
            return False, "Plan: Problem Statement is required."

        action = str(data.get("plan_action", "")).strip()
        if not action:
            return False, "Plan: Proposed Action is required."

        return True, ""

    @staticmethod
    def validate_settings(settings: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates application system settings."""
        records = settings.get("records_per_page")
        try:
            r_num = int(records)
            if r_num < 5 or r_num > 200:
                return False, "Records per page must be between 5 and 200."
        except (ValueError, TypeError):
            return False, "Records per page must be a valid number."

        scaling = settings.get("scaling")
        try:
            s_num = float(scaling)
            if s_num < 0.7 or s_num > 1.5:
                return False, "Interface scaling must be between 0.7 and 1.5."
        except (ValueError, TypeError):
            return False, "Scaling must be a valid decimal number."

        theme = str(settings.get("theme", "")).strip()
        if theme not in ["Dark", "Light", "System"]:
            return False, "Theme must be 'Dark', 'Light', or 'System'."

        return True, ""
