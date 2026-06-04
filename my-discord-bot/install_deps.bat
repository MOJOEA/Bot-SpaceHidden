@echo off
echo ==========================================
echo [Bot-SpaceHidden] Start Installing Libraries...
echo ==========================================
"%~dp0\.venv\Scripts\pip.exe" install -r "%~dp0\requirements.txt"
echo ==========================================
echo  Successfully Installed All Libraries!
echo ==========================================
pause
