@echo off
echo ==========================================
echo [Bot-SpaceHidden] Start Installing Libraries...
echo ==========================================
:: ใส่ ..\ เพื่อถอยออกจากโฟลเดอร์ปัจจุบันไปหา .venv ด้านนอกให้ถูกจุด
"%~dp0..\.venv\Scripts\pip.exe" install -r "%~dp0\requirements.txt"
echo ==========================================
echo  Successfully Installed All Libraries!
echo ==========================================
pause
