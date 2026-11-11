@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo   CAMPUS NEXUS - Presidency University AI Helpdesk
echo ========================================================

set "PY_CMD="

py -3 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3"
    goto :run
)

python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python"
    goto :run
)

for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%D\python.exe" (
        set "PY_CMD=%%D\python.exe"
        goto :run
    )
)

echo [ERROR] Python 3 was not detected automatically.
echo Please install Python 3.10+ from https://www.python.org/ or check "Add python.exe to PATH".
echo.
echo NOTE: You can also open "Campus Nexus Helpdesk.html" directly in any browser without Python!
pause
exit /b 1

:run
echo [INFO] Using Python: %PY_CMD%
%PY_CMD% -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Dependency install warning. Attempting to start server...
)

echo [INFO] Starting Campus Nexus server at http://127.0.0.1:5000
%PY_CMD% app.py
if %ERRORLEVEL% neq 0 (
    pause
)
