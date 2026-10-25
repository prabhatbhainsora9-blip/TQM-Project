"""
Activity Logs Viewer View (Feature 4: Activity Logs).
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Provides a live Log Viewer screen with search, level filtering (DEBUG, INFO, WARNING, ERROR),
timestamp filtering, and log export capability.
"""

import os
import customtkinter as ctk
from tkinter import messagebox
from typing import List, Dict

from services.logging_service import read_log_entries, get_logger


class LogsView(ctk.CTkFrame):
    """Real-time log viewer interface for monitoring application operational events."""

    def __init__(self, master, log_file_path: str = "logs/application.log", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.log_file_path = log_file_path
        self.logs_cache: List[Dict[str, str]] = []

        self._build_toolbar()
        self._build_table_header()
        self._build_table_body()

        self.reload_logs()

    def _build_toolbar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        bar.pack(fill="x", padx=10, pady=(10, 6))

        # Filter by level
        ctk.CTkLabel(bar, text="Level:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(12, 4), pady=8)
        self.combo_level = ctk.CTkComboBox(bar, values=["ALL", "INFO", "WARNING", "ERROR", "DEBUG"], width=110, height=32, command=lambda v: self.reload_logs())
        self.combo_level.pack(side="left", padx=4, pady=8)
        self.combo_level.set("ALL")

        # Search Query
        self.entry_search = ctk.CTkEntry(bar, placeholder_text="Filter log message...", width=220, height=32)
        self.entry_search.pack(side="left", padx=6, pady=8)
        self.entry_search.bind("<Return>", lambda e: self.reload_logs())

        btn_search = ctk.CTkButton(bar, text="Filter", width=70, height=32, command=self.reload_logs)
        btn_search.pack(side="left", padx=2, pady=8)

        # Right Action Buttons
        btn_refresh = ctk.CTkButton(bar, text="Refresh Logs", width=110, height=32, fg_color="#3b82f6", command=self.reload_logs)
        btn_refresh.pack(side="right", padx=(4, 12), pady=8)

        btn_export = ctk.CTkButton(bar, text="Export Log Copy", width=130, height=32, fg_color="#475569", command=self._export_log_copy)
        btn_export.pack(side="right", padx=4, pady=8)

    def _build_table_header(self) -> None:
        head = ctk.CTkFrame(self, height=32, fg_color=("#e2e8f0", "#0f172a"), corner_radius=6)
        head.pack(fill="x", padx=10, pady=(2, 2))

        cols = [
            ("Timestamp", 150),
            ("Level", 80),
            ("Module", 120),
            ("Operational Event / Message", 580)
        ]
        for name, width in cols:
            ctk.CTkLabel(head, text=name, width=width, font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", padx=4)

    def _build_table_body(self) -> None:
        self.table_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.table_scroll.pack(fill="both", expand=True, padx=10, pady=2)

    def reload_logs(self) -> None:
        """Parses newest log lines from the active RotatingFileHandler output."""
        lvl = self.combo_level.get()
        query = self.entry_search.get().strip()

        self.logs_cache = read_log_entries(
            log_file_path=self.log_file_path,
            max_lines=300,
            level_filter=lvl if lvl != "ALL" else None,
            search_text=query if query else None
        )
        self._render_rows()

    def _render_rows(self) -> None:
        for child in self.table_scroll.winfo_children():
            child.destroy()

        if not self.logs_cache:
            ctk.CTkLabel(self.table_scroll, text="No log entries found matching criteria.", font=("Segoe UI", 11), text_color="#94a3b8").pack(pady=40)
            return

        for i, item in enumerate(self.logs_cache):
            bg = ("#ffffff", "#1e293b") if i % 2 == 0 else ("#f8fafc", "#0f172a")
            row = ctk.CTkFrame(self.table_scroll, fg_color=bg, corner_radius=4, height=30)
            row.pack(fill="x", pady=1)

            ctk.CTkLabel(row, text=item["timestamp"], width=150, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=4)

            lvl = item["level"].upper()
            col = "#ef4444" if lvl in ["ERROR", "CRITICAL"] else "#f59e0b" if lvl == "WARNING" else "#3b82f6"
            ctk.CTkLabel(row, text=lvl, width=80, font=("Segoe UI", 9, "bold"), text_color=col, anchor="w").pack(side="left", padx=4)

            ctk.CTkLabel(row, text=item["module"], width=120, font=("Segoe UI", 9, "bold"), text_color=("#475569", "#94a3b8"), anchor="w").pack(side="left", padx=4)

            msg = item["message"]
            msg_short = msg[:80] + "..." if len(msg) > 80 else msg
            ctk.CTkLabel(row, text=msg_short, width=580, font=("Segoe UI", 9), anchor="w").pack(side="left", padx=4)

    def _export_log_copy(self) -> None:
        """Saves a text copy of the active log file to reports/."""
        if not os.path.exists(self.log_file_path):
            messagebox.showwarning("Warning", "Log file does not exist yet.")
            return

        out_path = os.path.abspath("reports/application_log_export.txt")
        try:
            with open(self.log_file_path, "r", encoding="utf-8", errors="replace") as fin:
                data = fin.read()
            with open(out_path, "w", encoding="utf-8") as fout:
                fout.write(data)
            messagebox.showinfo("Export Complete", f"Log file exported to:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
