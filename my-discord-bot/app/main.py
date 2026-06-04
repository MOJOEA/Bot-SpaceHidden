import shutil
import sys

def check_disk_storage(drive_letter="C"):
    """ฟังก์ชันเช็คพื้นที่ความจุภายในคอมพิวเตอร์"""
    # ปรับรูปแบบตัวอักษรไดรฟ์ให้ถูกต้องตามระบบ Windows (เช่น C:\)
    path = f"{drive_letter.upper()}:\\"
    
    print(f"🔍 กำลังตรวจสอบระบบพื้นที่ในไดรฟ์ {path}...\n")
    
    try:
        # ใช้คำสั่งของระบบดึงข้อมูลความจุ: ออกมาเป็นหน่วย Bytes
        total, used, free = shutil.disk_usage(path)
        
        # 📐 แปลงหน่วยจาก Bytes เป็น Gigabytes (GB)
        # โดยการหารด้วย 1024 ยกกำลัง 3 (หรือ 1,073,741,824)
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        
        # 📊 คำนวณเปอร์เซ็นต์พื้นที่ที่ถูกใช้งานไปแล้ว
        used_percent = (used / total) * 100
        
        # 🧱 สร้างแถบสถานะกราฟแท่งความยาว 15 ช่อง [██████░░░░░░░░░]
        bar_length = 15
        filled_chunks = int(bar_length * used_percent // 100)
        bar = '█' * filled_chunks + '░' * (bar_length - filled_chunks)
        progress_bar = f"[{bar}] {used_percent:.1f}%"
        
        # 📺 พิมพ์ผลลัพธ์แสดงบนหน้าจอ Terminal
        print(f"==========================================")
        print(f"💾 ผลลัพธ์การตรวจสอบไดรฟ์ ({drive_letter.upper()}:)")
        print(f"==========================================")
        print(f"📊 แถบการใช้งาน: {progress_bar}")
        print(f"🟢 พื้นที่ว่างคงเหลือ: {free_gb:.2f} GB")
        print(f"🔴 ใช้พื้นที่ไปแล้ว: {used_gb:.2f} GB / {total_gb:.2f} GB")
        print(f"==========================================")
        
    except FileNotFoundError:
        print(f"❌ ไม่พบไดรฟ์ {drive_letter.upper()}: ในคอมพิวเตอร์เครื่องนี้ กรุณาตรวจสอบชื่อไดรฟ์อีกครั้ง")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")

if __name__ == "__main__":
    # สามารถเปลี่ยนตัวอักษร 'C' เป็นไดรฟ์อื่นที่ต้องการทดสอบได้ เช่น 'D', 'E'
    check_disk_storage(drive_letter="C")
