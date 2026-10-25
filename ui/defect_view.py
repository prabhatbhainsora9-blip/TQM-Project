"""
TQM Defect Log and Checksheet Tracking View.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements persistent defect logging, classification, status lifecycle,
and real-time checksheet aggregation for SQC analysis.
"""

from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any, List

from models.defect import Defect
from services.tqm_service import TQMService
from services.validation_service import DEFECT_CATEGORIES, DEFECT_SEVERITIES, DEFECT_STATUSES


class DefectView(ctk.CTkFrame):
    """Defect log table, filter toolbar, and checksheet aggregator."""

    def __init__(self, master, tqm_service: TQMService, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.tqm_service = tqm_service
        self.defects_cache: List[Defect] = []

        self._build_toolbar()
        self._build_checksheet_summary()
        self._build_table_header()
        self._build_table_body()

        self.reload_data()

    def _build_toolbar(self) -> None:
        """Top toolbar with status and category filters and add defect button."""
        bar = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        bar.pack(fill="x", padx=10, pady=(10, 6))

        ctk.CTkLabel(bar, text="Filter by Status:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(12, 4), pady=8)
        self.combo_status = ctk.CTkComboBox(bar, values=["ALL"] + DEFECT_STATUSES, width=130, height=32, command=lambda v: self.reload_data())
        self.combo_status.pack(side="left", padx=4, pady=8)
        self.combo_status.set("ALL")

        ctk.CTkLabel(bar, text="Category:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(10, 4), pady=8)
        self.combo_category = ctk.CTkComboBox(bar, values=["ALL"] + DEFECT_CATEGORIES, width=160, height=32, command=lambda v: self.reload_data())
        self.combo_category.pack(side="left", padx=4, pady=8)
        self.combo_category.set("ALL")

        btn_add = ctk.CTkButton(bar, text="+ Log Quality Defect", width=150, height=32, fg_color="#ef4444", hover_color="#dc2626", command=self._open_add_dialog)
        btn_add.pack(side="right", padx=12, pady=8)

        btn_refresh = ctk.CTkButton(bar, text="Refresh", width=80, height=32, fg_color="#475569", hover_color="#334155", command=self.reload_data)
        btn_refresh.pack(side="right", padx=4, pady=8)

    def _build_checksheet_summary(self) -> None:
        """Summary card displaying the TQM checksheet aggregated by category."""
        self.checksheet_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        self.checksheet_frame.pack(fill="x", padx=10, pady=(0, 6))

        title = ctk.CTkLabel(self.checksheet_frame, text="TQM DEFECT CHECKSHEET SUMMARY (By Quality Category & Severity)", font=("Segoe UI", 10, "bold"), text_color=("#475569", "#94a3b8"))
        title.pack(anchor="w", padx=15, pady=(8, 4))

        self.checksheet_content = ctk.CTkFrame(self.checksheet_frame, fg_color="transparent")
        self.checksheet_content.pack(fill="x", padx=15, pady=(0, 8))

    def _render_checksheet_items(self) -> None:
        for child in self.checksheet_content.winfo_children():
            child.destroy()

        summary_data = self.tqm_service.get_defect_checksheet()
        if not summary_data:
            ctk.CTkLabel(self.checksheet_content, text="No defect records available for checksheet aggregation.", font=("Segoe UI", 9), text_color="#94a3b8").pack(anchor="w")
            return

        # Render horizontal pills for categories
        pills_frame = ctk.CTkFrame(self.checksheet_content, fg_color="transparent")
        pills_frame.pack(fill="x")

        for item in summary_data[:5]:
            pill = ctk.CTkFrame(pills_frame, fg_color=("#f1f5f9", "#0f172a"), corner_radius=6)
            pill.pack(side="left", padx=4, pady=2)

            cat = item["category"]
            total = item["total_occurrences"]
            crit = item["critical_count"]
            txt = f"{cat}: {total} total (Crit: {crit})"
            ctk.CTkLabel(pill, text=txt, font=("Segoe UI", 9, "bold"), padx=8, pady=4).pack()

    def _build_table_header(self) -> None:
        head = ctk.CTkFrame(self, height=32, fg_color=("#e2e8f0", "#0f172a"), corner_radius=6)
        head.pack(fill="x", padx=10, pady=(2, 2))

        cols = [
            ("Code", 75),
            ("Date", 85),
            ("Module", 110),
            ("Category", 130),
            ("Severity", 80),
            ("Count", 55),
            ("Description", 240),
            ("Status", 90),
            ("Actions", 130)
        ]
        for name, width in cols:
            ctk.CTkLabel(head, text=name, width=width, font=("Segoe UI", 9, "bold"), anchor="w" if name != "Actions" else "center").pack(side="left", padx=2)

    def _build_table_body(self) -> None:
        self.table_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.table_scroll.pack(fill="both", expand=True, padx=10, pady=2)

    def reload_data(self) -> None:
        status = self.combo_status.get()
        cat = self.combo_category.get()
        self.defects_cache = self.tqm_service.get_all_defects(
            status=status if status != "ALL" else None,
            category=cat if cat != "ALL" else None
        )
        self._render_checksheet_items()
        self._render_rows()

    def _render_rows(self) -> None:
        for child in self.table_scroll.winfo_children():
            child.destroy()

        if not self.defects_cache:
            ctk.CTkLabel(self.table_scroll, text="No defects found matching current filters.", font=("Segoe UI", 11), text_color="#94a3b8").pack(pady=40)
            return

        for i, d in enumerate(self.defects_cache):
            bg = ("#ffffff", "#1e293b") if i % 2 == 0 else ("#f8fafc", "#0f172a")
            row = ctk.CTkFrame(self.table_scroll, fg_color=bg, corner_radius=4, height=36)
            row.pack(fill="x", pady=1)

            ctk.CTkLabel(row, text=d.defect_code, width=75, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=d.date_detected, width=85, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=d.module, width=110, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=d.category, width=130, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)

            sev_color = "#ef4444" if d.severity in ["Critical", "High"] else "#f59e0b" if d.severity == "Medium" else "#10b981"
            ctk.CTkLabel(row, text=d.severity, width=80, font=("Segoe UI", 9, "bold"), text_color=sev_color, anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=str(d.occurrence_count), width=55, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)

            desc_text = d.description[:35] + "..." if len(d.description) > 35 else d.description
            ctk.CTkLabel(row, text=desc_text, width=240, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)

            st_color = "#10b981" if d.status in ["Resolved", "Closed"] else "#ef4444"
            ctk.CTkLabel(row, text=d.status, width=90, font=("Segoe UI", 9, "bold"), text_color=st_color, anchor="center").pack(side="left", padx=2)

            # Actions
            act = ctk.CTkFrame(row, fg_color="transparent", width=130)
            act.pack(side="left", padx=2)

            btn_res = ctk.CTkButton(act, text="Resolve", width=55, height=24, fg_color="#10b981", hover_color="#059669", command=lambda cur=d: self._open_resolve_dialog(cur))
            btn_res.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(act, text="Delete", width=55, height=24, fg_color="#64748b", hover_color="#475569", command=lambda cur=d: self._delete_defect(cur))
            btn_del.pack(side="left", padx=2)

    def _open_add_dialog(self) -> None:
        dlg = ctk.CTkToplevel(self)
        dlg.title("Log Quality Defect")
        dlg.geometry("480x560")
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="LOG NEW QUALITY DEFECT", font=("Segoe UI", 13, "bold")).pack(pady=(15, 8))

        form = ctk.CTkFrame(dlg, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=25, pady=5)

        ctk.CTkLabel(form, text="Module Name *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_mod = ctk.CTkEntry(form, placeholder_text="e.g. Employee Form", height=30)
        ent_mod.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(form, text="Defect Description *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_desc = ctk.CTkEntry(form, placeholder_text="Describe observed defect...", height=30)
        ent_desc.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(form, text="Category *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        cmb_cat = ctk.CTkComboBox(form, values=DEFECT_CATEGORIES, height=30)
        cmb_cat.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(form, text="Severity *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        cmb_sev = ctk.CTkComboBox(form, values=DEFECT_SEVERITIES, height=30)
        cmb_sev.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(form, text="Occurrence Count", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_cnt = ctk.CTkEntry(form, placeholder_text="1", height=30)
        ent_cnt.insert(0, "1")
        ent_cnt.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(form, text="Root Cause (Investigated / Suspected)", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_rc = ctk.CTkEntry(form, placeholder_text="Identified root cause", height=30)
        ent_rc.pack(fill="x", pady=(1, 6))

        def _save():
            data = {
                "module": ent_mod.get().strip(),
                "description": ent_desc.get().strip(),
                "category": cmb_cat.get().strip(),
                "severity": cmb_sev.get().strip(),
                "occurrence_count": ent_cnt.get().strip() or "1",
                "root_cause": ent_rc.get().strip(),
                "status": "Open",
                "date_detected": datetime.now().strftime("%Y-%m-%d")
            }
            ok, msg, _ = self.tqm_service.log_defect(data)
            if ok:
                messagebox.showinfo("Success", msg)
                self.reload_data()
                dlg.destroy()
            else:
                messagebox.showerror("Validation Error", msg)

        btn_box = ctk.CTkFrame(dlg, fg_color="transparent")
        btn_box.pack(fill="x", padx=25, pady=(10, 20))
        ctk.CTkButton(btn_box, text="Cancel", width=90, fg_color="#64748b", command=dlg.destroy).pack(side="left")
        ctk.CTkButton(btn_box, text="Record Defect", width=130, fg_color="#ef4444", command=_save).pack(side="right")

    def _open_resolve_dialog(self, defect: Defect) -> None:
        dlg = ctk.CTkToplevel(self)
        dlg.title(f"Resolve Defect: {defect.defect_code}")
        dlg.geometry("450x380")
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text=f"RESOLVE DEFECT {defect.defect_code}", font=("Segoe UI", 12, "bold")).pack(pady=(15, 6))

        form = ctk.CTkFrame(dlg, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=25, pady=5)

        ctk.CTkLabel(form, text="Corrective Action Implemented *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_ca = ctk.CTkEntry(form, placeholder_text="Detail corrective action", height=32)
        if defect.corrective_action:
            ent_ca.insert(0, defect.corrective_action)
        ent_ca.pack(fill="x", pady=(2, 8))

        ctk.CTkLabel(form, text="Verification Notes *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_vn = ctk.CTkEntry(form, placeholder_text="e.g. Unit tests passed, Poka-Yoke verified", height=32)
        if defect.verification_notes:
            ent_vn.insert(0, defect.verification_notes)
        ent_vn.pack(fill="x", pady=(2, 8))

        ctk.CTkLabel(form, text="New Status *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        cmb_st = ctk.CTkComboBox(form, values=["Resolved", "Closed", "In Progress", "Open"], height=32)
        cmb_st.set("Resolved")
        cmb_st.pack(fill="x", pady=(2, 8))

        def _resolve():
            ca = ent_ca.get().strip()
            vn = ent_vn.get().strip()
            if not ca:
                messagebox.showerror("Error", "Corrective action must be specified.")
                return

            data = defect.to_dict()
            data["corrective_action"] = ca
            data["verification_notes"] = vn
            data["status"] = cmb_st.get()
            data["resolution_date"] = datetime.now().strftime("%Y-%m-%d")

            if defect.id:
                ok, msg = self.tqm_service.update_defect(defect.id, data)
                if ok:
                    messagebox.showinfo("Resolved", f"Defect {defect.defect_code} marked as {data['status']}.")
                    self.reload_data()
                    dlg.destroy()
                else:
                    messagebox.showerror("Error", msg)

        btn_box = ctk.CTkFrame(dlg, fg_color="transparent")
        btn_box.pack(fill="x", padx=25, pady=(10, 20))
        ctk.CTkButton(btn_box, text="Cancel", width=90, fg_color="#64748b", command=dlg.destroy).pack(side="left")
        ctk.CTkButton(btn_box, text="Update Status", width=120, fg_color="#10b981", command=_resolve).pack(side="right")

    def _delete_defect(self, defect: Defect) -> None:
        ans = messagebox.askyesno("Confirm Deletion", f"Permanently delete defect record '{defect.defect_code}'?")
        if ans and defect.id:
            ok, msg = self.tqm_service.delete_defect(defect.id)
            if ok:
                self.reload_data()
            else:
                messagebox.showerror("Error", msg)
