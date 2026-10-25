"""
Report Generation and Export Service.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Generates professional, structured CSV, Excel, and PDF reports for:
- Employee Directory & Department Summaries
- TQM Defect Log & Checksheets
- FMEA Risk Register
- PDCA Continuous Improvement Records
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
import sqlite3

from services.logging_service import log_activity, get_logger

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class ReportService:
    """Manages CSV, Excel, and PDF structured exports."""

    def __init__(self, db_conn: sqlite3.Connection, output_dir: str = "reports"):
        self.conn = db_conn
        self.output_dir = os.path.abspath(output_dir)
        self.logger = get_logger()
        os.makedirs(self.output_dir, exist_ok=True)

    # =========================================================================
    # 1. EMPLOYEE REPORTS
    # =========================================================================

    def export_employees_csv(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """Exports all employee records to CSV."""
        try:
            df = pd.read_sql_query("SELECT employee_code, full_name, department, designation, email, phone, date_of_joining, status FROM employees ORDER BY employee_code", self.conn)
            fname = filename or f"employee_directory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            out_path = os.path.join(self.output_dir, fname)
            df.to_csv(out_path, index=False, encoding="utf-8")
            log_activity("REPORT_GENERATED", f"Exported employees CSV: {fname}", module="REPORT")
            return True, out_path
        except Exception as e:
            return False, f"Failed to export CSV: {e}"

    def export_employees_excel(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """Exports all employee records to Excel (.xlsx)."""
        try:
            df = pd.read_sql_query("SELECT employee_code, full_name, department, designation, email, phone, date_of_joining, status FROM employees ORDER BY employee_code", self.conn)
            fname = filename or f"employee_directory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            out_path = os.path.join(self.output_dir, fname)
            with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Employees", index=False)
            log_activity("REPORT_GENERATED", f"Exported employees Excel: {fname}", module="REPORT")
            return True, out_path
        except Exception as e:
            return False, f"Failed to export Excel: {e}"

    def export_employees_pdf(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """Generates a professional Employee Directory PDF."""
        try:
            df = pd.read_sql_query("SELECT employee_code, full_name, department, designation, email, phone, status FROM employees ORDER BY employee_code", self.conn)
            fname = filename or f"employee_directory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            out_path = os.path.join(self.output_dir, fname)

            doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
            styles = getSampleStyleSheet()

            elements = []
            title_style = ParagraphStyle(
                "DocTitle",
                parent=styles["Heading1"],
                fontSize=18,
                leading=22,
                textColor=colors.HexColor("#0f172a"),
                spaceAfter=6
            )
            sub_style = ParagraphStyle(
                "DocSub",
                parent=styles["Normal"],
                fontSize=10,
                leading=14,
                textColor=colors.HexColor("#475569"),
                spaceAfter=15
            )

            elements.append(Paragraph("Employee Management System — Employee Directory", title_style))
            elements.append(Paragraph(f"Student: Prabhat Singh Bhainsora (Roll: 2410302046) | Course: BBAT104 (TQM)<br/>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total Employees: {len(df)}", sub_style))

            table_data = [["Code", "Full Name", "Department", "Designation", "Email", "Status"]]
            for _, row in df.iterrows():
                table_data.append([
                    str(row["employee_code"]),
                    str(row["full_name"]),
                    str(row["department"]),
                    str(row["designation"]),
                    str(row["email"]),
                    str(row["status"])
                ])

            t = Table(table_data, colWidths=[65, 110, 105, 110, 115, 50])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
            ]))
            elements.append(t)

            doc.build(elements)
            log_activity("REPORT_GENERATED", f"Exported employees PDF: {fname}", module="REPORT")
            return True, out_path
        except Exception as e:
            return False, f"Failed to export PDF: {e}"

    # =========================================================================
    # 2. TQM DEFECT CHECK SHEET & LOG REPORTS
    # =========================================================================

    def export_defects_csv(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """Exports all defect records to CSV."""
        try:
            df = pd.read_sql_query("SELECT defect_code, date_detected, module, description, category, severity, occurrence_count, status, root_cause, corrective_action FROM defects ORDER BY id DESC", self.conn)
            fname = filename or f"tqm_defects_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            out_path = os.path.join(self.output_dir, fname)
            df.to_csv(out_path, index=False, encoding="utf-8")
            log_activity("REPORT_GENERATED", f"Exported defects CSV: {fname}", module="REPORT")
            return True, out_path
        except Exception as e:
            return False, f"Failed to export defects CSV: {e}"

    def export_defects_pdf(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """Generates TQM Defect Log & Checksheet PDF report."""
        try:
            df = pd.read_sql_query("SELECT defect_code, date_detected, module, category, severity, occurrence_count, status FROM defects ORDER BY id DESC", self.conn)
            fname = filename or f"tqm_defect_checksheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            out_path = os.path.join(self.output_dir, fname)

            doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
            styles = getSampleStyleSheet()

            elements = []
            title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=18, textColor=colors.HexColor("#0f172a"), spaceAfter=6)
            sub_style = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#475569"), spaceAfter=15)

            elements.append(Paragraph("TQM Defect Log & Checksheet Audit Report", title_style))
            elements.append(Paragraph(f"Student: Prabhat Singh Bhainsora (2410302046) | Quality Goal: Q11 - Improve Maintainability<br/>Total Defect Observations: {df['occurrence_count'].sum() if not df.empty else 0}", sub_style))

            table_data = [["Code", "Date", "Module", "Category", "Severity", "Count", "Status"]]
            for _, r in df.iterrows():
                table_data.append([
                    str(r["defect_code"]),
                    str(r["date_detected"]),
                    str(r["module"]),
                    str(r["category"]),
                    str(r["severity"]),
                    str(r["occurrence_count"]),
                    str(r["status"])
                ])

            t = Table(table_data, colWidths=[65, 75, 95, 115, 65, 45, 65])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0fdfa")]),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
            ]))
            elements.append(t)

            doc.build(elements)
            log_activity("REPORT_GENERATED", f"Exported defects PDF: {fname}", module="REPORT")
            return True, out_path
        except Exception as e:
            return False, f"Failed to export defects PDF: {e}"

    # =========================================================================
    # 3. FMEA RISK REGISTER REPORT
    # =========================================================================

    def export_fmea_pdf(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """Generates FMEA Risk Priority Register PDF report."""
        try:
            df = pd.read_sql_query("SELECT item_code, process_component, potential_failure_mode, severity, occurrence, detection, rpn, status FROM fmea_records ORDER BY rpn DESC", self.conn)
            fname = filename or f"fmea_risk_register_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            out_path = os.path.join(self.output_dir, fname)

            doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
            styles = getSampleStyleSheet()

            elements = []
            title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=18, textColor=colors.HexColor("#0f172a"), spaceAfter=6)
            sub_style = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#475569"), spaceAfter=15)

            elements.append(Paragraph("FMEA Risk Priority Register (RPN Analysis)", title_style))
            elements.append(Paragraph("RPN = Severity (1-10) x Occurrence (1-10) x Detection (1-10)<br/>High Risk Threshold: RPN >= 120", sub_style))

            table_data = [["Code", "Component", "Failure Mode", "S", "O", "D", "RPN", "Status"]]
            for _, r in df.iterrows():
                table_data.append([
                    str(r["item_code"]),
                    str(r["process_component"]),
                    str(r["potential_failure_mode"]),
                    str(r["severity"]),
                    str(r["occurrence"]),
                    str(r["detection"]),
                    str(r["rpn"]),
                    str(r["status"])
                ])

            t = Table(table_data, colWidths=[60, 110, 160, 25, 25, 25, 45, 60])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#b91c1c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fef2f2")]),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
            ]))
            elements.append(t)

            doc.build(elements)
            log_activity("REPORT_GENERATED", f"Exported FMEA PDF: {fname}", module="REPORT")
            return True, out_path
        except Exception as e:
            return False, f"Failed to export FMEA PDF: {e}"

    # =========================================================================
    # 4. PDCA CONTINUOUS IMPROVEMENT REPORT
    # =========================================================================

    def export_pdca_pdf(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """Generates PDCA Continuous Improvement Audit Report."""
        try:
            df = pd.read_sql_query("SELECT cycle_code, title, plan_problem, plan_action, check_target_achieved, act_status FROM pdca_records ORDER BY id DESC", self.conn)
            fname = filename or f"pdca_improvement_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            out_path = os.path.join(self.output_dir, fname)

            doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
            styles = getSampleStyleSheet()

            elements = []
            title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=18, textColor=colors.HexColor("#0f172a"), spaceAfter=6)
            sub_style = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#475569"), spaceAfter=15)

            elements.append(Paragraph("PDCA Continuous Improvement Audit Report", title_style))
            elements.append(Paragraph("Deming Plan-Do-Check-Act Kaizen Execution History", sub_style))

            table_data = [["Code", "Cycle Title", "Problem Statement", "Corrective Action", "Target Achieved?", "Status"]]
            for _, r in df.iterrows():
                table_data.append([
                    str(r["cycle_code"]),
                    str(r["title"]),
                    str(r["plan_problem"])[:40] + "...",
                    str(r["plan_action"])[:40] + "...",
                    str(r["check_target_achieved"]),
                    str(r["act_status"])
                ])

            t = Table(table_data, colWidths=[65, 110, 120, 120, 80, 70])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4338ca")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2ff")]),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
            ]))
            elements.append(t)

            doc.build(elements)
            log_activity("REPORT_GENERATED", f"Exported PDCA PDF: {fname}", module="REPORT")
            return True, out_path
        except Exception as e:
            return False, f"Failed to export PDCA PDF: {e}"
