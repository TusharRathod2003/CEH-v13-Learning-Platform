@echo off
title CEH v13 Practical Lab Learning Platform Launcher
echo ========================================================
echo   [+] Certified Ethical Hacker (CEH v13) Lab Platform
echo   [+] 20 Core Modules + Active Directory AD CS Master Lab
echo   [+] Enclave Scope: 10.10.20.0/24
echo ========================================================
echo.

set TARGET_URL=%~dp0ceh.html

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Starting CEH Python SQLite Backend Server on port 8000...
    start "CEH Backend Server" /D "%~dp0" py "%~dp0ceh_server.py" 8000
    ping 127.0.0.1 -n 2 >nul
    set TARGET_URL=http://localhost:8000/ceh.html
    goto LAUNCH_BROWSER
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Starting CEH Python SQLite Backend Server on port 8000...
    start "CEH Backend Server" /D "%~dp0" python "%~dp0ceh_server.py" 8000
    ping 127.0.0.1 -n 2 >nul
    set TARGET_URL=http://localhost:8000/ceh.html
    goto LAUNCH_BROWSER
)

:LAUNCH_BROWSER
echo Opening in browser: %TARGET_URL%

if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "%TARGET_URL%"
    exit
)

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "%TARGET_URL%"
    exit
)

start "" "%TARGET_URL%"
exit
