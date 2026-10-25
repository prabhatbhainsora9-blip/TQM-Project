"""
Pareto Analysis Module (80/20 Rule) for Statistical Quality Control.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Generates Pareto charts from defect frequency data, calculating accurate cumulative
percentages to identify the 'Vital Few' quality issues versus the 'Useful Many'.
"""

import os
from typing import Dict, Tuple, Any, Optional
import matplotlib
# Use Agg backend for non-GUI headless generation or embedded Canvas rendering
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


class ParetoAnalyzer:
    """Calculates Pareto cumulative percentages and creates SQC dual-axis charts."""

    @staticmethod
    def calculate_pareto_data(category_counts: Dict[str, int]) -> pd.DataFrame:
        """
        Takes raw category count dictionary and produces a DataFrame ordered by frequency
        with cumulative sums and cumulative percentages.
        """
        if not category_counts or sum(category_counts.values()) == 0:
            return pd.DataFrame(columns=["Category", "Count", "CumulativeSum", "CumulativePercentage"])

        df = pd.DataFrame(list(category_counts.items()), columns=["Category", "Count"])
        # Filter zero counts and sort descending
        df = df[df["Count"] > 0].sort_values(by="Count", ascending=False).reset_index(drop=True)
        total = df["Count"].sum()
        df["CumulativeSum"] = df["Count"].cumsum()
        df["CumulativePercentage"] = (df["CumulativeSum"] / total) * 100.0
        return df

    @classmethod
    def generate_chart(
        cls,
        category_counts: Dict[str, int],
        title: str = "TQM Defect Category Pareto Analysis",
        save_path: Optional[str] = None
    ) -> Tuple[plt.Figure, Dict[str, Any]]:
        """
        Builds a dual-axis Pareto chart:
        - Left Y-Axis: Frequency of defect occurrences (bars)
        - Right Y-Axis: Cumulative percentage curve (0-100%)
        - 80% Cutoff line indicating the Vital Few
        """
        df = cls.calculate_pareto_data(category_counts)

        fig, ax1 = plt.subplots(figsize=(9, 5), dpi=100)
        fig.patch.set_facecolor("#1e293b" if plt.rcParams.get("figure.facecolor") == "#1e293b" else "#ffffff")

        summary: Dict[str, Any] = {
            "total_defects": 0,
            "vital_few": [],
            "useful_many": [],
            "dataframe": df
        }

        if df.empty:
            ax1.text(0.5, 0.5, "Insufficient Defect Data for Pareto Analysis\nPlease record defects in the Defect Log.",
                     ha="center", va="center", fontsize=12, color="#64748b")
            ax1.set_axis_off()
            if save_path:
                os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
                fig.savefig(save_path, bbox_inches="tight")
            return fig, summary

        total_defects = int(df["Count"].sum())
        summary["total_defects"] = total_defects

        # Classify Vital Few (categories contributing up to 80% of defects)
        for _, row in df.iterrows():
            if row["CumulativePercentage"] <= 85.0 or len(summary["vital_few"]) == 0:
                summary["vital_few"].append(row["Category"])
            else:
                summary["useful_many"].append(row["Category"])

        # Plot Bars (Left Axis)
        categories = df["Category"].tolist()
        counts = df["Count"].tolist()
        cum_pct = df["CumulativePercentage"].tolist()

        color_bars = "#3b82f6"  # Blue
        color_line = "#ef4444"  # Red
        color_cutoff = "#f59e0b"  # Amber

        bars = ax1.bar(categories, counts, color=color_bars, width=0.55, edgecolor="#1e40af", alpha=0.9, label="Defect Count")
        ax1.set_ylabel("Defect Frequency (Count)", color="#1e293b", fontsize=11, fontweight="bold")
        ax1.tick_params(axis="y", labelcolor="#1e293b")
        ax1.set_xticks(range(len(categories)))
        ax1.set_xticklabels(categories, rotation=25, ha="right", fontsize=9)
        ax1.grid(axis="y", linestyle="--", alpha=0.4)

        # Bar value labels
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f"{int(height)}",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3), textcoords="offset points",
                         ha="center", va="bottom", fontsize=9, fontweight="bold")

        # Plot Cumulative % Line (Right Axis)
        ax2 = ax1.twinx()
        ax2.plot(categories, cum_pct, color=color_line, marker="o", linewidth=2.2, markersize=6, label="Cumulative %")
        ax2.set_ylabel("Cumulative Percentage (%)", color=color_line, fontsize=11, fontweight="bold")
        ax2.tick_params(axis="y", labelcolor=color_line)
        ax2.set_ylim(0, 105)

        # 80% Vital Few Benchmark Line
        ax2.axhline(80, color=color_cutoff, linestyle="--", linewidth=1.8, label="80% Vital Few Benchmark")
        ax2.text(len(categories) - 0.5, 81.5, "80% Threshold", color=color_cutoff, fontweight="bold", fontsize=9, ha="right")

        # Cumulative % labels
        for i, txt in enumerate(cum_pct):
            ax2.annotate(f"{txt:.1f}%", (categories[i], cum_pct[i] + 2),
                         fontsize=8, ha="center", color=color_line, fontweight="bold")

        plt.title(f"{title}\nTotal Recorded Defects: {total_defects}", fontsize=13, fontweight="bold", pad=15)
        fig.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            fig.savefig(save_path, bbox_inches="tight", dpi=150)

        return fig, summary
