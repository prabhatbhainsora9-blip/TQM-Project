"""
Unit tests for database schema, initialization, and connection behavior.
"""

import sqlite3
import pytest
from database.schema import initialize_database, SCHEMA_VERSION


def test_database_initialization_creates_all_tables(test_db_conn: sqlite3.Connection):
    """Verifies that all required tables are properly created on schema initialization."""
    cursor = test_db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row["name"] for row in cursor.fetchall()}

    expected_tables = {
        "employees",
        "defects",
        "fmea_records",
        "pdca_records",
        "fishbone_causes",
        "audit_logs",
        "schema_migrations"
    }

    for table in expected_tables:
        assert table in tables, f"Expected table '{table}' was not created."


def test_schema_migration_version_recorded(test_db_conn: sqlite3.Connection):
    """Verifies that the schema version is recorded in schema_migrations."""
    cursor = test_db_conn.cursor()
    cursor.execute("SELECT version FROM schema_migrations")
    row = cursor.fetchone()
    assert row is not None
    assert row["version"] == SCHEMA_VERSION


def test_foreign_keys_are_enabled(test_db_conn: sqlite3.Connection):
    """Verifies that PRAGMA foreign_keys is enabled."""
    cursor = test_db_conn.cursor()
    cursor.execute("PRAGMA foreign_keys")
    row = cursor.fetchone()
    assert row[0] == 1, "Foreign key constraints are not enabled."
