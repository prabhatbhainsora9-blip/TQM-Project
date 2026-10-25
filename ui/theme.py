"""
Theme and Styling System for Desktop GUI.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Defines standardized color palettes, typography tokens, and appearance modes.
"""

from typing import Dict, Any

THEME_COLORS: Dict[str, Dict[str, str]] = {
    "Dark": {
        "bg_primary": "#0f172a",       # Slate 900
        "bg_secondary": "#1e293b",     # Slate 800
        "bg_card": "#1e293b",          # Slate 800
        "bg_input": "#334155",         # Slate 700
        "sidebar_bg": "#020617",       # Slate 950
        "text_primary": "#f8fafc",     # Slate 50
        "text_secondary": "#94a3b8",   # Slate 400
        "text_muted": "#64748b",       # Slate 500
        "border": "#334155",           # Slate 700
        "accent": "#3b82f6",           # Blue 500
        "accent_hover": "#2563eb",     # Blue 600
        "success": "#10b981",          # Emerald 500
        "warning": "#f59e0b",          # Amber 500
        "danger": "#ef4444",           # Red 500
        "danger_hover": "#dc2626",     # Red 600
    },
    "Light": {
        "bg_primary": "#f8fafc",       # Slate 50
        "bg_secondary": "#ffffff",     # White
        "bg_card": "#ffffff",          # White
        "bg_input": "#f1f5f9",         # Slate 100
        "sidebar_bg": "#0f172a",       # Slate 900
        "text_primary": "#0f172a",     # Slate 900
        "text_secondary": "#475569",   # Slate 600
        "text_muted": "#94a3b8",       # Slate 400
        "border": "#e2e8f0",           # Slate 200
        "accent": "#2563eb",           # Blue 600
        "accent_hover": "#1d4ed8",     # Blue 700
        "success": "#059669",          # Emerald 600
        "warning": "#d97706",          # Amber 600
        "danger": "#dc2626",           # Red 600
        "danger_hover": "#b91c1c",     # Red 700
    }
}

FONTS = {
    "title": ("Segoe UI", 18, "bold"),
    "heading": ("Segoe UI", 14, "bold"),
    "subheading": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 11),
    "body_bold": ("Segoe UI", 11, "bold"),
    "small": ("Segoe UI", 9),
    "caption": ("Segoe UI", 8),
    "code": ("Consolas", 10),
}


def get_colors(mode: str = "Dark") -> Dict[str, str]:
    """Returns color dictionary for given mode ('Dark' or 'Light')."""
    if mode.lower() == "light":
        return THEME_COLORS["Light"]
    return THEME_COLORS["Dark"]
