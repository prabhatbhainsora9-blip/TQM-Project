"""
Employee Model for Employee Management System (TQM Edition).
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Represents an employee domain entity with dataclass serialization and type hints.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import sqlite3


@dataclass
class Employee:
    """Domain model representing an employee record."""
    employee_code: str
    full_name: str
    department: str
    designation: str
    email: str
    phone: str
    date_of_joining: str
    status: str = "Active"
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts model to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Employee":
        """Factory method to construct Employee model from an SQLite Row object."""
        return cls(
            id=row["id"],
            employee_code=row["employee_code"],
            full_name=row["full_name"],
            department=row["department"],
            designation=row["designation"],
            email=row["email"],
            phone=row["phone"],
            date_of_joining=row["date_of_joining"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
