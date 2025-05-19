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
pip install -r config\requirements.txt

:: Create .env file if it doesn't exist
if not exist config\.env (
    echo Creating .env file in config directory...
    
    :: Create an example .env file content
    (
    echo # OpenAI API Keys
    echo OPENAI_API_KEY=sk-your-openai-api-key
    echo OPENAI_API_KEY_EXTRACTOR=sk-your-openai-api-key-for-extraction
    echo.
    echo # API Connection Settings
    echo API_HOST=api.openai.com
    echo USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
    echo CONTENT_TYPE=application/json
    echo.
    echo # Output Directories
    echo # To customize data location, specify a custom path. Don't include 'generated_data' in this path
    echo # as it will be added automatically by the framework.
    echo OUTPUT_PATH=data
    ) > config\.env.template
    
    echo Please update the config\.env file with your API keys.
)

echo.
echo Environment setup complete!
echo Virtual environment is active. Run 'deactivate' to exit.
echo.
echo Usage examples:
echo   - Generate test data: python scripts\run_data_gen.py ^<settings_index^>
echo   - Run evaluation: python scripts\run_evaluation.py ^<settings_index^> 