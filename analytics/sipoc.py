"""
SIPOC Process Mapping Module for Employee Lifecycle Management.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Models Suppliers, Inputs, Process, Outputs, Customers for the entire
employee data lifecycle: Registration -> Validation -> Storage -> Modification -> Retrieval -> Reporting.
"""

import os
from typing import List, Dict, Any, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

SIPOC_DATA = [
    {
        "category": "Suppliers",
        "color": "#3b82f6",
        "items": [
            "HR Onboarding Team",
            "Department Heads",
            "Recruitment Portals",
            "System Administrators",
            "Employee Self-Service"
        ]
    },
    {
        "category": "Inputs",
        "color": "#6366f1",
        "items": [
            "Employee Code & Name",
            "Department & Role",
            "Contact & Email",
            "Date of Joining",
            "System Settings & Config"
        ]
    },
    {
        "category": "Process",
        "color": "#8b5cf6",
        "items": [
            "1. Data Entry & Submission",
            "2. Poka-Yoke Input Validation",
            "3. SQLite ACID Persistence",
            "4. Search & Multi-filter",
            "5. Quality Audit & Reporting"
        ]
    },
    {
        "category": "Outputs",
        "color": "#ec4899",
        "items": [
            "Verified Employee Records",
            "Audit Activity Logs",
            "TQM Defect Checksheets",
            "Pareto / SQC Charts",
            "PDF/Excel Executive Reports"
        ]
    },
    {
        "category": "Customers",
        "color": "#10b981",
        "items": [
            "HR Management",
            "Operations & Payroll",
            "Quality Assurance Team",
            "Academic Evaluators",
            "Senior Executives"
        ]
    }
]


class SIPOCMapper:
    """Manages SIPOC structured data and renders professional process diagrams."""

    @staticmethod
    def get_sipoc_data() -> List[Dict[str, Any]]:
        """Returns the structured SIPOC dataset."""
        return SIPOC_DATA

    @classmethod
    def generate_diagram(cls, save_path: Optional[str] = None) -> plt.Figure:
        """Renders an aesthetic 5-column SIPOC matrix flowchart."""
        fig, ax = plt.subplots(figsize=(11, 5.5), dpi=100)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")

        bg_color = "#f8fafc"
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        cols = cls.get_sipoc_data()
        col_width = 17.5
        spacing = 2.0
        start_x = 2.0

        for i, col in enumerate(cols):
            cx = start_x + (i * (col_width + spacing))

            # Column Header Box
            header_box = patches.FancyBboxPatch(
                (cx, 82), col_width, 12,
                boxstyle="round,pad=0.5",
                fc=col["color"], ec="#0f172a", lw=1.2
            )
            ax.add_patch(header_box)
            letter = col["category"][0]
            ax.text(
                cx + col_width / 2, 88,
                f"[{letter}] {col['category'].upper()}",
                color="#ffffff", fontsize=9.5, fontweight="bold", ha="center", va="center"
            )

            # Content Items Card
            content_box = patches.FancyBboxPatch(
                (cx, 10), col_width, 68,
                boxstyle="round,pad=0.5",
                fc="#ffffff", ec="#cbd5e1", lw=1.2
            )
            ax.add_patch(content_box)

            # List Items inside card
            item_y = 70
            for itm in col["items"]:
                ax.text(
                    cx + 1.2, item_y, f"• {itm}",
                    color="#1e293b", fontsize=7.8, fontweight="medium", ha="left", va="center"
                )
                item_y -= 13

            # Draw process flow arrows between columns
            if i < len(cols) - 1:
                arrow_x = cx + col_width + 0.2
                ax.annotate(
                    "", xy=(arrow_x + spacing - 0.4, 45), xytext=(arrow_x, 45),
                    arrowprops=dict(arrowstyle="->, head_width=0.4, head_length=0.6", color="#64748b", lw=2.0)
                )

        plt.title(
            "SIPOC High-Level Process Map: Employee Record Management Lifecycle\nCourse: BBAT104 (Fundamentals of TQM) | Student: Prabhat Singh Bhainsora",
            fontsize=11.5, fontweight="bold", pad=15, color="#0f172a"
        )

        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            fig.savefig(save_path, bbox_inches="tight", dpi=150)

        return fig
