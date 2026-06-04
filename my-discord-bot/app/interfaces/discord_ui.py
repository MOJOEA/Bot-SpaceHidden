# app/interfaces/discord_ui.py
import discord
from discord import app_commands
from discord.ext import tasks, commands
import os
from app.core.handler import process_central_command

# 🛠️ อย่าลืมเปลี่ยนตัวเลขนี้ให้ตรงกับเลข ID แชนเนลห้องข่าวสารในดิสคอร์ดของคุณ
REPORT_CHANNEL_ID = int(os.getenv("DISCORD_REPORT_CHANNEL_ID"))

def format_single_path_text(folder_data):
    """จัดรูปแบบข้อมูลโครงสร้างพาร์ทให้อยู่ในกรอบ Code Block สวยงาม"""
    text = f"📁 โฟลเดอร์หลัก: {folder_data['folder_name']} (ขนาดรวม: {folder_data['total_size']})\n"
    text += f"   {'📂 โฟลเดอร์ย่อยด้านใน':<25} | {'% Parent':<10} | {'ขนาดไฟล์':<10}\n"
    text += f"   {'-'*25}-|-{'-'*10}-|-{'-'*10}\n"
    for item in folder_data["items"]:
        short_name = item['name'][:22] + "..." if len(item['name']) > 22 else item['name']
        text += f"   • {short_name:<23} | {item['percent']:<10} | {item['size']:<10}\n"
    text += f"   {'-'*51}\n"
    return text

