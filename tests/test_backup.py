"""
Unit tests for database backup snapshot creation, integrity checks, and restore safety.
"""

import os
import sqlite3
import tempfile
from services.backup_service import BackupService
from database.schema import initialize_database


def test_backup_creation_and_integrity():
    """Verifies that BackupService creates a valid, verifiable SQLite snapshot."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "primary.db")
        backup_dir = os.path.join(tmpdir, "backups")

        # Create active database
        conn = sqlite3.connect(db_path)
        initialize_database(conn)
        conn.execute("INSERT INTO employees (employee_code, full_name, department, designation, email, phone, date_of_joining, status, created_at, updated_at) VALUES ('EMP-B1', 'Backup Test', 'IT', 'Admin', 'b1@test.com', '9876543210', '2026-01-01', 'Active', '2026-01-01', '2026-01-01')")
        conn.commit()
        conn.close()

        service = BackupService(db_path=db_path, backup_dir=backup_dir, max_backups=5)
        ok, msg, fpath = service.create_backup(note="test_unit")

        assert ok is True
        assert fpath is not None
        assert os.path.exists(fpath)

        # Verify integrity
        assert service.verify_backup_integrity(fpath) is True

        # Verify backup listing
        backups = service.list_backups()
        assert len(backups) == 1
        assert backups[0]["filename"].endswith("test_unit.db")


def test_backup_restore_recovers_data():
    """Tests that restoring from a backup successfully recovers saved data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "primary.db")
        backup_dir = os.path.join(tmpdir, "backups")

        # Create and initialize database
        conn = sqlite3.connect(db_path)
        initialize_database(conn)
        conn.execute("INSERT INTO employees (employee_code, full_name, department, designation, email, phone, date_of_joining, status, created_at, updated_at) VALUES ('EMP-RESTORE', 'Recovered User', 'Finance', 'Auditor', 'rec@test.com', '9876543210', '2026-01-01', 'Active', '2026-01-01', '2026-01-01')")
        conn.commit()
        conn.close()

        # Take backup
        service = BackupService(db_path=db_path, backup_dir=backup_dir)
        ok, _, backup_file = service.create_backup(note="checkpoint")
        assert ok is True
        assert backup_file is not None

        # Now simulate accidental data deletion in primary DB
        conn = sqlite3.connect(db_path)
        conn.execute("DELETE FROM employees")
        conn.commit()
        conn.close()

        # Perform restore
        restore_ok, restore_msg = service.restore_backup(backup_file)
        assert restore_ok is True

        # Verify record has returned
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT full_name FROM employees WHERE employee_code = 'EMP-RESTORE'")
        row = cursor.fetchone()
        conn.close()

        assert row is not None
        assert row[0] == "Recovered User"
