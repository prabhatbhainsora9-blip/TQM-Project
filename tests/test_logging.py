"""
Unit tests for Activity Logging (Feature 4: Activity Logs).
"""

import os
import tempfile
import logging
from services.logging_service import setup_logging, log_activity, read_log_entries, LOGGER_NAME


def test_activity_logging_records_event():
    """Verifies that log_activity writes formatted entries into the log file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "test.log")
        logger = setup_logging(log_dir=tmpdir, log_file=log_file, log_level="DEBUG")
        try:
            log_activity("TEST_EVENT", "This is a test audit event", module="TEST", level="INFO")

            # Read back log file
            assert os.path.exists(log_file)
            entries = read_log_entries(log_file_path=log_file, max_lines=10)
            assert len(entries) > 0
            assert any("This is a test audit event" in e["message"] for e in entries)
        finally:
            # Release Windows file locks
            for h in list(logger.handlers):
                h.close()
            logger.handlers.clear()


def test_log_filtering_by_level_and_search():
    """Verifies level and query filtering in read_log_entries."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "test.log")
        logger = setup_logging(log_dir=tmpdir, log_file=log_file, log_level="DEBUG")
        try:
            log_activity("OP_SUCCESS", "Record created cleanly", module="EMPLOYEE", level="INFO")
            log_activity("OP_WARN", "Record update near limit", module="EMPLOYEE", level="WARNING")
            log_activity("OP_FAIL", "Fatal database lock error", module="DATABASE", level="ERROR")

            # Filter by ERROR level
            err_entries = read_log_entries(log_file_path=log_file, level_filter="ERROR")
            assert len(err_entries) == 1
            assert "Fatal database lock error" in err_entries[0]["message"]

            # Filter by search string
            search_entries = read_log_entries(log_file_path=log_file, search_text="near limit")
            assert len(search_entries) == 1
            assert "Record update near limit" in search_entries[0]["message"]
        finally:
            # Release Windows file locks
            for h in list(logger.handlers):
                h.close()
            logger.handlers.clear()
