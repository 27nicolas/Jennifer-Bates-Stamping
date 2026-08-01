@echo off
REM This script starts the Jennifer Bates Stamping desktop application.

REM Change the current directory to the script's directory.
REM This ensures that the application can find its files correctly.
cd /d "%~dp0"

echo Starting the Bates Stamping application...
REM Run the Python GUI application.

REM --- Method 1: Try to activate Anaconda and run (most reliable for Anaconda users) ---
echo Trying to use Anaconda...
call conda.bat activate base >nul 2>nul
if %errorlevel% == 0 (
    echo Anaconda environment activated.
    python gui_app.py
    goto :eof
)

REM --- Method 2: Try the standard Python launcher 'py.exe' ---
echo Anaconda not found or failed. Trying standard Python launcher...
py gui_app.py
if %errorlevel% == 0 goto :eof

REM --- Method 3: Try the generic 'python' command ---
echo Standard launcher not found. Trying generic 'python' command...
python gui_app.py
if %errorlevel% == 0 goto :eof

REM --- If both methods fail, display a helpful error message ---
echo.
echo ====================================================================
echo  ERROR: Could not find a working Python installation.
echo ====================================================================
echo.
echo If you are using Anaconda, please try running this from the 'Anaconda Prompt'.
echo.
pause