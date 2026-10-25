"""
Defect Model for TQM Quality Tracking and SQC Pareto Analysis.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import sqlite3


@dataclass
class Defect:
    """Domain model representing a recorded software or operational defect."""
    defect_code: str
    date_detected: str
    module: str
    description: str
    category: str
    severity: str
    occurrence_count: int = 1
    root_cause: Optional[str] = None
    corrective_action: Optional[str] = None
    status: str = "Open"
    resolution_date: Optional[str] = None
    verification_notes: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts model to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Defect":
        """Factory method to construct Defect from SQLite Row."""
        return cls(
            id=row["id"],
            defect_code=row["defect_code"],
            date_detected=row["date_detected"],
            module=row["module"],
            description=row["description"],
            category=row["category"],
            severity=row["severity"],
            occurrence_count=row["occurrence_count"],
            root_cause=row["root_cause"],
            corrective_action=row["corrective_action"],
            status=row["status"],
            resolution_date=row["resolution_date"],
            verification_notes=row["verification_notes"],
            created_at=row["created_at"]
        )
