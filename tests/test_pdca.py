"""
Unit tests for PDCA (Plan-Do-Check-Act) Continuous Improvement cycle workflow.
"""

from services.tqm_service import TQMService


def test_pdca_lifecycle_creation_and_update(tqm_service: TQMService):
    """Tests creating and advancing a PDCA continuous improvement cycle."""
    data = {
        "cycle_code": "PDCA-T1",
        "title": "Reduce Query Latency in Search",
        "plan_problem": "Search latency exceeds 200ms without index",
        "plan_baseline": "220ms average query latency",
        "plan_root_cause": "Missing composite indices on SQLite table",
        "plan_target": "< 10ms query latency",
        "plan_action": "Add SQLite indices on employee_code and email",
        "plan_owner": "Prabhat",
        "act_status": "In Plan"
    }
    ok, msg, new_id = tqm_service.create_pdca_record(data)
    assert ok is True
    assert new_id is not None

    # Verify saved
    records = tqm_service.get_all_pdca_records()
    assert len(records) > 0
    record = next(r for r in records if r.cycle_code == "PDCA-T1")
    assert record.title == "Reduce Query Latency in Search"

    # Progress through DO -> CHECK -> ACT
    update_data = record.to_dict()
    update_data["do_action_taken"] = "Created indices idx_employees_code and idx_employees_email"
    update_data["check_before_metric"] = "220ms"
    update_data["check_after_metric"] = "4ms"
    update_data["check_evidence"] = "Benchmark timer across 1000 search queries"
    update_data["check_target_achieved"] = "Yes - Target Exceeded"
    update_data["act_standardization"] = "Included indices in schema.py CREATE_TABLES_SQL"
    update_data["act_status"] = "Standardized"

    update_ok, update_msg = tqm_service.update_pdca_record(new_id, update_data)
    assert update_ok is True

    # Verify updated record
    records_after = tqm_service.get_all_pdca_records()
    updated = next(r for r in records_after if r.cycle_code == "PDCA-T1")
    assert updated.act_status == "Standardized"
    assert updated.check_target_achieved == "Yes - Target Exceeded"
