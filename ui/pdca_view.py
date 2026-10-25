"""
PDCA (Plan-Do-Check-Act) Continuous Improvement Tracking View.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements Deming cycle records, before-and-after verification metrics,
standardization notes, and lifecycle status tracking.
"""

from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, List, Dict, Any

from models.pdca import PDCARecord
from services.tqm_service import TQMService


class PDCAView(ctk.CTkFrame):
    """Interface for managing continuous Kaizen improvement initiatives."""

    def __init__(self, master, tqm_service: TQMService, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.tqm_service = tqm_service
        self.pdca_records: List[PDCARecord] = []

        self._build_toolbar()
        self._build_table_header()
        self._build_table_body()

        self.reload_data()

    def _build_toolbar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        bar.pack(fill="x", padx=10, pady=(10, 6))

        ctk.CTkLabel(bar, text="PDCA CONTINUOUS IMPROVEMENT (Kaizen Cycles)", font=("Segoe UI", 12, "bold"), text_color=("#0f172a", "#f8fafc")).pack(side="left", padx=15, pady=8)

        btn_add = ctk.CTkButton(bar, text="+ New PDCA Cycle", width=140, height=32, fg_color="#8b5cf6", hover_color="#7c3aed", command=self._open_create_dialog)
        btn_add.pack(side="right", padx=12, pady=8)

        btn_refresh = ctk.CTkButton(bar, text="Refresh", width=80, height=32, fg_color="#475569", hover_color="#334155", command=self.reload_data)
        btn_refresh.pack(side="right", padx=4, pady=8)

    def _build_table_header(self) -> None:
        head = ctk.CTkFrame(self, height=32, fg_color=("#e2e8f0", "#0f172a"), corner_radius=6)
        head.pack(fill="x", padx=10, pady=(2, 2))

        cols = [
            ("Code", 75),
            ("Title / Initiative", 220),
            ("Problem Statement", 230),
            ("Before -> After Metric", 170),
            ("Target Met?", 100),
            ("Stage / Status", 110),
            ("Actions", 120)
        ]
        for name, width in cols:
            ctk.CTkLabel(head, text=name, width=width, font=("Segoe UI", 9, "bold"), anchor="w" if name not in ["Target Met?", "Stage / Status", "Actions"] else "center").pack(side="left", padx=2)

    def _build_table_body(self) -> None:
        self.table_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.table_scroll.pack(fill="both", expand=True, padx=10, pady=2)

    def reload_data(self) -> None:
        self.pdca_records = self.tqm_service.get_all_pdca_records()
        self._render_rows()

    def _render_rows(self) -> None:
        for child in self.table_scroll.winfo_children():
            child.destroy()

        if not self.pdca_records:
            ctk.CTkLabel(self.table_scroll, text="No PDCA cycles recorded yet. Click '+ New PDCA Cycle' to start an improvement initiative.", font=("Segoe UI", 11), text_color="#94a3b8").pack(pady=40)
            return

        for i, p in enumerate(self.pdca_records):
            bg = ("#ffffff", "#1e293b") if i % 2 == 0 else ("#f8fafc", "#0f172a")
            row = ctk.CTkFrame(self.table_scroll, fg_color=bg, corner_radius=4, height=38)
            row.pack(fill="x", pady=1)

            ctk.CTkLabel(row, text=p.cycle_code, width=75, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=p.title[:32], width=220, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=2)

            prob_short = p.plan_problem[:34] + "..." if len(p.plan_problem) > 34 else p.plan_problem
            ctk.CTkLabel(row, text=prob_short, width=230, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)

            metric_str = f"{p.check_before_metric or '-'} -> {p.check_after_metric or '-'}"
            metric_short = metric_str[:25] + "..." if len(metric_str) > 25 else metric_str
            ctk.CTkLabel(row, text=metric_short, width=170, font=("Segoe UI", 8), anchor="w").pack(side="left", padx=2)

            achieved_color = "#10b981" if "Yes" in (p.check_target_achieved or "") else "#ef4444" if "No" in (p.check_target_achieved or "") else "#f59e0b"
            ctk.CTkLabel(row, text=p.check_target_achieved or "Pending", width=100, font=("Segoe UI", 9, "bold"), text_color=achieved_color, anchor="center").pack(side="left", padx=2)

            st_color = "#10b981" if p.act_status in ["Standardized", "Completed"] else "#8b5cf6"
            ctk.CTkLabel(row, text=p.act_status, width=110, font=("Segoe UI", 9, "bold"), text_color=st_color, anchor="center").pack(side="left", padx=2)

            # Actions
            act = ctk.CTkFrame(row, fg_color="transparent", width=120)
            act.pack(side="left", padx=2)

            btn_view = ctk.CTkButton(act, text="View/Edit", width=60, height=24, fg_color="#3b82f6", command=lambda cur=p: self._open_edit_dialog(cur))
            btn_view.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(act, text="Delete", width=50, height=24, fg_color="#ef4444", hover_color="#dc2626", command=lambda cur=p: self._delete_pdca(cur))
            btn_del.pack(side="left", padx=2)

    def _open_create_dialog(self) -> None:
        dlg = ctk.CTkToplevel(self)
        dlg.title("New PDCA Continuous Improvement Cycle")
        dlg.geometry("540x650")
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="CREATE PDCA KAIZEN CYCLE", font=("Segoe UI", 13, "bold")).pack(pady=(12, 4))

        scroll = ctk.CTkScrollableFrame(dlg, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25, pady=5)

        ctk.CTkLabel(scroll, text="Initiative Title *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_title = ctk.CTkEntry(scroll, placeholder_text="e.g. Reduction of Input Validation Errors", height=30)
        ent_title.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="PLAN: Problem Statement *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_prob = ctk.CTkEntry(scroll, placeholder_text="Define the observed problem", height=30)
        ent_prob.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="PLAN: Baseline Metric", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_base = ctk.CTkEntry(scroll, placeholder_text="e.g. 30 errors per 100 entries", height=30)
        ent_base.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="PLAN: Target Metric", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_tgt = ctk.CTkEntry(scroll, placeholder_text="e.g. < 5 errors per 100 entries", height=30)
        ent_tgt.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="PLAN: Proposed Action *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_act = ctk.CTkEntry(scroll, placeholder_text="Action to be executed", height=30)
        ent_act.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="Responsible Owner", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_owner = ctk.CTkEntry(scroll, placeholder_text="e.g. Prabhat Singh Bhainsora", height=30)
        ent_owner.insert(0, "Prabhat Singh Bhainsora")
        ent_owner.pack(fill="x", pady=(1, 6))

        def _save():
            data = {
                "title": ent_title.get().strip(),
                "plan_problem": ent_prob.get().strip(),
                "plan_baseline": ent_base.get().strip(),
                "plan_target": ent_tgt.get().strip(),
                "plan_action": ent_act.get().strip(),
                "plan_owner": ent_owner.get().strip(),
                "plan_start_date": datetime.now().strftime("%Y-%m-%d"),
                "act_status": "In Plan"
            }
            ok, msg, _ = self.tqm_service.create_pdca_record(data)
            if ok:
                messagebox.showinfo("Saved", msg)
                self.reload_data()
                dlg.destroy()
            else:
                messagebox.showerror("Error", msg)

        btn_box = ctk.CTkFrame(dlg, fg_color="transparent")
        btn_box.pack(fill="x", padx=25, pady=(8, 16))
        ctk.CTkButton(btn_box, text="Cancel", width=90, fg_color="#64748b", command=dlg.destroy).pack(side="left")
        ctk.CTkButton(btn_box, text="Create Cycle", width=140, fg_color="#8b5cf6", command=_save).pack(side="right")

    def _open_edit_dialog(self, record: PDCARecord) -> None:
        dlg = ctk.CTkToplevel(self)
        dlg.title(f"PDCA Cycle: {record.cycle_code}")
        dlg.geometry("560x680")
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text=f"MANAGE PDCA CYCLE: {record.cycle_code}", font=("Segoe UI", 13, "bold")).pack(pady=(12, 4))

        scroll = ctk.CTkScrollableFrame(dlg, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25, pady=5)

        # Plan Info
        ctk.CTkLabel(scroll, text="Title:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_title = ctk.CTkEntry(scroll, height=30)
        ent_title.insert(0, record.title)
        ent_title.pack(fill="x", pady=(1, 4))

        ctk.CTkLabel(scroll, text="DO: Action Taken & Implementation Notes", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_do = ctk.CTkEntry(scroll, height=30)
        if record.do_action_taken:
            ent_do.insert(0, record.do_action_taken)
        ent_do.pack(fill="x", pady=(1, 4))

        # Check metrics
        ctk.CTkLabel(scroll, text="CHECK: Before Metric", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_bm = ctk.CTkEntry(scroll, height=30)
        if record.check_before_metric:
            ent_bm.insert(0, record.check_before_metric)
        ent_bm.pack(fill="x", pady=(1, 4))

        ctk.CTkLabel(scroll, text="CHECK: After Metric", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_am = ctk.CTkEntry(scroll, height=30)
        if record.check_after_metric:
            ent_am.insert(0, record.check_after_metric)
        ent_am.pack(fill="x", pady=(1, 4))

        ctk.CTkLabel(scroll, text="CHECK: Target Achieved?", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        cmb_ach = ctk.CTkComboBox(scroll, values=["Pending", "Yes - Target Achieved", "Yes - Target Exceeded", "No - Needs Revision"], height=30)
        if record.check_target_achieved:
            cmb_ach.set(record.check_target_achieved)
        cmb_ach.pack(fill="x", pady=(1, 4))

        ctk.CTkLabel(scroll, text="ACT: Standardization / Lessons Learned", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_act_notes = ctk.CTkEntry(scroll, height=30)
        if record.act_standardization:
            ent_act_notes.insert(0, record.act_standardization)
        ent_act_notes.pack(fill="x", pady=(1, 4))

        ctk.CTkLabel(scroll, text="Lifecycle Status", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        cmb_status = ctk.CTkComboBox(scroll, values=["In Plan", "In Implementation", "Under Evaluation", "Standardized", "Completed"], height=30)
        cmb_status.set(record.act_status)
        cmb_status.pack(fill="x", pady=(1, 4))

        def _update():
            data = record.to_dict()
            data["title"] = ent_title.get().strip()
            data["do_action_taken"] = ent_do.get().strip()
            data["do_completion_date"] = datetime.now().strftime("%Y-%m-%d")
            data["check_before_metric"] = ent_bm.get().strip()
            data["check_after_metric"] = ent_am.get().strip()
            data["check_target_achieved"] = cmb_ach.get()
            data["act_standardization"] = ent_act_notes.get().strip()
            data["act_status"] = cmb_status.get()

            if record.id:
                ok, msg = self.tqm_service.update_pdca_record(record.id, data)
                if ok:
                    messagebox.showinfo("Updated", "PDCA cycle updated successfully.")
                    self.reload_data()
                    dlg.destroy()
                else:
                    messagebox.showerror("Error", msg)

        btn_box = ctk.CTkFrame(dlg, fg_color="transparent")
        btn_box.pack(fill="x", padx=25, pady=(8, 16))
        ctk.CTkButton(btn_box, text="Cancel", width=90, fg_color="#64748b", command=dlg.destroy).pack(side="left")
        ctk.CTkButton(btn_box, text="Save Updates", width=140, fg_color="#2563eb", command=_update).pack(side="right")

    def _delete_pdca(self, record: PDCARecord) -> None:
        ans = messagebox.askyesno("Confirm Deletion", f"Permanently delete PDCA record '{record.cycle_code}'?")
        if ans and record.id:
            ok, msg = self.tqm_service.delete_pdca_record(record.id)
            if ok:
                self.reload_data()
            else:
                messagebox.showerror("Error", msg)
