"""
PDCA Model for Deming Continuous Improvement Cycle.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Models the 4-phase Deming cycle: Plan -> Do -> Check -> Act.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import sqlite3


@dataclass
class PDCARecord:
    """Domain model representing a continuous improvement initiative."""
    cycle_code: str
    title: str
    plan_problem: str
    plan_action: str
    plan_baseline: Optional[str] = None
    plan_root_cause: Optional[str] = None
    plan_target: Optional[str] = None
    plan_owner: Optional[str] = None
    plan_start_date: Optional[str] = None
    plan_target_date: Optional[str] = None
    do_action_taken: Optional[str] = None
    do_completion_date: Optional[str] = None
    do_notes: Optional[str] = None
    check_before_metric: Optional[str] = None
    check_after_metric: Optional[str] = None
    check_evidence: Optional[str] = None
    check_target_achieved: Optional[str] = "Pending"
    act_standardization: Optional[str] = None
    act_lessons_learned: Optional[str] = None
    act_followup: Optional[str] = None
    act_status: str = "In Plan"
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts model to dictionary."""
        return asdict(self)

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "PDCARecord":
        """Factory method to construct PDCARecord from an SQLite Row."""
        return cls(
            id=row["id"],
            cycle_code=row["cycle_code"],
            title=row["title"],
            plan_problem=row["plan_problem"],
            plan_baseline=row["plan_baseline"],
            plan_root_cause=row["plan_root_cause"],
            plan_target=row["plan_target"],
            plan_action=row["plan_action"],
            plan_owner=row["plan_owner"],
            plan_start_date=row["plan_start_date"],
            plan_target_date=row["plan_target_date"],
            do_action_taken=row["do_action_taken"],
            do_completion_date=row["do_completion_date"],
            do_notes=row["do_notes"],
            check_before_metric=row["check_before_metric"],
            check_after_metric=row["check_after_metric"],
            check_evidence=row["check_evidence"],
            check_target_achieved=row["check_target_achieved"],
            act_standardization=row["act_standardization"],
            act_lessons_learned=row["act_lessons_learned"],
            act_followup=row["act_followup"],
            act_status=row["act_status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
