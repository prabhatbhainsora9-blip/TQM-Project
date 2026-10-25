"""
TQM Quality Analysis Service for Defect Tracking, FMEA, PDCA, and Fishbone.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements statistical quality management workflows, RPN calculation,
Pareto aggregation, checksheet generation, and PDCA continuous improvement cycles.
"""

from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
import sqlite3

from models.defect import Defect
from models.fmea import FMEARecord
from models.pdca import PDCARecord
from services.validation_service import ValidationService
from services.logging_service import log_activity, get_logger


class TQMService:
    """Manages all TQM data operations, calculations, and lifecycle tracking."""

    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn
        self.logger = get_logger()

    # =========================================================================
    # 1. DEFECT LOG & CHECKSHEET
    # =========================================================================

    def log_defect(self, data: Dict[str, Any], operator: str = "Admin") -> Tuple[bool, str, Optional[int]]:
        """Records a new defect in the TQM defect tracking log."""
        if "status" not in data or not data["status"]:
            data["status"] = "Open"
        valid, err_msg = ValidationService.validate_defect(data)
        if not valid:
            return False, err_msg, None

        code = str(data.get("defect_code", "")).strip()
        if not code:
            # Auto-generate defect code
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM defects")
            cnt = cursor.fetchone()[0] + 1
            code = f"DEF-{cnt:03d}"

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_detected = data.get("date_detected") or datetime.now().strftime("%Y-%m-%d")

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO defects
                (defect_code, date_detected, module, description, category, severity, occurrence_count,
                 root_cause, corrective_action, status, resolution_date, verification_notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    code,
                    date_detected,
                    str(data["module"]).strip(),
                    str(data["description"]).strip(),
                    str(data["category"]).strip(),
                    str(data["severity"]).strip(),
                    int(data.get("occurrence_count", 1)),
                    data.get("root_cause"),
                    data.get("corrective_action"),
                    data.get("status", "Open"),
                    data.get("resolution_date"),
                    data.get("verification_notes"),
                    now_str
                )
            )
            self.conn.commit()
            new_id = cursor.lastrowid
            log_activity("DEFECT_LOGGED", f"Logged defect {code}: {data['description']}", module="TQM", level="INFO", user=operator, db_conn=self.conn)
            return True, f"Defect '{code}' recorded successfully.", new_id
        except Exception as e:
            self.conn.rollback()
            msg = f"Failed to log defect: {e}"
            log_activity("DB_ERROR", msg, module="TQM", level="ERROR", user=operator, db_conn=self.conn)
            return False, msg, None

    def update_defect(self, defect_id: int, data: Dict[str, Any], operator: str = "Admin") -> Tuple[bool, str]:
        """Updates an existing defect's status, root cause, or corrective action."""
        valid, err_msg = ValidationService.validate_defect(data)
        if not valid:
            return False, err_msg

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE defects
                SET module = ?, description = ?, category = ?, severity = ?, occurrence_count = ?,
                    root_cause = ?, corrective_action = ?, status = ?, resolution_date = ?,
                    verification_notes = ?
                WHERE id = ?
                """,
                (
                    str(data["module"]).strip(),
                    str(data["description"]).strip(),
                    str(data["category"]).strip(),
                    str(data["severity"]).strip(),
                    int(data.get("occurrence_count", 1)),
                    data.get("root_cause"),
                    data.get("corrective_action"),
                    data.get("status", "Open"),
                    data.get("resolution_date"),
                    data.get("verification_notes"),
                    defect_id
                )
            )
            self.conn.commit()
            log_activity("DEFECT_UPDATED", f"Updated defect ID {defect_id}", module="TQM", level="INFO", user=operator, db_conn=self.conn)
            return True, "Defect updated successfully."
        except Exception as e:
            self.conn.rollback()
            return False, f"Failed to update defect: {e}"

    def delete_defect(self, defect_id: int, operator: str = "Admin") -> Tuple[bool, str]:
        """Deletes a defect record."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM defects WHERE id = ?", (defect_id,))
            self.conn.commit()
            log_activity("DEFECT_DELETED", f"Deleted defect ID {defect_id}", module="TQM", level="INFO", user=operator, db_conn=self.conn)
            return True, "Defect deleted successfully."
        except Exception as e:
            self.conn.rollback()
            return False, f"Error deleting defect: {e}"

    def get_all_defects(self, status: Optional[str] = None, category: Optional[str] = None) -> List[Defect]:
        """Retrieves defects with optional filtering."""
        sql = "SELECT * FROM defects WHERE 1=1"
        params: List[Any] = []
        if status and status.upper() != "ALL":
            sql += " AND status = ?"
            params.append(status)
        if category and category.upper() != "ALL":
            sql += " AND category = ?"
            params.append(category)
        sql += " ORDER BY id DESC"

        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return [Defect.from_row(r) for r in cursor.fetchall()]

    def get_defect_checksheet(self) -> List[Dict[str, Any]]:
        """
        Generates a TQM Checksheet aggregating defect counts by category and severity.
        Avoids double-counting defects.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT category,
                   SUM(CASE WHEN severity = 'Critical' THEN occurrence_count ELSE 0 END) as critical_count,
                   SUM(CASE WHEN severity = 'High' THEN occurrence_count ELSE 0 END) as high_count,
                   SUM(CASE WHEN severity = 'Medium' THEN occurrence_count ELSE 0 END) as medium_count,
                   SUM(CASE WHEN severity = 'Low' THEN occurrence_count ELSE 0 END) as low_count,
                   SUM(occurrence_count) as total_occurrences,
                   COUNT(id) as distinct_defects
            FROM defects
            GROUP BY category
            ORDER BY total_occurrences DESC
            """
        )
        return [dict(r) for r in cursor.fetchall()]

    def get_category_defect_counts(self) -> Dict[str, int]:
        """Returns total defect occurrence counts grouped by category for Pareto analysis."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT category, SUM(occurrence_count) as total
            FROM defects
            GROUP BY category
            ORDER BY total DESC
            """
        )
        return {r["category"]: r["total"] for r in cursor.fetchall()}

    # =========================================================================
    # 2. FMEA (FAILURE MODE AND EFFECTS ANALYSIS)
    # =========================================================================

    def create_fmea_record(self, data: Dict[str, Any], operator: str = "Admin") -> Tuple[bool, str, Optional[int]]:
        """
        Creates an FMEA record with automatic RPN calculation.
        RPN = Severity * Occurrence * Detection (each scale 1-10).
        """
        valid, err_msg = ValidationService.validate_fmea_item(data)
        if not valid:
            return False, err_msg, None

        s = int(data["severity"])
        o = int(data["occurrence"])
        d = int(data["detection"])
        rpn = FMEARecord.calculate_rpn(s, o, d)

        code = str(data.get("item_code", "")).strip()
        if not code:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM fmea_records")
            cnt = cursor.fetchone()[0] + 1
            code = f"FMEA-{cnt:02d}"

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO fmea_records
                (item_code, process_component, potential_failure_mode, potential_effects, potential_causes,
                 current_controls, severity, occurrence, detection, rpn, recommended_action,
                 responsible_person, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    code,
                    str(data["process_component"]).strip(),
                    str(data["potential_failure_mode"]).strip(),
                    str(data.get("potential_effects", "")).strip(),
                    str(data.get("potential_causes", "")).strip(),
                    str(data.get("current_controls", "")).strip(),
                    s, o, d, rpn,
                    str(data.get("recommended_action", "")).strip(),
                    data.get("responsible_person"),
                    data.get("status", "Open"),
                    now_str,
                    now_str
                )
            )
            self.conn.commit()
            new_id = cursor.lastrowid
            log_activity("FMEA_CREATED", f"Created FMEA item {code} (RPN: {rpn})", module="TQM", level="INFO", user=operator, db_conn=self.conn)
            return True, f"FMEA item '{code}' saved with RPN = {rpn}.", new_id
        except Exception as e:
            self.conn.rollback()
            return False, f"Error saving FMEA record: {e}", None

    def update_fmea_record(self, fmea_id: int, data: Dict[str, Any], operator: str = "Admin") -> Tuple[bool, str]:
        """Updates FMEA record and recalculates RPN automatically."""
        valid, err_msg = ValidationService.validate_fmea_item(data)
        if not valid:
            return False, err_msg

        s = int(data["severity"])
        o = int(data["occurrence"])
        d = int(data["detection"])
        rpn = FMEARecord.calculate_rpn(s, o, d)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE fmea_records
                SET process_component = ?, potential_failure_mode = ?, potential_effects = ?,
                    potential_causes = ?, current_controls = ?, severity = ?, occurrence = ?,
                    detection = ?, rpn = ?, recommended_action = ?, responsible_person = ?,
                    status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    str(data["process_component"]).strip(),
                    str(data["potential_failure_mode"]).strip(),
                    str(data.get("potential_effects", "")).strip(),
                    str(data.get("potential_causes", "")).strip(),
                    str(data.get("current_controls", "")).strip(),
                    s, o, d, rpn,
                    str(data.get("recommended_action", "")).strip(),
                    data.get("responsible_person"),
                    data.get("status", "Open"),
                    now_str,
                    fmea_id
                )
            )
            self.conn.commit()
            log_activity("FMEA_UPDATED", f"Updated FMEA item ID {fmea_id} (New RPN: {rpn})", module="TQM", level="INFO", user=operator, db_conn=self.conn)
            return True, f"FMEA item updated with recalculated RPN = {rpn}."
        except Exception as e:
            self.conn.rollback()
            return False, f"Failed to update FMEA record: {e}"

    def delete_fmea_record(self, fmea_id: int, operator: str = "Admin") -> Tuple[bool, str]:
        """Deletes an FMEA record."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM fmea_records WHERE id = ?", (fmea_id,))
            self.conn.commit()
            log_activity("FMEA_DELETED", f"Deleted FMEA item ID {fmea_id}", module="TQM", level="INFO", user=operator, db_conn=self.conn)
            return True, "FMEA record deleted."
        except Exception as e:
            self.conn.rollback()
            return False, f"Error deleting FMEA record: {e}"

    def get_all_fmea_records(self, sort_by_rpn_desc: bool = True) -> List[FMEARecord]:
        """Retrieves all FMEA items sorted by risk priority number."""
        order = "DESC" if sort_by_rpn_desc else "ASC"
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM fmea_records ORDER BY rpn {order}")
        return [FMEARecord.from_row(r) for r in cursor.fetchall()]

    # =========================================================================
    # 3. PDCA CONTINUOUS IMPROVEMENT TRACKER
    # =========================================================================

    def create_pdca_record(self, data: Dict[str, Any], operator: str = "Admin") -> Tuple[bool, str, Optional[int]]:
        """Creates a new PDCA continuous improvement cycle."""
        valid, err_msg = ValidationService.validate_pdca(data)
        if not valid:
            return False, err_msg, None

        code = str(data.get("cycle_code", "")).strip()
        if not code:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pdca_records")
            cnt = cursor.fetchone()[0] + 1
            code = f"PDCA-{cnt:02d}"

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO pdca_records
                (cycle_code, title, plan_problem, plan_baseline, plan_root_cause, plan_target,
                 plan_action, plan_owner, plan_start_date, plan_target_date, do_action_taken,
                 do_completion_date, do_notes, check_before_metric, check_after_metric,
                 check_evidence, check_target_achieved, act_standardization, act_lessons_learned,
                 act_followup, act_status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    code,
                    str(data["title"]).strip(),
                    str(data["plan_problem"]).strip(),
                    data.get("plan_baseline"),
                    data.get("plan_root_cause"),
                    data.get("plan_target"),
                    str(data["plan_action"]).strip(),
                    data.get("plan_owner"),
                    data.get("plan_start_date"),
                    data.get("plan_target_date"),
                    data.get("do_action_taken"),
                    data.get("do_completion_date"),
                    data.get("do_notes"),
                    data.get("check_before_metric"),
                    data.get("check_after_metric"),
                    data.get("check_evidence"),
                    data.get("check_target_achieved", "Pending"),
                    data.get("act_standardization"),
                    data.get("act_lessons_learned"),
                    data.get("act_followup"),
                    data.get("act_status", "In Plan"),
                    now_str,
                    now_str
                )
            )
            self.conn.commit()
            new_id = cursor.lastrowid
            log_activity("PDCA_CREATED", f"Created PDCA cycle {code}: {data['title']}", module="TQM", level="INFO", user=operator, db_conn=self.conn)
            return True, f"PDCA Cycle '{code}' created.", new_id
        except Exception as e:
            self.conn.rollback()
            return False, f"Failed to create PDCA cycle: {e}", None

    def update_pdca_record(self, pdca_id: int, data: Dict[str, Any], operator: str = "Admin") -> Tuple[bool, str]:
        """Updates an ongoing PDCA improvement cycle."""
        valid, err_msg = ValidationService.validate_pdca(data)
        if not valid:
            return False, err_msg

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE pdca_records
                SET title = ?, plan_problem = ?, plan_baseline = ?, plan_root_cause = ?, plan_target = ?,
                    plan_action = ?, plan_owner = ?, plan_start_date = ?, plan_target_date = ?,
                    do_action_taken = ?, do_completion_date = ?, do_notes = ?, check_before_metric = ?,
                    check_after_metric = ?, check_evidence = ?, check_target_achieved = ?,
                    act_standardization = ?, act_lessons_learned = ?, act_followup = ?,
                    act_status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    str(data["title"]).strip(),
                    str(data["plan_problem"]).strip(),
                    data.get("plan_baseline"),
                    data.get("plan_root_cause"),
                    data.get("plan_target"),
                    str(data["plan_action"]).strip(),
                    data.get("plan_owner"),
                    data.get("plan_start_date"),
                    data.get("plan_target_date"),
                    data.get("do_action_taken"),
                    data.get("do_completion_date"),
                    data.get("do_notes"),
                    data.get("check_before_metric"),
                    data.get("check_after_metric"),
                    data.get("check_evidence"),
                    data.get("check_target_achieved", "Pending"),
                    data.get("act_standardization"),
                    data.get("act_lessons_learned"),
                    data.get("act_followup"),
                    data.get("act_status", "In Plan"),
                    now_str,
                    pdca_id
                )
            )
            self.conn.commit()
            log_activity("PDCA_UPDATED", f"Updated PDCA cycle ID {pdca_id}", module="TQM", level="INFO", user=operator, db_conn=self.conn)
            return True, "PDCA record updated."
        except Exception as e:
            self.conn.rollback()
            return False, f"Failed to update PDCA record: {e}"

    def delete_pdca_record(self, pdca_id: int, operator: str = "Admin") -> Tuple[bool, str]:
        """Deletes a PDCA record."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM pdca_records WHERE id = ?", (pdca_id,))
            self.conn.commit()
            log_activity("PDCA_DELETED", f"Deleted PDCA cycle ID {pdca_id}", module="TQM", level="INFO", user=operator, db_conn=self.conn)
            return True, "PDCA record deleted."
        except Exception as e:
            self.conn.rollback()
            return False, f"Error deleting PDCA record: {e}"

    def get_all_pdca_records(self) -> List[PDCARecord]:
        """Retrieves all PDCA improvement records."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pdca_records ORDER BY id DESC")
        return [PDCARecord.from_row(r) for r in cursor.fetchall()]

    # =========================================================================
    # 4. ISHIKAWA / FISHBONE CAUSES
    # =========================================================================

    def get_fishbone_causes(self, problem_title: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieves root causes grouped by the 4 required categories:
        People, Process, Software Code, Infrastructure.
        """
        cursor = self.conn.cursor()
        if problem_title:
            cursor.execute("SELECT * FROM fishbone_causes WHERE problem_title = ?", (problem_title,))
        else:
            cursor.execute("SELECT * FROM fishbone_causes")

        grouped: Dict[str, List[Dict[str, Any]]] = {
            "People": [],
            "Process": [],
            "Software Code": [],
            "Infrastructure": []
        }
        for row in cursor.fetchall():
            cat = row["category"]
            if cat in grouped:
                grouped[cat].append({
                    "id": row["id"],
                    "problem_title": row["problem_title"],
                    "cause_text": row["cause_text"],
                    "is_investigated": bool(row["is_investigated"])
                })
        return grouped

    def add_fishbone_cause(self, problem_title: str, category: str, cause_text: str, is_investigated: bool = False) -> bool:
        """Adds a root cause to the Fishbone diagram."""
        if category not in ["People", "Process", "Software Code", "Infrastructure"]:
            return False
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO fishbone_causes (problem_title, category, cause_text, is_investigated, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (problem_title, category, cause_text, 1 if is_investigated else 0, now_str)
            )
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False

    def delete_fishbone_cause(self, cause_id: int) -> bool:
        """Deletes a fishbone cause item."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM fishbone_causes WHERE id = ?", (cause_id,))
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False
