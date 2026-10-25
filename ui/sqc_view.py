"""
SQC (Statistical Quality Control) Interactive Charts View.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Integrates embedded Matplotlib visualizations using FigureCanvasTkAgg for:
1. Pareto Analysis (80/20 Rule & Cumulative Percentages)
2. Ishikawa / Fishbone Cause-and-Effect Diagram
3. SIPOC Process Flowchart
4. CTQ Quality Tree
"""

import os
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from services.tqm_service import TQMService
from analytics.pareto import ParetoAnalyzer
from analytics.fishbone import FishboneGenerator
from analytics.sipoc import SIPOCMapper
from analytics.ctq import CTQTree


class SQCChartsView(ctk.CTkFrame):
    """Hosts embedded interactive SQC charts with tab switching and PNG export."""

    def __init__(self, master, tqm_service: TQMService, reports_dir: str = "reports", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.tqm_service = tqm_service
        self.reports_dir = os.path.abspath(reports_dir)
        os.makedirs(self.reports_dir, exist_ok=True)

        self.current_canvas: Optional[FigureCanvasTkAgg] = None
        self.active_tab = "Pareto"

        self._build_top_controls()
        self._build_chart_container()

        self.show_pareto_chart()

    def _build_top_controls(self) -> None:
        """Navigation buttons to switch between the 4 TQM SQC visualizations."""
        bar = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        bar.pack(fill="x", padx=10, pady=(10, 6))

        ctk.CTkLabel(bar, text="SQC Analysis Tool:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(12, 6), pady=8)

        self.btn_pareto = ctk.CTkButton(bar, text="Pareto Chart (80/20)", width=150, height=32, command=self.show_pareto_chart)
        self.btn_pareto.pack(side="left", padx=4, pady=8)

        self.btn_fishbone = ctk.CTkButton(bar, text="Fishbone Diagram", width=140, height=32, fg_color="#475569", command=self.show_fishbone_chart)
        self.btn_fishbone.pack(side="left", padx=4, pady=8)

        self.btn_sipoc = ctk.CTkButton(bar, text="SIPOC Process Map", width=140, height=32, fg_color="#475569", command=self.show_sipoc_chart)
        self.btn_sipoc.pack(side="left", padx=4, pady=8)

        self.btn_ctq = ctk.CTkButton(bar, text="CTQ Quality Tree", width=130, height=32, fg_color="#475569", command=self.show_ctq_chart)
        self.btn_ctq.pack(side="left", padx=4, pady=8)

        self.btn_export = ctk.CTkButton(bar, text="Export Chart (PNG)", width=140, height=32, fg_color="#059669", hover_color="#047857", command=self._export_current_chart)
        self.btn_export.pack(side="right", padx=12, pady=8)

    def _build_chart_container(self) -> None:
        """Container frame where Matplotlib canvas is mounted."""
        self.chart_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _clear_canvas(self) -> None:
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        plt.close("all")

    def _highlight_tab(self, active_btn) -> None:
        for btn in [self.btn_pareto, self.btn_fishbone, self.btn_sipoc, self.btn_ctq]:
            if btn == active_btn:
                btn.configure(fg_color="#2563eb")
            else:
                btn.configure(fg_color="#475569")

    def show_pareto_chart(self) -> None:
        """Renders Pareto 80/20 chart from current defect database."""
        self.active_tab = "Pareto"
        self._highlight_tab(self.btn_pareto)
        self._clear_canvas()

        cat_counts = self.tqm_service.get_category_defect_counts()
        fig, summary = ParetoAnalyzer.generate_chart(cat_counts, title="Pareto Analysis: Defect Frequencies & 80% Vital Few Benchmark")

        self.current_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self.active_fig = fig

    def show_fishbone_chart(self) -> None:
        """Renders Ishikawa Fishbone diagram with recorded causes."""
        self.active_tab = "Fishbone"
        self._highlight_tab(self.btn_fishbone)
        self._clear_canvas()

        causes = self.tqm_service.get_fishbone_causes()
        fig = FishboneGenerator.generate_diagram(
            problem_statement="High Employee Registration Data Errors",
            causes_by_category=causes
        )

        self.current_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self.active_fig = fig

    def show_sipoc_chart(self) -> None:
        """Renders 5-column SIPOC process flowchart."""
        self.active_tab = "SIPOC"
        self._highlight_tab(self.btn_sipoc)
        self._clear_canvas()

        fig = SIPOCMapper.generate_diagram()
        self.current_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self.active_fig = fig

    def show_ctq_chart(self) -> None:
        """Renders Critical to Quality tree."""
        self.active_tab = "CTQ"
        self._highlight_tab(self.btn_ctq)
        self._clear_canvas()

        fig = CTQTree.generate_diagram()
        self.current_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self.active_fig = fig

    def _export_current_chart(self) -> None:
        """Saves active Matplotlib figure as high-resolution PNG."""
        if not hasattr(self, "active_fig") or self.active_fig is None:
            messagebox.showwarning("Warning", "No active chart to export.")
            return

        fname = f"sqc_{self.active_tab.lower()}_chart.png"
        out_path = os.path.join(self.reports_dir, fname)
        try:
            self.active_fig.savefig(out_path, bbox_inches="tight", dpi=200)
            messagebox.showinfo("Export Success", f"Chart successfully saved to:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not save chart: {e}")
