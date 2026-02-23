@echo off
setlocal enabledelayedexpansion

REM Video Downloader - Windows Batch Runner
REM This file runs the Video Downloader application

echo ========================================
echo     Video Downloader Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Display Python version
echo Python installed:
python --version
echo.

REM Check if dependencies are installed
echo Checking dependencies...
pip show yt-dlp >nul 2>&1
if errorlevel 1 (
    echo.
    echo yt-dlp is not installed. Installing now...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Starting Video Downloader...
echo ========================================
echo.

REM Run the application
python video_downloader.py

REM Pause at the end if the script closes unexpectedly
if errorlevel 1 (
    echo.
    echo An error occurred while running the application.
    pause
    exit /b 1
)

endlocal
