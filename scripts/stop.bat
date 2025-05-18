@echo off
:: Script to stop and remove RGCI environment on Windows

echo Cleaning up RGCI environment...

:: Check if venv exists
if exist venv (
    :: Deactivate virtual environment if active
    where deactivate >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo Deactivating virtual environment...
        call deactivate
    )
    
    :: Remove virtual environment
    echo Removing virtual environment...
    rmdir /s /q venv
) else (
    echo No virtual environment found.
)

:: Clean pip cache
echo Cleaning pip cache...
pip cache purge || echo Failed to clean pip cache. May require manual deletion.

echo.
echo Environment cleanup complete!
echo Note: The .env file in config directory was not removed. Delete it manually if needed. 