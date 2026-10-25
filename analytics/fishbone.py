"""
Ishikawa / Fishbone Diagram (Cause and Effect) Generator.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Generates clear Fishbone root-cause visualizations organizing causes into:
1. People
2. Process
3. Software Code
4. Infrastructure
"""

import os
from typing import Dict, List, Any, Optional, Tuple
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class FishboneGenerator:
    """Renders Ishikawa cause-and-effect diagrams using Matplotlib."""

    @classmethod
    def generate_diagram(
        cls,
        problem_statement: str,
        causes_by_category: Dict[str, List[Dict[str, Any]]],
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Draws a customized Fishbone diagram:
        - Central horizontal spine terminating at the problem statement box
        - Upper ribs: People, Process
        - Lower ribs: Software Code, Infrastructure
        - Sub-branches for each recorded cause
        """
        fig, ax = plt.subplots(figsize=(11, 6.5), dpi=100)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")

        # Color palette
        bg_color = "#f8fafc"
        spine_color = "#0f172a"
        box_color = "#1e293b"
        upper_rib_color = "#2563eb"  # Blue
        lower_rib_color = "#059669"  # Emerald
        cause_color = "#334155"
        investigated_color = "#dc2626"  # Red marker for verified root causes

        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        # 1. Main Spine: from (10, 50) to (78, 50)
        ax.annotate(
            "", xy=(78, 50), xytext=(8, 50),
            arrowprops=dict(arrowstyle="->, head_width=0.6, head_length=0.9", color=spine_color, lw=3.0)
        )

        # 2. Problem Statement Box (Fish Head)
        head_box = patches.FancyBboxPatch(
            (79, 36), 19, 28,
            boxstyle="round,pad=0.8",
            fc=box_color, ec="#0f172a", lw=2
        )
        ax.add_patch(head_box)

        # Word wrap problem statement
        lines = []
        words = problem_statement.split()
        cur_line = []
        for w in words:
            cur_line.append(w)
            if len(" ".join(cur_line)) > 16:
                lines.append(" ".join(cur_line))
                cur_line = []
        if cur_line:
            lines.append(" ".join(cur_line))
        display_problem = "\n".join(lines[:4])

        ax.text(88.5, 50, f"PROBLEM:\n{display_problem}",
                color="#ffffff", fontsize=9, fontweight="bold", ha="center", va="center")

        # Rib definitions: (Category Name, rib_start_x, rib_start_y, rib_end_x, rib_end_y, is_upper)
        ribs = [
            ("People", 24, 85, 38, 50, True, upper_rib_color),
            ("Process", 54, 85, 66, 50, True, upper_rib_color),
            ("Software Code", 24, 15, 38, 50, False, lower_rib_color),
            ("Infrastructure", 54, 15, 66, 50, False, lower_rib_color)
        ]

        for cat_name, sx, sy, ex, ey, is_upper, color in ribs:
            # Draw primary rib line
            ax.plot([sx, ex], [sy, ey], color=color, lw=2.2)

            # Category Label Box
            label_y = sy + 3 if is_upper else sy - 4
            ax.text(
                sx, label_y, cat_name.upper(),
                color=color, fontsize=10, fontweight="bold", ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec=color, lw=1.5)
            )

            # Render cause sub-branches
            cat_causes = causes_by_category.get(cat_name, [])
            count = min(len(cat_causes), 4)

            for i in range(count):
                cause_item = cat_causes[i]
                cause_text = cause_item.get("cause_text", "")
                is_inv = cause_item.get("is_investigated", False)

                # Interpolate anchor position along rib
                t = 0.25 + (i * 0.22)
                bx = sx + t * (ex - sx)
                by = sy + t * (ey - sy)

                # Branch extends horizontally to the left
                branch_len = 12
                branch_end_x = bx - branch_len
                ax.plot([bx, branch_end_x], [by, by], color="#94a3b8", lw=1.2, linestyle="-")

                # Marker indicating verified/investigated root cause
                marker_color = investigated_color if is_inv else "#64748b"
                ax.plot(bx, by, marker="o", color=marker_color, markersize=4)

                # Truncate text if needed
                short_text = cause_text if len(cause_text) <= 24 else cause_text[:21] + "..."
                tag = " [VERIFIED]" if is_inv else ""
                ax.text(
                    branch_end_x - 0.5, by, f"{short_text}{tag}",
                    color="#0f172a", fontsize=7.5, ha="right", va="center",
                    fontweight="bold" if is_inv else "normal"
                )

        # Diagram Title & Subtitle
        plt.title(
            "Ishikawa (Cause & Effect) Root-Cause Analysis Diagram\nTotal Quality Management - BBAT104",
            fontsize=13, fontweight="bold", pad=20, color="#0f172a"
        )

        # Legend at bottom
        ax.plot([30], [5], marker="o", color=investigated_color, markersize=6)
        ax.text(32, 5, "Verified Root Cause", fontsize=8, color="#0f172a", va="center")
        ax.plot([55], [5], marker="o", color="#64748b", markersize=6)
        ax.text(57, 5, "Suspected Root Cause", fontsize=8, color="#0f172a", va="center")

        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            fig.savefig(save_path, bbox_inches="tight", dpi=150)

        return fig
