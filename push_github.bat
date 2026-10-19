@echo off
title GitHub Repository Publisher
echo ========================================================
echo   Publishing to https://github.com/TusharRathod2003
echo ========================================================
echo.

set PATH=C:\Users\ratho\AppData\Local\Programs\Git\cmd;%PATH%

cd /d "C:\Users\ratho\.gemini\antigravity\scratch\hackrange"

gh auth status >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [*] Authenticating with GitHub...
    gh auth login --web -h github.com -p https
)

echo.
echo [*] Creating repository and pushing main branch...
gh repo create CEH-v13-Learning-Platform --public --source=. --remote=origin --push

echo.
echo ========================================================
echo   [+] Successfully published!
echo   [+] Visit: https://github.com/TusharRathod2003/CEH-v13-Learning-Platform
echo ========================================================
pause
