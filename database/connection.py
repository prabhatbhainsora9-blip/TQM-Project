"""
Database Connection Manager for Employee Management System (TQM Edition).
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Provides parameterized query execution, transaction support, connection pooling,
and foreign key enforcement for SQLite3 storage.
"""

import os
import sqlite3
import threading
from contextlib import contextmanager
from typing import Generator, Optional


class DatabaseConnection:
    """Thread-safe SQLite connection factory with automatic foreign keys and WAL mode."""

    def __init__(self, db_path: str = "data/employee_tqm.db", timeout: float = 10.0):
        self.db_path = os.path.abspath(db_path)
        self.timeout = timeout
        self._local = threading.local()

        # Ensure parent directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _create_raw_connection(self) -> sqlite3.Connection:
        """Creates and configures a new SQLite connection."""
        conn = sqlite3.connect(
            self.db_path,
            timeout=self.timeout,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.row_factory = sqlite3.Row
        # Enforce foreign key constraints and fast journaling
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def get_connection(self) -> sqlite3.Connection:
        """Retrieves or creates a thread-local database connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = self._create_raw_connection()
        return self._local.conn

    def close(self) -> None:
        """Closes the current thread's connection if open."""
        if hasattr(self._local, "conn") and self._local.conn is not None:
            try:
                self._local.conn.close()
            except Exception:
                pass
            finally:
                self._local.conn = None

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Cursor, None, None]:
        """
        Context manager providing atomic transaction management.
        Automatically commits on success or rolls back on exception.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()


# Global default instance
_GLOBAL_DB_INSTANCE: Optional[DatabaseConnection] = None


def get_db_manager(db_path: Optional[str] = None) -> DatabaseConnection:
    """Returns or creates the global DatabaseConnection singleton."""
    global _GLOBAL_DB_INSTANCE
    if _GLOBAL_DB_INSTANCE is None or (db_path and os.path.abspath(db_path) != _GLOBAL_DB_INSTANCE.db_path):
        _GLOBAL_DB_INSTANCE = DatabaseConnection(db_path=db_path or "data/employee_tqm.db")
    return _GLOBAL_DB_INSTANCE


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Convenience accessor to get an active SQLite connection."""
    return get_db_manager(db_path).get_connection()
