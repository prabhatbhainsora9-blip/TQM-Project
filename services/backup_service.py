"""
Backup and Restore Service for Database Maintenance and Disaster Recovery.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements automated and on-demand database snapshots, integrity verification,
pre-restore safety backups, and backup rotation.
"""

import os
import shutil
import sqlite3
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any

from services.logging_service import log_activity, get_logger


class BackupService:
    """Manages database backup creation, verification, and restoration."""

    def __init__(self, db_path: str = "data/employee_tqm.db", backup_dir: str = "backups", max_backups: int = 10):
        self.db_path = os.path.abspath(db_path)
        self.backup_dir = os.path.abspath(backup_dir)
        self.max_backups = max_backups
        self.logger = get_logger()
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self, note: str = "manual", operator: str = "Admin") -> Tuple[bool, str, Optional[str]]:
        """
        Creates a verified snapshot of the active SQLite database using the SQLite backup API.
        Safe to run while application is active.
        """
        if not os.path.exists(self.db_path):
            return False, "Database file does not exist yet.", None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}_{note}.db"
        backup_filepath = os.path.join(self.backup_dir, backup_filename)

        try:
            # Use SQLite native backup API to ensure a clean, consistent snapshot even during active writes
            source_conn = sqlite3.connect(self.db_path)
            dest_conn = sqlite3.connect(backup_filepath)
            with dest_conn:
                source_conn.backup(dest_conn, pages=100)
            dest_conn.close()
            source_conn.close()

            # Verify backup integrity
            if not self.verify_backup_integrity(backup_filepath):
                if os.path.exists(backup_filepath):
                    os.remove(backup_filepath)
                return False, "Backup failed integrity verification.", None

            # Enforce max backups limit
            self._prune_old_backups()

            log_activity("BACKUP_CREATED", f"Database backed up to {backup_filename}", module="BACKUP", level="INFO", user=operator)
            return True, f"Backup created successfully: {backup_filename}", backup_filepath

        except Exception as e:
            msg = f"Failed to create backup: {e}"
            log_activity("BACKUP_FAILED", msg, module="BACKUP", level="ERROR", user=operator)
            return False, msg, None

    def restore_backup(self, backup_filepath: str, operator: str = "Admin") -> Tuple[bool, str]:
        """
        Restores database from a selected backup file.
        Creates a pre-restore safety copy first to prevent unrecoverable data loss.
        """
        full_backup_path = os.path.abspath(backup_filepath)
        if not os.path.exists(full_backup_path):
            return False, f"Backup file not found: {backup_filepath}"

        if not self.verify_backup_integrity(full_backup_path):
            return False, "Selected backup file failed integrity check. Restore aborted."

        # 1. Create safety backup of the existing database
        safety_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safety_path = os.path.join(self.backup_dir, f"pre_restore_safety_{safety_ts}.db")
        if os.path.exists(self.db_path):
            try:
                shutil.copy2(self.db_path, safety_path)
            except Exception as e:
                return False, f"Could not create safety snapshot before restore: {e}"

        # 2. Perform restore
        try:
            shutil.copy2(full_backup_path, self.db_path)
            log_activity("BACKUP_RESTORED", f"Database restored from {os.path.basename(full_backup_path)}", module="BACKUP", level="WARNING", user=operator)
            return True, f"Database restored successfully from {os.path.basename(full_backup_path)}."
        except Exception as e:
            # Attempt rollback from safety backup
            if os.path.exists(safety_path):
                shutil.copy2(safety_path, self.db_path)
            msg = f"Failed to restore database: {e}"
            log_activity("RESTORE_FAILED", msg, module="BACKUP", level="CRITICAL", user=operator)
            return False, msg

    def verify_backup_integrity(self, filepath: str) -> bool:
        """Runs SQLite PRAGMA integrity_check on the specified file."""
        try:
            conn = sqlite3.connect(filepath)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check;")
            res = cursor.fetchone()
            conn.close()
            return res is not None and res[0] == "ok"
        except Exception:
            return False

    def list_backups(self) -> List[Dict[str, Any]]:
        """Returns sorted list of available backups with size and modification timestamp."""
        if not os.path.exists(self.backup_dir):
            return []

        backups = []
        for fname in os.listdir(self.backup_dir):
            if fname.endswith(".db"):
                fpath = os.path.join(self.backup_dir, fname)
                try:
                    stat = os.stat(fpath)
                    size_kb = round(stat.st_size / 1024, 2)
                    mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    backups.append({
                        "filename": fname,
                        "filepath": fpath,
                        "size_kb": size_kb,
                        "modified_at": mod_time,
                        "timestamp": stat.st_mtime
                    })
                except Exception:
                    pass

        # Sort newest first
        backups.sort(key=lambda x: x["timestamp"], reverse=True)
        return backups

    def _prune_old_backups(self) -> None:
        """Removes oldest backups if count exceeds max_backups limit."""
        backups = self.list_backups()
        if len(backups) > self.max_backups:
            for b in backups[self.max_backups:]:
                try:
                    os.remove(b["filepath"])
                except Exception:
                    pass