class DeepPathSelectionView(discord.ui.View):
    """คลาสจัดการปุ่มกดตอบกลับแบบเจาะลึกเฉพาะอัน"""
    def __init__(self, selected_drive):
        super().__init__(timeout=180)
        self.selected_drive = selected_drive
        if selected_drive != "C":
            self.view_local.disabled = True
            self.view_pf.disabled = True
            self.view_pfx86.disabled = True

    @discord.ui.button(label="📊 ดูพาร์ททั้งหมดพร้อมกัน (/all)", style=discord.ButtonStyle.secondary, row=0)
    async def view_all_parts(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 🌟 ใช้ defer ในปุ่มกดเพื่อดึงเวลาป้องกัน Unknown interaction
        await interaction.response.defer(ephemeral=True)
        response = process_central_command("/all")
        if response["action"] == "display_all":
            parts_info = response["parts_data"]
            
            # 🌟 [แก้ไขปัญหาตัวอักษรเกิน 2,000] ส่งแยกพาร์ททีละกล่องข้อความเพื่อความปลอดภัย
            head_report = "==============================================\n"
            head_report += "📑 รายงานแจกแจงพาร์ทระบบจัดเต็มแบบมัดรวม 3 อัน\n"
            head_report += "==============================================\n"
            await interaction.followup.send(content=f"```text\n{head_report}```", ephemeral=True)
            
            for key in ["local", "program_files", "program_files_x86"]:
                if key in parts_info:
                    part_text = format_single_path_text(parts_info[key])
                    await interaction.followup.send(content=f"```text\n{part_text}```", ephemeral=True)
        else:
            await interaction.followup.send(content=f"❌ ALERT: {response.get('message', 'เกิดข้อผิดพลาด')}", ephemeral=True)

    @discord.ui.button(label="1️⃣ เจาะลึก Local", style=discord.ButtonStyle.primary, row=1)
    async def view_local(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        result = process_central_command("/local")
        if result["action"] == "display_deep_path":
            table_text = format_single_path_text(result["data"])
            await interaction.followup.send(f"```text\n{table_text}```", ephemeral=True)
        else:
            await interaction.followup.send(f"❌ ALERT: {result.get('message')}", ephemeral=True)

    @discord.ui.button(label="2️⃣ เจาะลึก Program Files", style=discord.ButtonStyle.success, row=1)
    async def view_pf(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        result = process_central_command("/program_files")
        if result["action"] == "display_deep_path":
            table_text = format_single_path_text(result["data"])
            await interaction.followup.send(f"```text\n{table_text}```", ephemeral=True)
        else:
            await interaction.followup.send(f"❌ ALERT: {result.get('message')}", ephemeral=True)

    @discord.ui.button(label="3️⃣ เจาะลึก Program Files (x86)", style=discord.ButtonStyle.danger, row=1)
    async def view_pfx86(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        result = process_central_command("/program_files_x86")
        if result["action"] == "display_deep_path":
            table_text = format_single_path_text(result["data"])
            await interaction.followup.send(f"```text\n{table_text}```", ephemeral=True)
        else:
            await interaction.followup.send(f"❌ ALERT: {result.get('message')}", ephemeral=True)

class DiskScannerBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = DiskScannerBot()

@bot.event
async def on_ready():
    print("==============================================")
    print(f"🤖 DISCORD BOT INTERFACE [ {bot.user.name} ] IS ONLINE")
    print("==============================================")
    if not daily_auto_report.is_running():
        daily_auto_report.start()

@bot.tree.command(name="scan_disk", description="[Stage 1] เริ่มต้นเปิดโหมดสแกนพื้นที่ดิสก์คอมพิวเตอร์จริงของคุณ")
@app_commands.describe(drive="[Stage 2] เลือกชื่อไดรฟ์พื้นที่ที่ต้องการสแกนความจุ")
@app_commands.choices(drive=[
    app_commands.Choice(name="💿 Drive C:", value="C"),
    app_commands.Choice(name="📀 Drive D:", value="D")
])
async def scan_disk(interaction: discord.Interaction, drive: app_commands.Choice[str]):
    await interaction.response.defer(ephemeral=True)
    
    # 🌟 [จุดสำคัญป้องกันบั๊กปุ่มกดโต้ตอบล้มเหลว] สั่งแสกนล่วงหน้าทั้งภาพรวมและเก็บแคช 3 พาร์ททันทีด้วยคำสั่ง /all
    if drive.value == "C":
        response = process_central_command("/all")
        # สลับแปลงหัวข้อมูลให้แมตช์สเตจการ์ดหลัก
        if response["action"] == "display_all":
            info = response["drive_data"]
        else:
            info = None
    else:
        # กรณีไดรฟ์ D รันดึงแค่ค่าพื้นฐานปกติ
        res = process_central_command("scan d")
        info = res.get("data") if res["action"] == "display_base_drive" else None
    
    if info:
        base_text = f"--- 📊 ผลการสแกนคอมพิวเตอร์ Drive {info['drive']} ---\n"
        base_text += f"ภาพรวมดิส:     {info['progress_bar']}\n"
        base_text += f"กำลังใช้งาน:    {info['used']}\n"
        base_text += f"พื้นที่คงเหลือ:   {info['free']}\n"
        base_text += f"ความจุสูงสุด:   {info['total']}\n"
        base_text += "==============================================\n"
        
        view = DeepPathSelectionView(selected_drive=info['drive'])
        
        await interaction.followup.send(
            content=f"```text\n{base_text}```\n🔘 **[Stage 3]** โปรดเลือกพาร์ทที่ต้องการดึงรายละเอียดเชิงลึกต่อด้านล่างนี้:",
            view=view,
            ephemeral=True
        )
    else:
        await interaction.followup.send(content=f"❌ ALERT: ไม่สามารถดึงข้อมูลโครงสร้างดิสก์ได้ในขณะนี้", ephemeral=True)

@tasks.loop(hours=24)
async def daily_auto_report():
    """ส่งผลสรุปความจุจัดเต็มมัดรวมลงแชนเนลเป้าหมายอัตโนมัติประจำวัน"""
    channel = bot.get_channel(REPORT_CHANNEL_ID)
    if channel:
        print("📢 [Daily Tasks] กำลังแผ่สถิติรายงานรอบวันลงแชนเนล Discord...")
        response = process_central_command("/all")
        if response["action"] == "display_all":
            drive = response["drive_data"]
            full_report = f"--- 📊 ผลการสแกนคอมพิวเตอร์ Drive {drive['drive']} ---\n"
            full_report += f"ภาพรวมดิส:     {drive['progress_bar']}\n"
            full_report += f"กำลังใช้งาน:    {drive['used']}\n"
            full_report += f"พื้นที่คงเหลือ:   {drive['free']}\n"
            full_report += f"ความจุสูงสุด:   {drive['total']}\n"
            full_report += "==============================================\n\n"
            
            # ส่งภาพรวมหลักก้อนแรกก่อน
            await channel.send(f"```text\n{full_report}```")
            
            # คลี่แบ่งส่งตารางแยกย่อยทีละข้อความเพื่อแก้ปัญหากล่องข้อความเต็ม
            parts = response["parts_data"]
            for key in ["local", "program_files", "program_files_x86"]:
                if key in parts:
                    part_report = format_single_path_text(parts[key])
                    await channel.send(f"```text\n{part_report}```")
# แปะต่อท้ายบรรทัดล่างสุดของไฟล์ app/interfaces/discord_ui.py

def launch_discord_interface():
    """ฟังก์ชันหลักสำหรับโหลดค่าความลับและปลุกบอทให้ขึ้นออนไลน์บนคลาวด์/โลคอล"""
    from dotenv import load_dotenv
    load_dotenv()
    bot.run(os.getenv("DISCORD_TOKEN"))
