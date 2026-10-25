"""
Help and Academic Viva Reference View.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Presents academic project details, TQM principles, maintainability architectural explanations,
and viva defense reference notes.
"""

import customtkinter as ctk


class HelpView(ctk.CTkScrollableFrame):
    """Academic documentation and student viva defense handbook."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self._build_student_card()
        self._build_q11_card()
        self._build_tqm_principles_card()
        self._build_viva_tips_card()

    def _build_student_card(self) -> None:
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.pack(fill="x", padx=10, pady=(10, 6))

        ctk.CTkLabel(card, text="ACADEMIC CREDENTIALS & PROJECT METADATA", font=("Segoe UI", 12, "bold"), text_color="#3b82f6").pack(anchor="w", padx=16, pady=(14, 8))

        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=16, pady=(0, 14))
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        fields = [
            ("Student Name", "Prabhat Singh Bhainsora"),
            ("Roll / Reg. Number", "2410302046"),
            ("Branch & Section", "CSE — Section B"),
            ("Course Code", "BBAT104"),
            ("Course Name", "Fundamentals of TQM"),
            ("Academic Session", "2026–2027"),
            ("Baseline Software", "Employee Management System"),
            ("Assigned Quality Goal", "Q11 — Improve Maintainability"),
            ("GitHub Target Repo", "BBAT104_TQM_2410302046")
        ]

        for i, (k, v) in enumerate(fields):
            r = i // 3
            c = i % 3
            f_box = ctk.CTkFrame(grid, fg_color=("#f1f5f9", "#0f172a"), corner_radius=6)
            f_box.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
            ctk.CTkLabel(f_box, text=k.upper(), font=("Segoe UI", 8, "bold"), text_color=("#64748b", "#94a3b8")).pack(anchor="w", padx=8, pady=(6, 1))
            ctk.CTkLabel(f_box, text=v, font=("Segoe UI", 10, "bold"), text_color=("#0f172a", "#f8fafc")).pack(anchor="w", padx=8, pady=(0, 6))

    def _build_q11_card(self) -> None:
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.pack(fill="x", padx=10, pady=6)

        ctk.CTkLabel(card, text="THE FIVE MANDATORY Q11 MAINTAINABILITY FEATURES", font=("Segoe UI", 12, "bold"), text_color="#10b981").pack(anchor="w", padx=16, pady=(14, 8))

        features = [
            ("Feature 1: Modular Structure", "Application logic is strictly decoupled across independent packages: database, models, services, analytics, and ui. Single Responsibility Principle prevents monolithic code rot."),
            ("Feature 2: Configuration Files", "External config.json manages app parameters (paths, themes, scaling, log limits). Safely recovers with default fallbacks if corrupted."),
            ("Feature 3: System Settings", "Live interactive Settings screen dynamically modifies appearance mode, font scaling, pagination limits, and backup rules, persisting changes to disk."),
            ("Feature 4: Activity Logs", "RotatingFileHandler records all startup events, CRUD operations, database transactions, and Poka-Yoke validation errors with live UI log filtering."),
            ("Feature 5: Code Comments & Docs", "Complete architectural SRS, FMEA matrices, SIPOC maps, CTQ trees, and comprehensive docstrings explaining RPN math and SQC Pareto calculations.")
        ]

        for name, desc in features:
            box = ctk.CTkFrame(card, fg_color=("#f8fafc", "#0f172a"), corner_radius=6)
            box.pack(fill="x", padx=16, pady=3)
            ctk.CTkLabel(box, text=name, font=("Segoe UI", 10, "bold"), text_color="#10b981").pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(box, text=desc, font=("Segoe UI", 9), text_color=("#475569", "#cbd5e1"), wraplength=920, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

        ctk.CTkLabel(card, text="", height=6).pack()

    def _build_tqm_principles_card(self) -> None:
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.pack(fill="x", padx=10, pady=6)

        ctk.CTkLabel(card, text="TQM PHILOSOPHICAL & STATISTICAL PILLARS APPLIED", font=("Segoe UI", 12, "bold"), text_color="#8b5cf6").pack(anchor="w", padx=16, pady=(14, 8))

        pillars = [
            ("Customer Focus", "Operator-friendly interface, meaningful error feedback, accessible keyboard navigation, and responsive scaling."),
            ("Continuous Improvement (Kaizen)", "PDCA cycle engine tracking Plan -> Do -> Check -> Act with before-and-after empirical verification metrics."),
            ("Process-Centric Approach (SIPOC)", "Maps complete employee lifecycle across Suppliers, Inputs, Process steps, Outputs, and Customers."),
            ("Fact-Based Decision Making", "Real-time Pareto 80/20 analysis and checksheet aggregation derived from active SQLite defect occurrences."),
            ("Error Prevention (Poka-Yoke)", "Centralized ValidationService preventing duplicate codes/emails, invalid formats, and data corruptions prior to DB write.")
        ]

        for name, desc in pillars:
            box = ctk.CTkFrame(card, fg_color=("#f8fafc", "#0f172a"), corner_radius=6)
            box.pack(fill="x", padx=16, pady=3)
            ctk.CTkLabel(box, text=name, font=("Segoe UI", 10, "bold"), text_color="#8b5cf6").pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(box, text=desc, font=("Segoe UI", 9), text_color=("#475569", "#cbd5e1"), wraplength=920, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

        ctk.CTkLabel(card, text="", height=6).pack()

    def _build_viva_tips_card(self) -> None:
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.pack(fill="x", padx=10, pady=(6, 15))

        ctk.CTkLabel(card, text="KEY VIVA QUESTIONS QUICK REFERENCE", font=("Segoe UI", 12, "bold"), text_color="#f59e0b").pack(anchor="w", padx=16, pady=(14, 8))

        tips = [
            ("Q: How does RPN work in your FMEA module?", "A: RPN = Severity (1-10) × Occurrence (1-10) × Detection (1-10). The scale ranges from 1 to 1000. Any item with RPN ≥ 120 triggers an automated high-risk alert requiring corrective action."),
            ("Q: What is the 80/20 rule in your Pareto chart?", "A: 80% of software defects typically originate from roughly 20% of root cause categories ('Vital Few'). Our chart dynamically orders frequencies descending and overlays cumulative percentages."),
            ("Q: How does Q11 (Maintainability) improve software life?", "A: By decoupling UI, Business Logic, and Database layers, software can be modified, tested, and scaled without unintended side effects or monolithic rewrites.")
        ]

        for q, a in tips:
            box = ctk.CTkFrame(card, fg_color=("#f8fafc", "#0f172a"), corner_radius=6)
            box.pack(fill="x", padx=16, pady=3)
            ctk.CTkLabel(box, text=q, font=("Segoe UI", 9, "bold"), text_color="#f59e0b").pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(box, text=a, font=("Segoe UI", 9), text_color=("#475569", "#cbd5e1"), wraplength=920, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

        ctk.CTkLabel(card, text="", height=6).pack()
