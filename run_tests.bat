@echo off
REM ==============================================================================
REM Automated Test Runner for Employee Management System (TQM Edition)
REM ==============================================================================

title Run Pytest Automated Tests
echo ======================================================================
echo Running Automated Test Suite for BBAT104 TQM Project
echo ======================================================================

pytest -v -s tests/

echo.
pause
