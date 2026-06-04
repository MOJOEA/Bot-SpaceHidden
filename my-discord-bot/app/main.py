# app/main.py
from app.interfaces.terminal_ui import launch_terminal_interface
from app.interfaces.discord_ui import launch_discord_interface

# สลับสวิตช์ทางผ่านให้หันมาประมวลผลสตาร์ทตัวบอทดิสคอร์ดแทนหน้าต่าง Terminal 
#if __name__ == "__main__":
    # ปัจจุบันสั่งเปิดหน้าต่าง Terminal อนาคตสามารถสลับบรรทัดเป็นเปิด Discord บอทได้ทันที
    #launch_terminal_interface()

# สลับสวิตช์ทางผ่านให้หันมาประมวลผลสตาร์ทตัวบอทดิสคอร์ดแทนหน้าต่าง discord 
if __name__ == "__main__":
    launch_discord_interface()
