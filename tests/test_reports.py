"""
Unit tests for ReportService CSV, Excel, and PDF document exports.
"""

import os
import tempfile
import sqlite3
from services.report_service import ReportService
from database.schema import seed_sample_data


def test_reports_export_csv_excel_pdf(test_db_conn: sqlite3.Connection):
    """Verifies that employee directory CSV, Excel, and PDF reports generate without exceptions."""
    seed_sample_data(test_db_conn, clear_existing=False)

    with tempfile.TemporaryDirectory() as tmpdir:
        report_service = ReportService(db_conn=test_db_conn, output_dir=tmpdir)

        # 1. Export CSV
        ok_csv, path_csv = report_service.export_employees_csv()
        assert ok_csv is True
        assert os.path.exists(path_csv)
        assert os.path.getsize(path_csv) > 0

        # 2. Export Excel
        ok_excel, path_excel = report_service.export_employees_excel()
        assert ok_excel is True
        assert os.path.exists(path_excel)
        assert os.path.getsize(path_excel) > 0

        # 3. Export PDF
        ok_pdf, path_pdf = report_service.export_employees_pdf()
        assert ok_pdf is True
        assert os.path.exists(path_pdf)
        assert os.path.getsize(path_pdf) > 0

        # 4. Export Defects PDF
        ok_def_pdf, path_def_pdf = report_service.export_defects_pdf()
        assert ok_def_pdf is True
        assert os.path.exists(path_def_pdf)
        assert os.path.getsize(path_def_pdf) > 0

        # 5. Export FMEA PDF
        ok_fmea_pdf, path_fmea_pdf = report_service.export_fmea_pdf()
        assert ok_fmea_pdf is True
        assert os.path.exists(path_fmea_pdf)
        assert os.path.getsize(path_fmea_pdf) > 0
