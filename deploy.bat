@echo off
echo ========================================
echo   Argentine ADR Portfolio Analysis
echo   Streamlit Deployment Helper
echo ========================================
echo.

echo Step 1: Check if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git from:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
) else (
    echo Git is installed. 
)

echo.
echo Step 2: Check if Python is installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python from:
    echo https://python.org
    echo.
    pause
    exit /b 1
) else (
    echo Python is installed. 
)

echo.
echo Step 3: Initialize Git repository...
git init
git add .
git commit -m "Initial Argentine ADR Portfolio Analysis"

echo.
echo Step 4: Instructions for GitHub...
echo.
echo Please follow these steps:
echo 1. Go to https://github.com
echo 2. Create a new repository named: argentine-adr-portfolio
echo 3. Make it Public
echo 4. Don't initialize with README
echo 5. Copy the repository URL
echo.
echo Then run these commands (replace YOUR_USERNAME with your GitHub username):
echo git remote add origin https://github.com/YOUR_USERNAME/argentine-adr-portfolio.git
echo git branch -M main
echo git push -u origin main
echo.
echo Finally, deploy on Streamlit Cloud:
echo 1. Go to https://share.streamlit.io
echo 2. Sign in with GitHub
echo 3. Click "New app"
echo 4. Select your repository
echo 5. Set main file path: app.py
echo 6. Click "Deploy"
echo.
pause
