"""
Stat Card Component for Dashboard Key Performance Indicators.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability
"""

import customtkinter as ctk
from typing import Optional


class StatCard(ctk.CTkFrame):
    """Reusable metric KPI card with accent color highlights."""

    def __init__(
        self,
        master,
        title: str,
        value: str,
        subtitle: Optional[str] = None,
        accent_color: str = "#3b82f6",
        **kwargs
    ):
        super().__init__(master, corner_radius=10, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"), **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # Title Label
        self.lbl_title = ctk.CTkLabel(
            self,
            text=title.upper(),
            font=("Segoe UI", 10, "bold"),
            text_color=("#64748b", "#94a3b8"),
            anchor="w"
        )
        self.lbl_title.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 2))

        # Main Value Display
        self.lbl_value = ctk.CTkLabel(
            self,
            text=str(value),
            font=("Segoe UI", 26, "bold"),
            text_color=accent_color,
            anchor="w"
        )
        self.lbl_value.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 2))

        # Optional Subtitle
        if subtitle:
            self.lbl_sub = ctk.CTkLabel(
                self,
                text=subtitle,
                font=("Segoe UI", 9),
                text_color=("#94a3b8", "#64748b"),
                anchor="w"
            )
            self.lbl_sub.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 14))
        else:
            self.grid_rowconfigure(1, pad=10)

    def update_value(self, new_value: str, new_subtitle: Optional[str] = None) -> None:
        """Dynamically updates the displayed metric."""
        self.lbl_value.configure(text=str(new_value))
        if new_subtitle and hasattr(self, "lbl_sub"):
            self.lbl_sub.configure(text=new_subtitle)
