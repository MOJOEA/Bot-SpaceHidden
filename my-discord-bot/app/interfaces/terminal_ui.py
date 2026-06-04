# app/interfaces/terminal_ui.py
import app.core.handler as core_module

def launch_terminal_interface():
    print("==============================================")
    print(" CORE ENGINE MULTI-STAGE CLI TERMINAL ACTIVE")
    print("==============================================")
    print(" ขั้นตอนเริ่มต้น: พิมพ์คำสั่ง 'scan' แล้วกด Enter เพื่อปลุกระบบ")
    
    while True:
        # ปรับโฉมตัวอักษรหน้าช่องป้อนข้อมูลให้เปลี่ยนตามสเตจปัจจุบันเพื่อความสวยงามและเข้าใจง่าย
        if core_module.current_state == 'START':
            prompt_label = "[Engine Root]"
        elif core_module.current_state == 'DRIVE_SELECTED_STAGE':
            prompt_label = "[Select Drive]"
        else:
            prompt_label = f"[Drive {core_module.selected_drive} Path]"
            
        user_input = input(f"{prompt_label}: ")
        response = core_module.process_central_command(user_input)
        
        action = response.get("action")
        
        if action == "shutdown":
            print(f"\n⚡ {response['message']}")
            break
            
        elif action == "prompt_drive_selection":
            # ปรับสเตจเข้าสู่ขั้นเลือกไดรฟ์ผ่านคีย์บอร์ด
            core_module.current_state = 'DRIVE_SELECTED_STAGE'
            print("\n💿 [Stage 2] โปรดระบุไดรฟ์คอมพิวเตอร์ที่ต้องการตรวจสอบ:")
            print("'/c'Scanner Drive C")
            print("'/d'Scanner Drive D")
            
        elif action == "display_base_drive":
            info = response["data"]
            print(f"\n--- ผลการสแกนคอมพิวเตอร์ Drive {info['drive']} ---")
            print(f"ภาพรวมดิส:     {info['progress_bar']}")
            print(f"กำลังใช้งาน:    {info['used']}")
            print(f"พื้นที่คงเหลือ:   {info['free']}")
            print(f"ความจุสูงสุด:   {info['total']}")
            print("=" * 46)
            
            print(f"\n🔘 [Stage 3] ข้อมูลภาพรวมของไดรฟ์ {info['drive']} ล็อกเข้าหน่วยความจำแล้ว เลือกพิมพ์คำสั่งดูพาร์ทต่อ:")
            print("'/all'               Scanner to get all 3 parts (Local, Program Files, Program Files x86) at once")
            if info["drive"] == "C":
                print("1️'/local'            Scanner AppData/Local")
                print("'/program_files'     Scanner Program Files")
                print("'/program_files_x86' Scanner Program Files (x86)")
            print("'/back'              back to main menu")
                
        elif action == "display_deep_path":
            folder_data = response["data"]
            print_single_path_table(folder_data)
            
        elif action == "display_all":
            parts_info = response["parts_data"]
            print("\n==============================================")
            print("📑 รายงานแจกแจงพาร์ทระบบจัดเต็มแบบมัดรวม 3 อัน")
            print("==============================================")
            for key in ["local", "program_files", "program_files_x86"]:
                if key in parts_info:
                    print_single_path_table(parts_info[key])
                    
        elif action == "info_only" or action == "error":
            # จัดการพิมพ์ข้อความกระชับตักเตือนกรณีหลงสเตจหรือเกิดข้อผิดพลาด
            prefix = "ℹINFO" if action == "info_only" else " ALERT"
            print(f"\n{prefix}: {response['message']}")

def print_single_path_table(folder_data):
    print(f"\n📁 โฟลเดอร์หลัก: {folder_data['folder_name']} (ขนาดรวม: {folder_data['total_size']})")
    print(f"   {'📂 โฟลเดอร์ย่อยด้านใน':<25} | {'% Parent':<10} | {'ขนาดไฟล์':<10}")
    print(f"   {'-'*25}-|-{'-'*10}-|-{'-'*10}")
    for item in folder_data["items"]:
        short_name = item['name'][:22] + "..." if len(item['name']) > 22 else item['name']
        print(f"   • {short_name:<23} | {item['percent']:<10} | {item['size']:<10}")
    print(f"   {'-'*51}")
