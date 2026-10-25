"""
Critical to Quality (CTQ) Tree Module.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Deconstructs broad customer and operational needs into measurable quality drivers
and specific Critical to Quality (CTQ) metrics with project-defined targets.
"""

import os
from typing import List, Dict, Any, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

CTQ_ITEMS = [
    {
        "need": "Reliable Employee Record Management",
        "driver": "Data Integrity & Accuracy",
        "ctq": "Validation Accuracy Rate",
        "target": ">= 99.5% valid inputs without corrupting records",
        "eval_method": "Automated unit tests with 100+ edge-case inputs (test_employees.py)"
    },
    {
        "need": "Reliable Employee Record Management",
        "driver": "Entity Uniqueness",
        "ctq": "Zero Duplicate Records",
        "target": "100% duplicate rejection for code and email",
        "eval_method": "SQLite UNIQUE constraint verification and Poka-Yoke error handling"
    },
    {
        "need": "High Software Maintainability (Q11)",
        "driver": "Modular Architecture",
        "ctq": "Separation of Concerns",
        "target": "100% decoupling: DB, UI, Models, Services, and Analytics",
        "eval_method": "Code inspection and circular dependency auditing"
    },
    {
        "need": "High Software Maintainability (Q11)",
        "driver": "External Configuration",
        "ctq": "Zero Code Change for Config",
        "target": "100% dynamic settings loading from config.json with fallback",
        "eval_method": "test_configuration.py verifying safe defaults upon file corruption"
    },
    {
        "need": "Fast and Responsive Desktop UI",
        "driver": "Search Performance",
        "ctq": "Query Latency",
        "target": "< 50 ms query time for up to 5,000 records",
        "eval_method": "Benchmark execution with SQLite indices on employee_code and email"
    },
    {
        "need": "Disaster Resilience & Zero Data Loss",
        "driver": "Persistence & Recovery",
        "ctq": "Recovery Time Objective (RTO)",
        "target": "< 10 seconds database restoration with zero corruption",
        "eval_method": "SQLite integrity check and BackupService snapshot restore test"
    }
]


class CTQTree:
    """Manages Critical to Quality tree data and renders graphical hierarchy."""

    @staticmethod
    def get_ctq_data() -> List[Dict[str, Any]]:
        """Returns the structured CTQ tree specifications."""
        return CTQ_ITEMS

    @classmethod
    def generate_diagram(cls, save_path: Optional[str] = None) -> plt.Figure:
        """Renders a tree diagram mapping Need -> Drivers -> Measurable CTQs."""
        fig, ax = plt.subplots(figsize=(11, 6.5), dpi=100)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")

        bg_color = "#f8fafc"
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        # 1. Level 1: Customer Need (Root Box)
        root_box = patches.FancyBboxPatch(
            (2, 38), 22, 24,
            boxstyle="round,pad=0.6",
            fc="#1e293b", ec="#0f172a", lw=1.5
        )
        ax.add_patch(root_box)
        ax.text(13, 50, "CUSTOMER NEED:\n\nMaintainable &\nAccurate Employee\nManagement System",
                color="#ffffff", fontsize=9.5, fontweight="bold", ha="center", va="center")

        # 2. Level 2: Quality Drivers
        drivers = [
            ("Data Integrity\n& Accuracy", 82, "#2563eb"),
            ("Entity\nUniqueness", 66, "#2563eb"),
            ("Modular Code\nStructure (Q11)", 50, "#0891b2"),
            ("External Config\n& Logs (Q11)", 34, "#0891b2"),
            ("Disaster Resilience\n& Recovery", 18, "#059669")
        ]

        # 3. Level 3: Measurable CTQs
        ctqs = [
            ("Validation Accuracy Rate (>=99.5%)", 82),
            ("Zero Duplicate Records (100% rejection)", 66),
            ("Separation of Concerns (100% decoupled)", 50),
            ("Zero Code Change for Config (JSON + Fallback)", 34),
            ("Recovery Time Objective (< 10s restore)", 18)
        ]

        for i, (d_name, d_y, d_color) in enumerate(drivers):
            # Connector from Root to Driver
            ax.plot([24, 34], [50, d_y], color="#94a3b8", lw=1.5, linestyle="-")

            # Driver Box
            dbox = patches.FancyBboxPatch(
                (34, d_y - 5), 22, 10,
                boxstyle="round,pad=0.4",
                fc=d_color, ec="#0f172a", lw=1.0
            )
            ax.add_patch(dbox)
            ax.text(45, d_y, d_name, color="#ffffff", fontsize=8, fontweight="bold", ha="center", va="center")

            # Connector from Driver to CTQ
            ax.plot([56, 64], [d_y, d_y], color="#94a3b8", lw=1.5, linestyle="-")

            # CTQ Metric Box
            ctq_text, ctq_y = ctqs[i]
            cbox = patches.FancyBboxPatch(
                (64, ctq_y - 5), 34, 10,
                boxstyle="round,pad=0.4",
                fc="#ffffff", ec=d_color, lw=1.3
            )
            ax.add_patch(cbox)
            ax.text(81, ctq_y, ctq_text, color="#0f172a", fontsize=7.8, fontweight="bold", ha="center", va="center")

        plt.title(
            "CTQ Tree: Voice of Customer to Measurable Quality Metrics\nAssigned Goal: Q11 - Improve Maintainability | BBAT104",
            fontsize=12, fontweight="bold", pad=15, color="#0f172a"
        )

        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            fig.savefig(save_path, bbox_inches="tight", dpi=150)

        return fig
