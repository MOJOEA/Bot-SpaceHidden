# app/modules/disk_scanner/formatter.py

def generate_progress_bar(used_bytes, total_bytes, bar_length=15):
    """ทำหน้าที่วาดหน้าตา Progress Bar ความสวยงามอย่างเดียว"""
    used_percent = (used_bytes / total_bytes) * 100 if total_bytes > 0 else 0
    filled_chunks = int(bar_length * used_percent // 100)
    bar = '█' * filled_chunks + '░' * (bar_length - filled_chunks)
    return f"[{bar}] {used_percent:.1f}%"
