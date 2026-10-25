"""
FMEA (Failure Mode and Effects Analysis) Risk Management View.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements Risk Priority Number (RPN = S x O x D) calculations,
risk register table, and automated high-risk threshold warnings (RPN >= 120).
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, List, Dict, Any

from models.fmea import FMEARecord
from services.tqm_service import TQMService


class FMEAView(ctk.CTkFrame):
    """FMEA risk register interface with live RPN sorting and color-coded risk levels."""

    def __init__(self, master, tqm_service: TQMService, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.tqm_service = tqm_service
        self.fmea_records: List[FMEARecord] = []

        self._build_toolbar()
        self._build_info_banner()
        self._build_table_header()
        self._build_table_body()

        self.reload_data()

    def _build_toolbar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        bar.pack(fill="x", padx=10, pady=(10, 6))

        ctk.CTkLabel(bar, text="FMEA RISK REGISTER (RPN Analysis)", font=("Segoe UI", 12, "bold"), text_color=("#0f172a", "#f8fafc")).pack(side="left", padx=15, pady=8)

        btn_add = ctk.CTkButton(bar, text="+ Add FMEA Item", width=140, height=32, fg_color="#dc2626", hover_color="#b91c1c", command=self._open_add_dialog)
        btn_add.pack(side="right", padx=12, pady=8)

        btn_refresh = ctk.CTkButton(bar, text="Refresh", width=80, height=32, fg_color="#475569", hover_color="#334155", command=self.reload_data)
        btn_refresh.pack(side="right", padx=4, pady=8)

    def _build_info_banner(self) -> None:
        """Explains the RPN calculation methodology and rating scale."""
        banner = ctk.CTkFrame(self, fg_color=("#f1f5f9", "#0f172a"), corner_radius=8)
        banner.pack(fill="x", padx=10, pady=(0, 6))

        txt = (
            "Formula: RPN = Severity (S) × Occurrence (O) × Detection (D). "
            "Scale: 1 (Lowest Risk / Easiest Detection) to 10 (Critical Impact / Undetectable). "
            "Threshold: Items with RPN ≥ 120 require immediate mitigation."
        )
        ctk.CTkLabel(banner, text=txt, font=("Segoe UI", 9), text_color=("#475569", "#94a3b8"), wraplength=950, justify="left").pack(anchor="w", padx=12, pady=6)

    def _build_table_header(self) -> None:
        head = ctk.CTkFrame(self, height=32, fg_color=("#e2e8f0", "#0f172a"), corner_radius=6)
        head.pack(fill="x", padx=10, pady=(2, 2))

        cols = [
            ("Code", 75),
            ("Process / Component", 150),
            ("Potential Failure Mode", 180),
            ("Potential Effects", 170),
            ("S", 30),
            ("O", 30),
            ("D", 30),
            ("RPN", 60),
            ("Status", 80),
            ("Actions", 110)
        ]
        for name, width in cols:
            ctk.CTkLabel(head, text=name, width=width, font=("Segoe UI", 9, "bold"), anchor="w" if name not in ["S", "O", "D", "RPN", "Actions"] else "center").pack(side="left", padx=2)

    def _build_table_body(self) -> None:
        self.table_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.table_scroll.pack(fill="both", expand=True, padx=10, pady=2)

    def reload_data(self) -> None:
        self.fmea_records = self.tqm_service.get_all_fmea_records(sort_by_rpn_desc=True)
        self._render_rows()

    def _render_rows(self) -> None:
        for child in self.table_scroll.winfo_children():
            child.destroy()

        if not self.fmea_records:
            ctk.CTkLabel(self.table_scroll, text="No FMEA items found. Click '+ Add FMEA Item' to analyze potential failure modes.", font=("Segoe UI", 11), text_color="#94a3b8").pack(pady=40)
            return

        for i, f in enumerate(self.fmea_records):
            bg = ("#ffffff", "#1e293b") if i % 2 == 0 else ("#f8fafc", "#0f172a")
            row = ctk.CTkFrame(self.table_scroll, fg_color=bg, corner_radius=4, height=36)
            row.pack(fill="x", pady=1)

            ctk.CTkLabel(row, text=f.item_code, width=75, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=f.process_component[:22], width=150, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=f.potential_failure_mode[:26], width=180, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=f.potential_effects[:24], width=170, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=2)

            ctk.CTkLabel(row, text=str(f.severity), width=30, font=("Segoe UI", 9), anchor="center").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=str(f.occurrence), width=30, font=("Segoe UI", 9), anchor="center").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=str(f.detection), width=30, font=("Segoe UI", 9), anchor="center").pack(side="left", padx=2)

            rpn_val = f.rpn or 0
            rpn_color = "#dc2626" if rpn_val >= 120 else "#d97706" if rpn_val >= 80 else "#10b981"
            ctk.CTkLabel(row, text=f"{rpn_val}", width=60, font=("Segoe UI", 10, "bold"), text_color=rpn_color, anchor="center").pack(side="left", padx=2)

            st_color = "#10b981" if f.status == "Completed" else "#3b82f6"
            ctk.CTkLabel(row, text=f.status, width=80, font=("Segoe UI", 9, "bold"), text_color=st_color, anchor="center").pack(side="left", padx=2)

            # Action buttons
            act = ctk.CTkFrame(row, fg_color="transparent", width=110)
            act.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(act, text="Delete", width=50, height=24, fg_color="#ef4444", hover_color="#dc2626", command=lambda cur=f: self._delete_fmea(cur))
            btn_del.pack(side="left", padx=2)

    def _open_add_dialog(self) -> None:
        dlg = ctk.CTkToplevel(self)
        dlg.title("Add FMEA Failure Mode Item")
        dlg.geometry("520x640")
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="FMEA RISK ANALYSIS ENTRY", font=("Segoe UI", 13, "bold")).pack(pady=(15, 6))

        scroll = ctk.CTkScrollableFrame(dlg, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25, pady=5)

        ctk.CTkLabel(scroll, text="Process / Component *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_comp = ctk.CTkEntry(scroll, placeholder_text="e.g. Employee Database", height=30)
        ent_comp.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="Potential Failure Mode *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_mode = ctk.CTkEntry(scroll, placeholder_text="e.g. Unhandled duplicate key", height=30)
        ent_mode.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="Potential Effects *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_eff = ctk.CTkEntry(scroll, placeholder_text="e.g. Data corruption / application crash", height=30)
        ent_eff.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="Potential Causes *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_causes = ctk.CTkEntry(scroll, placeholder_text="e.g. Missing pre-check query", height=30)
        ent_causes.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="Current Controls *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_ctrl = ctk.CTkEntry(scroll, placeholder_text="e.g. SQLite UNIQUE constraint", height=30)
        ent_ctrl.pack(fill="x", pady=(1, 6))

        # RPN Sliders Frame
        scores_frame = ctk.CTkFrame(scroll, fg_color=("#f1f5f9", "#0f172a"), corner_radius=6)
        scores_frame.pack(fill="x", pady=8)

        lbl_rpn_preview = ctk.CTkLabel(scores_frame, text="Calculated RPN = 125", font=("Segoe UI", 11, "bold"), text_color="#ef4444")

        def _update_rpn(*args):
            s = int(slider_s.get())
            o = int(slider_o.get())
            d = int(slider_d.get())
            val = s * o * d
            lbl_s_val.configure(text=str(s))
            lbl_o_val.configure(text=str(o))
            lbl_d_val.configure(text=str(d))
            col = "#dc2626" if val >= 120 else "#d97706" if val >= 80 else "#10b981"
            lbl_rpn_preview.configure(text=f"Calculated RPN = {val} ({'HIGH RISK ≥ 120' if val>=120 else 'Moderate/Low'})", text_color=col)

        # Severity
        f_s = ctk.CTkFrame(scores_frame, fg_color="transparent")
        f_s.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(f_s, text="Severity (1-10):", width=120, anchor="w", font=("Segoe UI", 9, "bold")).pack(side="left")
        slider_s = ctk.CTkSlider(f_s, from_=1, to=10, number_of_steps=9, command=_update_rpn)
        slider_s.set(5)
        slider_s.pack(side="left", fill="x", expand=True, padx=4)
        lbl_s_val = ctk.CTkLabel(f_s, text="5", width=25, font=("Segoe UI", 9, "bold"))
        lbl_s_val.pack(side="left")

        # Occurrence
        f_o = ctk.CTkFrame(scores_frame, fg_color="transparent")
        f_o.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(f_o, text="Occurrence (1-10):", width=120, anchor="w", font=("Segoe UI", 9, "bold")).pack(side="left")
        slider_o = ctk.CTkSlider(f_o, from_=1, to=10, number_of_steps=9, command=_update_rpn)
        slider_o.set(5)
        slider_o.pack(side="left", fill="x", expand=True, padx=4)
        lbl_o_val = ctk.CTkLabel(f_o, text="5", width=25, font=("Segoe UI", 9, "bold"))
        lbl_o_val.pack(side="left")

        # Detection
        f_d = ctk.CTkFrame(scores_frame, fg_color="transparent")
        f_d.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(f_d, text="Detection (1-10):", width=120, anchor="w", font=("Segoe UI", 9, "bold")).pack(side="left")
        slider_d = ctk.CTkSlider(f_d, from_=1, to=10, number_of_steps=9, command=_update_rpn)
        slider_d.set(5)
        slider_d.pack(side="left", fill="x", expand=True, padx=4)
        lbl_d_val = ctk.CTkLabel(f_d, text="5", width=25, font=("Segoe UI", 9, "bold"))
        lbl_d_val.pack(side="left")

        lbl_rpn_preview.pack(pady=6)
        _update_rpn()

        ctk.CTkLabel(scroll, text="Recommended Mitigation *", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_mit = ctk.CTkEntry(scroll, placeholder_text="Action to reduce Severity, Occurrence, or Detection", height=30)
        ent_mit.pack(fill="x", pady=(1, 6))

        ctk.CTkLabel(scroll, text="Responsible Person", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_resp = ctk.CTkEntry(scroll, placeholder_text="e.g. QA Lead / Prabhat S.", height=30)
        ent_resp.pack(fill="x", pady=(1, 6))

        def _save():
            data = {
                "process_component": ent_comp.get().strip(),
                "potential_failure_mode": ent_mode.get().strip(),
                "potential_effects": ent_eff.get().strip(),
                "potential_causes": ent_causes.get().strip(),
                "current_controls": ent_ctrl.get().strip(),
                "severity": int(slider_s.get()),
                "occurrence": int(slider_o.get()),
                "detection": int(slider_d.get()),
                "recommended_action": ent_mit.get().strip(),
                "responsible_person": ent_resp.get().strip(),
                "status": "Open"
            }
            ok, msg, _ = self.tqm_service.create_fmea_record(data)
            if ok:
                messagebox.showinfo("Saved", msg)
                self.reload_data()
                dlg.destroy()
            else:
                messagebox.showerror("Error", msg)

        btn_box = ctk.CTkFrame(dlg, fg_color="transparent")
        btn_box.pack(fill="x", padx=25, pady=(8, 16))
        ctk.CTkButton(btn_box, text="Cancel", width=90, fg_color="#64748b", command=dlg.destroy).pack(side="left")
        ctk.CTkButton(btn_box, text="Save FMEA Item", width=140, fg_color="#dc2626", command=_save).pack(side="right")

    def _delete_fmea(self, item: FMEARecord) -> None:
        ans = messagebox.askyesno("Confirm Deletion", f"Permanently delete FMEA record '{item.item_code}'?")
        if ans and item.id:
            ok, msg = self.tqm_service.delete_fmea_record(item.id)
            if ok:
                self.reload_data()
            else:
                messagebox.showerror("Error", msg)
