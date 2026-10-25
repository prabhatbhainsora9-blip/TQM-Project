"""
System Settings and Backup Management View.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements Feature 3 (System Settings) and Feature 2 (Configuration Persistence):
- Appearance mode (Dark/Light/System)
- Accent color schemes
- UI scaling (80% - 120%)
- Records pagination limit
- Logging verbosity
- Database backup snapshot and restore controls
"""

import os
import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Optional

from services.configuration_service import ConfigurationService
from services.backup_service import BackupService
from services.validation_service import ValidationService


class SettingsView(ctk.CTkScrollableFrame):
    """System settings management interface with live configuration persistence."""

    def __init__(
        self,
        master,
        config_service: ConfigurationService,
        backup_service: BackupService,
        on_settings_applied: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.config_service = config_service
        self.backup_service = backup_service
        self.on_settings_applied = on_settings_applied

        self.grid_columnconfigure((0, 1), weight=1)

        self._build_header()
        self._build_appearance_settings()
        self._build_table_settings()
        self._build_logging_settings()
        self._build_backup_controls()
        self._build_action_buttons()

        self._load_current_values()

    def _build_header(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 6))

        ctk.CTkLabel(bar, text="SYSTEM CONFIGURATION & QUALITY CONTROLS (Q11)", font=("Segoe UI", 12, "bold"), text_color=("#0f172a", "#f8fafc")).pack(side="left", padx=15, pady=10)
        ctk.CTkLabel(bar, text="All settings are persisted to config.json with safe default recovery.", font=("Segoe UI", 9.5), text_color=("#64748b", "#94a3b8")).pack(side="right", padx=15, pady=10)

    def _build_appearance_settings(self) -> None:
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)

        ctk.CTkLabel(card, text="APPEARANCE & THEME", font=("Segoe UI", 11, "bold"), text_color="#3b82f6").pack(anchor="w", padx=15, pady=(12, 6))

        # Theme Mode
        ctk.CTkLabel(card, text="Color Theme Mode:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(4, 1))
        self.combo_theme = ctk.CTkComboBox(card, values=["Dark", "Light", "System"], height=30)
        self.combo_theme.pack(fill="x", padx=15, pady=(0, 8))

        # Accent Color
        ctk.CTkLabel(card, text="Accent Color Theme:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(4, 1))
        self.combo_accent = ctk.CTkComboBox(card, values=["blue", "dark-blue", "green"], height=30)
        self.combo_accent.pack(fill="x", padx=15, pady=(0, 8))

        # UI Scaling
        ctk.CTkLabel(card, text="Interface Scaling:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(4, 1))
        self.combo_scaling = ctk.CTkComboBox(card, values=["90%", "100%", "110%", "120%"], height=30)
        self.combo_scaling.pack(fill="x", padx=15, pady=(0, 14))

    def _build_table_settings(self) -> None:
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.grid(row=1, column=1, sticky="nsew", padx=10, pady=6)

        ctk.CTkLabel(card, text="DATA & INTERACTION PREFERENCES", font=("Segoe UI", 11, "bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(12, 6))

        # Records per page
        ctk.CTkLabel(card, text="Records Displayed Per Page:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(4, 1))
        self.combo_records = ctk.CTkComboBox(card, values=["5", "10", "20", "50", "100"], height=30)
        self.combo_records.pack(fill="x", padx=15, pady=(0, 8))

        # Confirm Delete
        self.switch_confirm_delete = ctk.CTkSwitch(card, text="Require confirmation dialog before record deletion", font=("Segoe UI", 9))
        self.switch_confirm_delete.pack(anchor="w", padx=15, pady=(10, 8))

        # Toast notifications
        self.switch_toasts = ctk.CTkSwitch(card, text="Enable audit toast feedback for database operations", font=("Segoe UI", 9))
        self.switch_toasts.pack(anchor="w", padx=15, pady=(4, 14))

    def _build_logging_settings(self) -> None:
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.grid(row=2, column=0, sticky="nsew", padx=10, pady=6)

        ctk.CTkLabel(card, text="ACTIVITY LOGGING (Feature 4)", font=("Segoe UI", 11, "bold"), text_color="#f59e0b").pack(anchor="w", padx=15, pady=(12, 6))

        ctk.CTkLabel(card, text="Logging Verbosity Level:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(4, 1))
        self.combo_log_level = ctk.CTkComboBox(card, values=["DEBUG", "INFO", "WARNING", "ERROR"], height=30)
        self.combo_log_level.pack(fill="x", padx=15, pady=(0, 8))

        ctk.CTkLabel(card, text="Log File Target:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(4, 1))
        self.entry_log_path = ctk.CTkEntry(card, height=30)
        self.entry_log_path.pack(fill="x", padx=15, pady=(0, 14))

    def _build_backup_controls(self) -> None:
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.grid(row=2, column=1, sticky="nsew", padx=10, pady=6)

        ctk.CTkLabel(card, text="DISASTER RECOVERY & BACKUPS", font=("Segoe UI", 11, "bold"), text_color="#8b5cf6").pack(anchor="w", padx=15, pady=(12, 6))

        ctk.CTkLabel(card, text="Create instant snapshot of SQLite database with integrity verification:", font=("Segoe UI", 9), text_color=("#64748b", "#94a3b8"), wraplength=400, justify="left").pack(anchor="w", padx=15, pady=(2, 6))

        btn_box = ctk.CTkFrame(card, fg_color="transparent")
        btn_box.pack(fill="x", padx=15, pady=(4, 8))

        btn_create_backup = ctk.CTkButton(btn_box, text="Create Backup Snapshot", width=170, height=32, fg_color="#8b5cf6", hover_color="#7c3aed", command=self._create_backup)
        btn_create_backup.pack(side="left", padx=(0, 8))

        btn_list_backups = ctk.CTkButton(btn_box, text="List / Restore Backups", width=160, height=32, fg_color="#475569", command=self._open_restore_dialog)
        btn_list_backups.pack(side="left")

        self.lbl_backup_status = ctk.CTkLabel(card, text="", font=("Segoe UI", 9), text_color="#10b981")
        self.lbl_backup_status.pack(anchor="w", padx=15, pady=(2, 10))

    def _build_action_buttons(self) -> None:
        actions = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
        actions.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        btn_reset = ctk.CTkButton(actions, text="Reset to Defaults", width=140, height=34, fg_color="#ef4444", hover_color="#dc2626", command=self._reset_defaults)
        btn_reset.pack(side="left", padx=15, pady=10)

        btn_save = ctk.CTkButton(actions, text="Save Settings", width=150, height=34, fg_color="#2563eb", hover_color="#1d4ed8", command=self._save_settings)
        btn_save.pack(side="right", padx=15, pady=10)

    def _load_current_values(self) -> None:
        """Fills input fields from current ConfigurationService."""
        cfg = self.config_service.get_all()

        self.combo_theme.set(cfg.get("ui", {}).get("theme", "Dark"))
        self.combo_accent.set(cfg.get("ui", {}).get("accent_color", "blue"))

        scaling_val = cfg.get("ui", {}).get("scaling", 1.0)
        self.combo_scaling.set(f"{int(scaling_val * 100)}%")

        self.combo_records.set(str(cfg.get("ui", {}).get("records_per_page", 10)))

        if cfg.get("ui", {}).get("confirm_delete", True):
            self.switch_confirm_delete.select()
        else:
            self.switch_confirm_delete.deselect()

        if cfg.get("ui", {}).get("enable_toast_notifications", True):
            self.switch_toasts.select()
        else:
            self.switch_toasts.deselect()

        self.combo_log_level.set(cfg.get("logging", {}).get("log_level", "INFO"))
        self.entry_log_path.delete(0, "end")
        self.entry_log_path.insert(0, cfg.get("logging", {}).get("log_file", "logs/application.log"))

    def _save_settings(self) -> None:
        """Validates settings and writes to config.json, applying theme dynamically."""
        scaling_map = {"90%": 0.9, "100%": 1.0, "110%": 1.1, "120%": 1.2}
        scaling_num = scaling_map.get(self.combo_scaling.get(), 1.0)

        new_settings = {
            "records_per_page": int(self.combo_records.get()),
            "scaling": scaling_num,
            "theme": self.combo_theme.get()
        }

        ok, err = ValidationService.validate_settings(new_settings)
        if not ok:
            messagebox.showerror("Invalid Settings", err)
            return

        self.config_service.set("ui.theme", self.combo_theme.get())
        self.config_service.set("ui.accent_color", self.combo_accent.get())
        self.config_service.set("ui.scaling", scaling_num)
        self.config_service.set("ui.records_per_page", int(self.combo_records.get()))
        self.config_service.set("ui.confirm_delete", bool(self.switch_confirm_delete.get()))
        self.config_service.set("ui.enable_toast_notifications", bool(self.switch_toasts.get()))
        self.config_service.set("logging.log_level", self.combo_log_level.get())
        self.config_service.set("logging.log_file", self.entry_log_path.get().strip())

        if self.config_service.save():
            # Apply theme change live
            ctk.set_appearance_mode(self.combo_theme.get())
            ctk.set_widget_scaling(scaling_num)

            messagebox.showinfo("Settings Saved", "System settings saved successfully and applied to the application.")
            if self.on_settings_applied:
                self.on_settings_applied()
        else:
            messagebox.showerror("Error", "Failed to write configuration file.")

    def _reset_defaults(self) -> None:
        ans = messagebox.askyesno("Reset to Defaults", "Reset all settings to factory default values?")
        if ans:
            self.config_service.reset_to_defaults()
            self._load_current_values()
            ctk.set_appearance_mode("Dark")
            ctk.set_widget_scaling(1.0)
            messagebox.showinfo("Reset Complete", "Default configuration restored.")
            if self.on_settings_applied:
                self.on_settings_applied()

    def _create_backup(self) -> None:
        ok, msg, fpath = self.backup_service.create_backup(note="manual_snapshot")
        if ok and fpath:
            self.lbl_backup_status.configure(text=f"Last backup: {os.path.basename(fpath)}")
            messagebox.showinfo("Backup Successful", msg)
        else:
            messagebox.showerror("Backup Failed", msg)

    def _open_restore_dialog(self) -> None:
        backups = self.backup_service.list_backups()
        if not backups:
            messagebox.showinfo("No Backups", "No database backups found in 'backups/' directory.")
            return

        dlg = ctk.CTkToplevel(self)
        dlg.title("Database Restore Manager")
        dlg.geometry("520x420")
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="AVAILABLE DATABASE BACKUPS", font=("Segoe UI", 12, "bold")).pack(pady=(15, 6))
        ctk.CTkLabel(dlg, text="Restoring will automatically create a pre-restore safety copy first.", font=("Segoe UI", 9), text_color="#94a3b8").pack(pady=(0, 10))

        scroll = ctk.CTkScrollableFrame(dlg, fg_color="transparent", height=240)
        scroll.pack(fill="both", expand=True, padx=20, pady=5)

        for b in backups:
            row = ctk.CTkFrame(scroll, fg_color=("#ffffff", "#1e293b"), corner_radius=6)
            row.pack(fill="x", pady=3)

            info_text = f"{b['filename']}\nSize: {b['size_kb']} KB | Modified: {b['modified_at']}"
            ctk.CTkLabel(row, text=info_text, font=("Segoe UI", 9), justify="left", anchor="w").pack(side="left", padx=10, pady=6)

            btn_rest = ctk.CTkButton(
                row, text="Restore", width=80, height=28, fg_color="#ef4444", hover_color="#dc2626",
                command=lambda f=b["filepath"], d=dlg: self._perform_restore(f, d)
            )
            btn_rest.pack(side="right", padx=10, pady=6)

    def _perform_restore(self, filepath: str, dialog: ctk.CTkToplevel) -> None:
        ans = messagebox.askyesno(
            "Confirm Database Restore",
            f"Are you sure you want to restore from:\n{os.path.basename(filepath)}?\nA pre-restore safety snapshot will be created automatically."
        )
        if ans:
            ok, msg = self.backup_service.restore_backup(filepath)
            if ok:
                messagebox.showinfo("Restore Success", f"{msg}\nPlease restart or refresh the view.")
                dialog.destroy()
                if self.on_settings_applied:
                    self.on_settings_applied()
            else:
                messagebox.showerror("Restore Failed", msg)
