@echo off
setlocal
cd /d "%~dp0"
title AI Claims Triage Prototype
color 0B

echo ======================================================
echo       AI-DRIVEN CLAIMS TRIAGE PROTOTYPE
echo ======================================================
echo.
echo Starting the application. Please keep this window open.
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py"
    goto :start
)

where python >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
    goto :start
)

echo ERROR: Python was not found on this computer.
echo.
echo Please install Python 3 from:
echo https://www.python.org/downloads/
echo.
echo During installation, select "Add Python to PATH".
echo Then close this window and double-click START_APPLICATION.bat again.
echo.
pause
exit /b 1

:start
echo Python detected: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.
echo The application will open at http://127.0.0.1:53127
echo If the browser does not open, copy that address into Chrome or Edge.
echo.

start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:53127"
%PYTHON_CMD% -u -m app.server

if not %errorlevel%==0 (
    echo.
    echo ======================================================
    echo The application stopped because of an error.
    echo ======================================================
    echo.
    pause
)
endlocal
