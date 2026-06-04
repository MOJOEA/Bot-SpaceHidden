@echo off
:: ถอยออกไป 1 ชั้นเพื่อวิ่งไปหาโฟลเดอร์ .venv ที่อยู่ด้านนอก
"%~dp0..\.venv\Scripts\python.exe" -m app.main
