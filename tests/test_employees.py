"""
Unit tests for Employee CRUD operations, validation rules, and search filtering.
"""

import pytest
from services.employee_service import EmployeeService


def test_create_employee_success(employee_service: EmployeeService):
    """Tests creating a valid employee record."""
    data = {
        "employee_code": "EMP-9001",
        "full_name": "Test User",
        "department": "Engineering",
        "designation": "Software Engineer",
        "email": "test.user@company.com",
        "phone": "+91 9876543210",
        "date_of_joining": "2026-01-15",
        "status": "Active"
    }
    success, msg, new_id = employee_service.create_employee(data)
    assert success is True
    assert new_id is not None

    emp = employee_service.get_employee_by_id(new_id)
    assert emp is not None
    assert emp.employee_code == "EMP-9001"
    assert emp.full_name == "Test User"


def test_duplicate_employee_code_rejected(employee_service: EmployeeService):
    """Verifies Poka-Yoke prevention of duplicate employee codes."""
    data = {
        "employee_code": "EMP-9002",
        "full_name": "First User",
        "department": "Finance",
        "designation": "Analyst",
        "email": "first@company.com",
        "phone": "9876543210",
        "date_of_joining": "2026-02-01",
        "status": "Active"
    }
    success1, _, _ = employee_service.create_employee(data)
    assert success1 is True

    # Attempt to insert same code with different email
    data["email"] = "second@company.com"
    success2, msg, _ = employee_service.create_employee(data)
    assert success2 is False
    assert "already exists" in msg


def test_invalid_email_format_rejected(employee_service: EmployeeService):
    """Verifies that invalid email syntax is caught and rejected."""
    data = {
        "employee_code": "EMP-9003",
        "full_name": "Invalid Email User",
        "department": "Marketing",
        "designation": "Manager",
        "email": "not-a-valid-email",
        "phone": "9876543210",
        "date_of_joining": "2026-03-01",
        "status": "Active"
    }
    success, msg, _ = employee_service.create_employee(data)
    assert success is False
    assert "Invalid email format" in msg


def test_short_phone_number_rejected(employee_service: EmployeeService):
    """Verifies that phone numbers with fewer than 10 digits are rejected."""
    data = {
        "employee_code": "EMP-9004",
        "full_name": "Short Phone User",
        "department": "Operations",
        "designation": "Specialist",
        "email": "phone@company.com",
        "phone": "12345",  # Only 5 digits
        "date_of_joining": "2026-03-01",
        "status": "Active"
    }
    success, msg, _ = employee_service.create_employee(data)
    assert success is False
    assert "between 10 and 15 digits" in msg


def test_invalid_date_format_rejected(employee_service: EmployeeService):
    """Verifies that dates not following YYYY-MM-DD are rejected."""
    data = {
        "employee_code": "EMP-9005",
        "full_name": "Bad Date User",
        "department": "Operations",
        "designation": "Lead",
        "email": "date@company.com",
        "phone": "9876543210",
        "date_of_joining": "15/05/2026",  # DD/MM/YYYY instead of YYYY-MM-DD
        "status": "Active"
    }
    success, msg, _ = employee_service.create_employee(data)
    assert success is False
    assert "YYYY-MM-DD" in msg


def test_update_employee_success(employee_service: EmployeeService):
    """Tests updating an existing employee's designation and status."""
    data = {
        "employee_code": "EMP-9006",
        "full_name": "Update User",
        "department": "Engineering",
        "designation": "Junior Engineer",
        "email": "update@company.com",
        "phone": "9876543210",
        "date_of_joining": "2026-04-01",
        "status": "Active"
    }
    _, _, emp_id = employee_service.create_employee(data)
    assert emp_id is not None

    update_data = dict(data)
    update_data["designation"] = "Lead Architect"
    update_data["status"] = "Inactive"

    ok, msg = employee_service.update_employee(emp_id, update_data)
    assert ok is True

    emp = employee_service.get_employee_by_id(emp_id)
    assert emp is not None
    assert emp.designation == "Lead Architect"
    assert emp.status == "Inactive"


def test_delete_employee_success(employee_service: EmployeeService):
    """Tests employee deletion."""
    data = {
        "employee_code": "EMP-9007",
        "full_name": "Delete User",
        "department": "Finance",
        "designation": "Auditor",
        "email": "delete@company.com",
        "phone": "9876543210",
        "date_of_joining": "2026-05-01",
        "status": "Active"
    }
    _, _, emp_id = employee_service.create_employee(data)
    assert emp_id is not None

    ok, msg = employee_service.delete_employee(emp_id)
    assert ok is True

    assert employee_service.get_employee_by_id(emp_id) is None


def test_search_and_filter_employees(employee_service: EmployeeService):
    """Tests multi-criteria search and department/status filtering."""
    # Insert two distinct employees
    employee_service.create_employee({
        "employee_code": "EMP-9008",
        "full_name": "Alice Wonderland",
        "department": "Human Resources",
        "designation": "Recruiter",
        "email": "alice@company.com",
        "phone": "9876543210",
        "date_of_joining": "2026-01-01",
        "status": "Active"
    })
    employee_service.create_employee({
        "employee_code": "EMP-9009",
        "full_name": "Bob Builder",
        "department": "Engineering",
        "designation": "Constructor",
        "email": "bob@company.com",
        "phone": "9876543211",
        "date_of_joining": "2026-02-01",
        "status": "Inactive"
    })

    # Query search
    res = employee_service.search_employees(query="Alice")
    assert len(res) == 1
    assert res[0].employee_code == "EMP-9008"

    # Department filter
    res_dept = employee_service.search_employees(department="Engineering")
    assert any(e.employee_code == "EMP-9009" for e in res_dept)

    # Status filter
    res_status = employee_service.search_employees(status="Inactive")
    assert all(e.status == "Inactive" for e in res_status)
