"""
Unit tests for Statistical Quality Control (SQC) analytics and Pareto 80/20 mathematics.
"""

from analytics.pareto import ParetoAnalyzer
from services.tqm_service import TQMService


def test_pareto_cumulative_percentage_calculation():
    """Verifies that ParetoAnalyzer correctly computes cumulative sums and percentages."""
    counts = {
        "Validation Error": 50,
        "Database Lock": 25,
        "UI Glitch": 15,
        "Report Formatting": 10
    }
    # Total = 100
    df = ParetoAnalyzer.calculate_pareto_data(counts)

    assert len(df) == 4
    # Highest count first
    assert df.iloc[0]["Category"] == "Validation Error"
    assert df.iloc[0]["Count"] == 50
    assert df.iloc[0]["CumulativePercentage"] == 50.0

    # Second row
    assert df.iloc[1]["Category"] == "Database Lock"
    assert df.iloc[1]["CumulativeSum"] == 75
    assert df.iloc[1]["CumulativePercentage"] == 75.0

    # Final row must equal 100%
    assert df.iloc[-1]["CumulativePercentage"] == 100.0


def test_pareto_handles_empty_dataset():
    """Verifies graceful handling when defect counts are empty."""
    df = ParetoAnalyzer.calculate_pareto_data({})
    assert df.empty

    fig, summary = ParetoAnalyzer.generate_chart({})
    assert summary["total_defects"] == 0
    assert len(summary["vital_few"]) == 0


def test_tqm_checksheet_aggregation_avoids_double_counting(tqm_service: TQMService):
    """Verifies that checksheet correctly groups by category and sums distinct occurrences."""
    tqm_service.log_defect({
        "defect_code": "DEF-T1",
        "module": "Form",
        "description": "Email syntax error",
        "category": "Validation Error",
        "severity": "High",
        "occurrence_count": 5
    })
    tqm_service.log_defect({
        "defect_code": "DEF-T2",
        "module": "Form",
        "description": "Phone format error",
        "category": "Validation Error",
        "severity": "Medium",
        "occurrence_count": 3
    })
    tqm_service.log_defect({
        "defect_code": "DEF-T3",
        "module": "DB",
        "description": "Lock timeout",
        "category": "Database Error",
        "severity": "Critical",
        "occurrence_count": 2
    })

    checksheet = tqm_service.get_defect_checksheet()
    assert len(checksheet) >= 2

    val_item = next(item for item in checksheet if item["category"] == "Validation Error")
    assert val_item["total_occurrences"] == 8
    assert val_item["distinct_defects"] == 2
    assert val_item["high_count"] == 5
    assert val_item["medium_count"] == 3


def test_fishbone_diagram_generation(tqm_service: TQMService):
    """Verifies that FishboneGenerator creates a valid Matplotlib figure from recorded causes."""
    from analytics.fishbone import FishboneGenerator
    causes = tqm_service.get_fishbone_causes()
    assert "People" in causes
    assert "Process" in causes
    assert "Software Code" in causes
    assert "Infrastructure" in causes

    fig = FishboneGenerator.generate_diagram("Test Problem Statement", causes)
    assert fig is not None
    import matplotlib.pyplot as plt
    plt.close(fig)


def test_sipoc_and_ctq_diagram_generation():
    """Verifies that SIPOCMapper and CTQTree produce valid non-empty Matplotlib figures."""
    from analytics.sipoc import SIPOCMapper
    from analytics.ctq import CTQTree
    import matplotlib.pyplot as plt

    sipoc_fig = SIPOCMapper.generate_diagram()
    assert sipoc_fig is not None
    plt.close(sipoc_fig)

    ctq_fig = CTQTree.generate_diagram()
    assert ctq_fig is not None
    plt.close(ctq_fig)

