@echo off
setlocal

cd /d "%~dp0"

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=py
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PY_CMD=python
    ) else (
        echo Python was not found on PATH.
        echo Install Python 3.12 and make sure 'py' or 'python' is available.
        pause
        exit /b 1
    )
)

if not exist .venv (
    echo Creating virtual environment...
    %PY_CMD% -3.12 -m venv .venv 2>nul
    if %ERRORLEVEL% NEQ 0 (
        %PY_CMD% -m venv .venv
    )
)

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m app.main

pause
