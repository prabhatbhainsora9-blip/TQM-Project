"""
Reports and Exports Generation View.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Provides single-click generation for structured CSV, Excel, and ReportLab PDF documents.
"""

import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional

from services.report_service import ReportService


class ReportsView(ctk.CTkFrame):
    """Interface for generating audit-ready reports and document exports."""

    def __init__(self, master, report_service: ReportService, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.report_service = report_service
        self.output_dir = report_service.output_dir

        self._build_header()
        self._build_report_cards()

    def _build_header(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        bar.pack(fill="x", padx=10, pady=(10, 6))

        ctk.CTkLabel(bar, text="TQM AUDIT & COMPLIANCE REPORTING", font=("Segoe UI", 12, "bold"), text_color=("#0f172a", "#f8fafc")).pack(side="left", padx=15, pady=10)

        btn_open_folder = ctk.CTkButton(
            bar, text="Open Reports Folder", width=160, height=32, fg_color="#475569", hover_color="#334155",
            command=self._open_reports_folder
        )
        btn_open_folder.pack(side="right", padx=12, pady=10)

    def _build_report_cards(self) -> None:
        grid_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=5)
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        reports_config = [
            {
                "title": "Employee Directory Report",
                "desc": "Complete employee roster including Department, Designation, Email, Phone, and Employment Status.",
                "color": "#3b82f6",
                "exports": [
                    ("Generate PDF", lambda: self._run_export(self.report_service.export_employees_pdf)),
                    ("Export Excel (.xlsx)", lambda: self._run_export(self.report_service.export_employees_excel)),
                    ("Export CSV", lambda: self._run_export(self.report_service.export_employees_csv))
                ]
            },
            {
                "title": "TQM Defect Log & Checksheet",
                "desc": "Recorded defects, root causes, corrective actions, and aggregated category frequency checksheet.",
                "color": "#0d9488",
                "exports": [
                    ("Generate PDF", lambda: self._run_export(self.report_service.export_defects_pdf)),
                    ("Export CSV", lambda: self._run_export(self.report_service.export_defects_csv))
                ]
            },
            {
                "title": "FMEA Risk Priority Register",
                "desc": "Failure modes, causes, severity, occurrence, detection, and calculated RPN values with high-risk highlights.",
                "color": "#dc2626",
                "exports": [
                    ("Generate PDF", lambda: self._run_export(self.report_service.export_fmea_pdf))
                ]
            },
            {
                "title": "PDCA Continuous Improvement Audit",
                "desc": "Deming Kaizen cycle records with problem statements, before-and-after measurements, and standardization notes.",
                "color": "#8b5cf6",
                "exports": [
                    ("Generate PDF", lambda: self._run_export(self.report_service.export_pdca_pdf))
                ]
            }
        ]

        for i, rep in enumerate(reports_config):
            r = i // 2
            c = i % 2

            card = ctk.CTkFrame(grid_frame, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")

            title_lbl = ctk.CTkLabel(card, text=rep["title"], font=("Segoe UI", 12, "bold"), text_color=rep["color"], anchor="w")
            title_lbl.pack(fill="x", padx=16, pady=(14, 4))

            desc_lbl = ctk.CTkLabel(card, text=rep["desc"], font=("Segoe UI", 9.5), text_color=("#64748b", "#94a3b8"), wraplength=420, justify="left", anchor="w")
            desc_lbl.pack(fill="x", padx=16, pady=(0, 14))

            btn_box = ctk.CTkFrame(card, fg_color="transparent")
            btn_box.pack(fill="x", padx=16, pady=(0, 14))

            for btn_text, action in rep["exports"]:
                btn = ctk.CTkButton(btn_box, text=btn_text, width=120, height=30, fg_color=rep["color"], command=action)
                btn.pack(side="left", padx=(0, 8))

    def _run_export(self, export_fn) -> None:
        try:
            ok, out_or_err = export_fn()
            if ok:
                fname = os.path.basename(out_or_err)
                ans = messagebox.askyesno(
                    "Report Generated",
                    f"Report successfully saved:\n{fname}\n\nWould you like to open the reports folder now?"
                )
                if ans:
                    self._open_reports_folder()
            else:
                messagebox.showerror("Export Failed", out_or_err)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during export:\n{e}")

    def _open_reports_folder(self) -> None:
        """Opens Windows Explorer to output directory."""
        try:
            os.startfile(self.output_dir)
        except Exception:
            subprocess.run(["explorer", self.output_dir])
