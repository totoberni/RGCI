@echo off
:: Setup script for RGCI environment on Windows

echo Setting up RGCI environment...

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo Failed to activate virtual environment. Please check your Python installation.
    exit /b 1
)

:: Install requirements
echo Installing requirements...
pip install -r requirements.txt

:: Create .env file if it doesn't exist
if not exist .env if exist .env.example (
    echo Creating .env file from example...
    copy .env.example .env
    echo Please update the .env file with your API keys.
)

echo.
echo Environment setup complete!
echo Virtual environment is active. Run 'deactivate' to exit.
echo.
echo Usage examples:
echo   - Generate test data: python scripts\run_data_gen.py ^<settings_index^>
echo   - Run evaluation: python scripts\run_evaluation.py ^<settings_index^> 