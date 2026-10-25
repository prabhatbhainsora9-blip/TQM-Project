"""
FMEA Model for Failure Mode and Effects Analysis.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Calculates Risk Priority Number (RPN) = Severity * Occurrence * Detection.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import sqlite3


@dataclass
class FMEARecord:
    """Domain model representing a Failure Mode and Effects Analysis item."""
    item_code: str
    process_component: str
    potential_failure_mode: str
    potential_effects: str
    potential_causes: str
    current_controls: str
    severity: int
    occurrence: int
    detection: int
    recommended_action: str
    rpn: Optional[int] = None
    responsible_person: Optional[str] = None
    status: str = "Open"
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        """Automatically calculates RPN if not explicitly set."""
        if self.rpn is None:
            self.rpn = self.calculate_rpn(self.severity, self.occurrence, self.detection)

    @staticmethod
    def calculate_rpn(severity: int, occurrence: int, detection: int) -> int:
        """Calculates RPN = Severity * Occurrence * Detection."""
        return int(severity) * int(occurrence) * int(detection)

    def to_dict(self) -> Dict[str, Any]:
        """Converts model to dictionary."""
        return asdict(self)

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "FMEARecord":
        """Factory method to construct FMEARecord from an SQLite Row."""
        return cls(
            id=row["id"],
            item_code=row["item_code"],
            process_component=row["process_component"],
            potential_failure_mode=row["potential_failure_mode"],
            potential_effects=row["potential_effects"],
            potential_causes=row["potential_causes"],
            current_controls=row["current_controls"],
            severity=row["severity"],
            occurrence=row["occurrence"],
            detection=row["detection"],
            rpn=row["rpn"],
            recommended_action=row["recommended_action"],
            responsible_person=row["responsible_person"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
