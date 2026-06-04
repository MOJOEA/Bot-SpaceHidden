# app/core/handler.py
from app.modules.disk_scanner.scanner import check_drive_space_and_cache, get_cached_path_info, get_all_cached_data

def process_central_command(raw_input):
    """ฟังก์ชันศูนย์กลางฉบับรับจบสำหรับ Discord บอท ดึงข้อมูลตรงจากคำสั่งสแลชได้ทันที"""
    clean_text = raw_input.strip().lower()
    
    if not clean_text:
        return {"action": "ignore"}
    if clean_text == "exit":
        return {"action": "shutdown", "message": "กำลังปิดระบบ..."}
        
    # 1. คำสั่งดึงข้อมูลมัดรวม 3 พาร์ทสำหรับปุ่ม /all
    if clean_text == "/all":
        drive_result = check_drive_space_and_cache("C")
        if drive_result["success"]:
            all_parts_result = get_all_cached_data()
            return {
                "action": "display_all", 
                "drive_data": drive_result, 
                "parts_data": all_parts_result.get("all_parts", {})
            }
        return {"action": "error", "message": drive_result["error"]}
        
    # 2. คำสั่งสแกนทั่วไปตามเงื่อนไขชื่อไดรฟ์ที่ส่งมาจากปุ่มแรก (scan c, scan d)
    if clean_text.startswith("scan "):
        parts = clean_text.split(" ")
        if len(parts) >= 2:
            # ดึงตัวอักษรไดรฟ์ตัวที่สอง เช่น "c" หรือ "d"
            drive_letter = parts[1].upper() 
            result = check_drive_space_and_cache(drive_letter)
            if result["success"]:
                return {"action": "display_base_drive", "data": result}
            return {"action": "error", "message": result["error"]}
            
    # 3. คำสั่งจิ้มดึงสถิติรายโฟลเดอร์สำหรับปุ่มกด
    if clean_text in ["/local", "/program_files", "/program_files_x86"]:
        target_key = clean_text.replace("/", "")
        result = get_cached_path_info(target_key)
        if result["success"]:
            return {"action": "display_deep_path", "data": result}
        return {"action": "error", "message": result["error"]}
            
    return {"action": "error", "message": f"ไม่พบชุดคำสั่งระบบสำหรับ: '{raw_input}'"}
