"""
Pytest Fixtures for Employee Management System Test Suite.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Provides isolated temporary SQLite databases and configuration files
so test execution never alters real operational data.
"""

import os
import tempfile
import sqlite3
import pytest
from typing import Generator

from database.schema import initialize_database
from database.connection import DatabaseConnection
from services.configuration_service import ConfigurationService
from services.employee_service import EmployeeService
from services.tqm_service import TQMService
from services.backup_service import BackupService


@pytest.fixture
def temp_db_path() -> Generator[str, None, None]:
    """Provides a temporary SQLite database file that is cleaned up after testing."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass


@pytest.fixture
def test_db_conn(temp_db_path: str) -> Generator[sqlite3.Connection, None, None]:
    """Provides an initialized SQLite connection with tables created."""
    manager = DatabaseConnection(db_path=temp_db_path)
    conn = manager.get_connection()
    initialize_database(conn)
    yield conn
    manager.close()


@pytest.fixture
def employee_service(test_db_conn: sqlite3.Connection) -> EmployeeService:
    """Provides an EmployeeService instance backed by an isolated test database."""
    return EmployeeService(test_db_conn)


@pytest.fixture
def tqm_service(test_db_conn: sqlite3.Connection) -> TQMService:
    """Provides a TQMService instance backed by an isolated test database."""
    return TQMService(test_db_conn)


@pytest.fixture
def temp_config_file() -> Generator[str, None, None]:
    """Provides a temporary config.json file path for testing."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass


@pytest.fixture
def config_service(temp_config_file: str) -> ConfigurationService:
    """Provides an isolated ConfigurationService using a temporary file."""
    return ConfigurationService(config_file_path=temp_config_file)
