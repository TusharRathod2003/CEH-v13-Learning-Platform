@echo off
title HackRange & CEH v13 Cyber Enclave Launcher
cls
echo ========================================================
echo   [+] Cyber Warfare & CEH v13 Practical Training Hub
echo ========================================================
echo.
echo   [1] Launch HackRange Cyber Range (24 Labs, Admin Deck, Sandboxes)
echo   [2] Launch CEH v13 Practical Learning Platform (20 Modules + AD CS)
echo   [3] Launch Both Platforms
echo.
echo ========================================================
choice /c 123 /t 5 /d 1 /m "Select platform to launch [Default in 5s: 1]: "

if errorlevel 3 goto BOTH
if errorlevel 2 goto CEH
if errorlevel 1 goto HACKRANGE

:HACKRANGE
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "%~dp0index.html"
    exit
)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "%~dp0index.html"
    exit
)
start "" "%~dp0index.html"
exit

:CEH
call "%~dp0launch_ceh.bat"
exit

:BOTH
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "%~dp0index.html"
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "%~dp0ceh.html"
    exit
)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "%~dp0index.html"
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "%~dp0ceh.html"
    exit
)
start "" "%~dp0index.html"
start "" "%~dp0ceh.html"
exit
