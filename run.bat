@echo off
REM ==============================================================================
REM Launcher for Employee Management System (TQM Edition)
REM Student: Prabhat Singh Bhainsora (2410302046) | Course: BBAT104
REM ==============================================================================

title Employee Management System - TQM Edition
echo ======================================================================
echo Launching Employee Management System (TQM Maintainability Edition)
echo Student: Prabhat Singh Bhainsora  ^| Roll: 2410302046  ^| Course: BBAT104
echo ======================================================================

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application exited with error code %ERRORLEVEL%.
    pause
)
