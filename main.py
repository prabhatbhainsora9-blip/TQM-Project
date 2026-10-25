"""
==============================================================================
EMPLOYEE MANAGEMENT SYSTEM WITH MAINTAINABILITY ENHANCEMENT (Q11)
AND TOTAL QUALITY MANAGEMENT (TQM) STATISTICAL ANALYSIS
==============================================================================
Student Name: Prabhat Singh Bhainsora
Roll Number:  2410302046
Branch / Sec: CSE - B
Course Code:  BBAT104
Course Name:  Fundamentals of Total Quality Management (TQM)
Session:      2026-27
Assigned Goal:Q11 — Improve Maintainability
==============================================================================
Entry point for running the desktop application.
Usage:
    python main.py
==============================================================================
"""

import sys
import os

# Anchor sys.path to this directory so imports resolve cleanly across Windows environments
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def main():
    """Main execution entry point."""
    if "--version" in sys.argv:
        print("Employee Management System (TQM Edition) - Version 1.0.0")
        print("Author: Prabhat Singh Bhainsora (2410302046)")
        return

    try:
        from app.application import Application
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] Application startup failure: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
