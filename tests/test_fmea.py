"""
Unit tests for FMEA (Failure Mode and Effects Analysis) and RPN calculations.
"""

from services.tqm_service import TQMService
from models.fmea import FMEARecord


def test_fmea_rpn_calculation_formula():
    """Verifies that RPN = Severity * Occurrence * Detection."""
    rpn = FMEARecord.calculate_rpn(severity=8, occurrence=4, detection=5)
    assert rpn == 8 * 4 * 5  # 160


def test_create_fmea_record_calculates_rpn_automatically(tqm_service: TQMService):
    """Tests saving FMEA record and verifying calculated RPN in SQLite."""
    data = {
        "item_code": "FMEA-TEST-1",
        "process_component": "Database Layer",
        "potential_failure_mode": "Disk full corruption",
        "potential_effects": "Loss of audit logs",
        "potential_causes": "Unbounded log file growth",
        "current_controls": "Manual cleanup",
        "severity": 7,
        "occurrence": 5,
        "detection": 4,
        "recommended_action": "Enable rotating file logs",
        "responsible_person": "Prabhat",
        "status": "Open"
    }
    ok, msg, new_id = tqm_service.create_fmea_record(data)
    assert ok is True
    assert "RPN = 140" in msg

    records = tqm_service.get_all_fmea_records()
    assert len(records) > 0
    saved = next(r for r in records if r.item_code == "FMEA-TEST-1")
    assert saved.rpn == 140


def test_fmea_score_out_of_bounds_rejected(tqm_service: TQMService):
    """Verifies that Severity, Occurrence, or Detection scores outside 1-10 are rejected."""
    bad_data = {
        "item_code": "FMEA-BAD",
        "process_component": "Input Form",
        "potential_failure_mode": "Typo",
        "severity": 15,  # Exceeds max 10
        "occurrence": 5,
        "detection": 3,
        "recommended_action": "Validation"
    }
    ok, msg, _ = tqm_service.create_fmea_record(bad_data)
    assert ok is False
    assert "between 1 and 10" in msg


def test_fmea_records_sorted_by_rpn_descending(tqm_service: TQMService):
    """Verifies that FMEA records can be retrieved sorted by risk priority number."""
    tqm_service.create_fmea_record({
        "item_code": "FMEA-LOW",
        "process_component": "UI",
        "potential_failure_mode": "Minor typo",
        "severity": 2, "occurrence": 2, "detection": 2,
        "recommended_action": "Fix"
    })  # RPN = 8

    tqm_service.create_fmea_record({
        "item_code": "FMEA-HIGH",
        "process_component": "Security",
        "potential_failure_mode": "Data Leak",
        "severity": 9, "occurrence": 5, "detection": 6,
        "recommended_action": "Encrypt"
    })  # RPN = 270

    records = tqm_service.get_all_fmea_records(sort_by_rpn_desc=True)
    rpns = [r.rpn for r in records if r.rpn is not None]
    assert rpns == sorted(rpns, reverse=True)
