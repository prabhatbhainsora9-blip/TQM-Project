"""
Activity Logging Service for Employee Management System (TQM Edition).
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements Feature 4: Activity Logs.
Uses Python's logging module with RotatingFileHandler to record all
operational events, validation errors, database changes, and system warnings.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import List, Dict, Optional, Any

_LOGGER_INITIALIZED = False
LOGGER_NAME = "tqm_ems"


def setup_logging(
    log_dir: str = "logs",
    log_file: str = "logs/application.log",
    log_level: str = "INFO",
    max_bytes: int = 1048576,
    backup_count: int = 5
) -> logging.Logger:
    """Configures the root application logger with rotating file and console handlers."""
    global _LOGGER_INITIALIZED

    os.makedirs(os.path.abspath(log_dir), exist_ok=True)
    full_log_path = os.path.abspath(log_file)

    logger = logging.getLogger(LOGGER_NAME)
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Close existing handlers to release file locks
    for h in list(logger.handlers):
        try:
            h.close()
        except Exception:
            pass
    logger.handlers.clear()

    # Formatter with timestamp, level, module, message
    log_format = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s:%(module)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Rotating file handler
    file_handler = RotatingFileHandler(
        full_log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(numeric_level)
    logger.addHandler(file_handler)

    # Console handler for terminal visibility
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(numeric_level)
    logger.addHandler(console_handler)

    _LOGGER_INITIALIZED = True
    return logger


def get_logger() -> logging.Logger:
    """Returns the preconfigured application logger."""
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        return setup_logging()
    return logger


def log_activity(
    event_type: str,
    description: str,
    module: str = "SYSTEM",
    level: str = "INFO",
    user: str = "Admin",
    db_conn: Optional[Any] = None
) -> None:
    """
    Records an operational event in the activity log and optionally in the database audit log.
    Never logs sensitive passwords or authentication tokens.
    """
    logger = get_logger()
    log_msg = f"[{module}] [{event_type}] ({user}) {description}"

    level_upper = level.upper()
    if level_upper == "DEBUG":
        logger.debug(log_msg)
    elif level_upper == "WARNING":
        logger.warning(log_msg)
    elif level_upper == "ERROR":
        logger.error(log_msg)
    elif level_upper == "CRITICAL":
        logger.critical(log_msg)
    else:
        logger.info(log_msg)

    # Immediately flush handlers so disk file is up to date
    for h in logger.handlers:
        try:
            h.flush()
        except Exception:
            pass

    # Also persist to database audit table if connection is supplied
    if db_conn is not None:
        try:
            cursor = db_conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                INSERT INTO audit_logs (timestamp, event_type, description, user, module, level)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (timestamp, event_type, description, user, module, level_upper)
            )
            db_conn.commit()
        except Exception as e:
            logger.debug(f"Failed to write audit log to database: {e}")


def read_log_entries(
    log_file_path: str = "logs/application.log",
    max_lines: int = 500,
    level_filter: Optional[str] = None,
    search_text: Optional[str] = None,
    date_filter: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Parses and filters log entries from the rotating log file for the Log Viewer UI.
    """
    full_path = os.path.abspath(log_file_path)
    if not os.path.exists(full_path):
        return []

    entries: List[Dict[str, str]] = []

    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        # Parse from newest to oldest
        for line in reversed(lines):
            line_str = line.strip()
            if not line_str:
                continue

            # Check format: [timestamp] [level] [module] message
            if line_str.startswith("[") and "]" in line_str:
                try:
                    parts = line_str.split("] [", 2)
                    if len(parts) >= 3:
                        timestamp = parts[0].lstrip("[")
                        level = parts[1]
                        rest = parts[2]
                        module_part, message = rest.split("] ", 1) if "] " in rest else ("SYSTEM", rest)

                        # Filter checks
                        if level_filter and level_filter.upper() != "ALL" and level.upper() != level_filter.upper():
                            continue
                        if date_filter and not timestamp.startswith(date_filter):
                            continue
                        if search_text and search_text.lower() not in line_str.lower():
                            continue

                        entries.append({
                            "timestamp": timestamp,
                            "level": level,
                            "module": module_part,
                            "message": message,
                            "raw": line_str
                        })

                        if len(entries) >= max_lines:
                            break
                        continue
                except Exception:
                    pass

            # Fallback for multiline traceback or unformatted lines
            if search_text and search_text.lower() not in line_str.lower():
                continue
            entries.append({
                "timestamp": "-",
                "level": "INFO",
                "module": "RAW",
                "message": line_str,
                "raw": line_str
            })
            if len(entries) >= max_lines:
                break

    except Exception as e:
        get_logger().error(f"Error reading log file: {e}")

    return entries
