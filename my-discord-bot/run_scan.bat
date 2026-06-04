@echo off
cls
echo ==========================================
echo       MyPC Storage Scanner
echo ==========================================
echo.

# 💡 ข้อความถามรับ Input ปกติ: จะค้างหน้าจอให้พิมพ์กรอกไดรฟ์ลงไปตรงนี้
set /p drive="Please enter drive letter to scan (C or D): "

# ถ้าผู้ใช้ไม่ได้พิมพ์อะไรแล้วกด Enter ผ่าน ให้กำหนดเป็นไดรฟ์ C อัตโนมัติ
if "%drive%"=="" set drive=C

echo.
echo ------------------------------------------
echo Running scan for Drive %drive%:...
echo ------------------------------------------
echo.

# เรียกใช้ Python วิ่งไปทำงานที่ไฟล์ test_client.py พร้อมแนบค่าไดรฟ์ที่พิมพ์ตอบไป
"%~dp0\.venv\Scripts\python.exe" "%~dp0\my-discord-bot\test_client.py" %drive%

echo.
pause
