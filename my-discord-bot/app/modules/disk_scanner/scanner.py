# app/modules/disk_scanner/scanner.py
import os
import shutil
import getpass

# แคชส่วนกลางรองรับการเก็บแยกไดรฟ์
_cached_deep_scan_data = {}

def get_folder_size(path):
    """คำนวณขนาดโฟลเดอร์แบบปลอดภัยด้วย os.scandir"""
    total_size = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_file(follow_symlinks=False):
                        total_size += entry.stat(follow_symlinks=False).st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total_size += get_folder_size(entry.path)
                except (PermissionError, FileNotFoundError):
                    continue
    except (PermissionError, FileNotFoundError):
        pass
    return total_size

def format_size_dynamic(size_bytes):
    if size_bytes >= 1024**3:
        return f"{size_bytes / (1024**3):.1f} GB"
    return f"{size_bytes / (1024**2):.1f} MB"

def check_drive_space_and_cache(drive_letter):
    """[คำสั่งสเตจ 2] ดึงภาพรวมความจุไดรฟ์ + ทำการแอบคำนวณพาร์ทย่อยเก็บลงหน่วยความจำทันที"""
    global _cached_deep_scan_data
    drive_letter = drive_letter.upper()
    drive_path = f"{drive_letter}:\\"
    
    try:
        total, used, free = shutil.disk_usage(drive_path)
    except FileNotFoundError:
        return {"success": False, "error": f"ไม่พบไดรฟ์ {drive_letter}: บนคอมพิวเตอร์เครื่องนี้"}

    # เคลียร์และจองพื้นที่หน่วยความจำสำหรับไดรฟ์นั้นๆ
    _cached_deep_scan_data = {}

    if drive_letter == "C":
        username = getpass.getuser()
        targets = {
            "local": (f"C:\\Users\\{username}\\AppData\\Local", "Local"),
            "program_files": ("C:\\Program Files", "Program Files"),
            "program_files_x86": ("C:\\Program Files (x86)", "Program Files (x86)")
        }
        
        for key, (path, display_name) in targets.items():
            if os.path.exists(path):
                print(f"[Processing] กำลังคำนวณสถิติภายใน: {display_name} ...")
                parent_size = get_folder_size(path)
                sub_folders = []
                
                try:
                    with os.scandir(path) as it:
                        for entry in it:
                            if entry.is_dir(follow_symlinks=False):
                                sub_size = get_folder_size(entry.path)
                                if sub_size > 0:
                                    sub_folders.append({"name": entry.name, "size_bytes": sub_size})
                except PermissionError:
                    pass
                
                sub_folders.sort(key=lambda x: x["size_bytes"], reverse=True)
                
                _cached_deep_scan_data[key] = {
                    "success": True,
                    "folder_name": display_name,
                    "total_size": format_size_dynamic(parent_size),
                    "items": [
                        {
                            "name": item["name"],
                            "size": format_size_dynamic(item["size_bytes"]),
                            "percent": f"{(item['size_bytes'] / parent_size * 100):.1f}%" if parent_size > 0 else "0%"
                        }
                        for item in sub_folders[:10]
                    ]
                }

    used_percent = (used / total) * 100 if total > 0 else 0
    bar_length = 15
    filled = int(bar_length * used_percent // 100)
    progress_bar = f"[{'█' * filled}{'░' * (bar_length - filled)}] {used_percent:.1f}%"

    return {
        "success": True,
        "drive": drive_letter,
        "progress_bar": progress_bar,
        "used": format_size_dynamic(used),
        "free": format_size_dynamic(free),
        "total": format_size_dynamic(total)
    }

def get_cached_path_info(target_key):
    global _cached_deep_scan_data
    if target_key in _cached_deep_scan_data:
        return _cached_deep_scan_data[target_key]
    return {"success": False, "error": "ไดรฟ์นี้ไม่มีพาร์ทดังกล่าว หรือพาร์ทไม่พร้อมใช้งาน"}

def get_all_cached_data():
    global _cached_deep_scan_data
    return {"success": True, "all_parts": _cached_deep_scan_data} if _cached_deep_scan_data else {"success": False}
