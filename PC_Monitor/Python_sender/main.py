import os
import time
import GPUtil
import psutil
import serial

# --- การตั้งค่าคอนฟิก ---
SERIAL_PORT = "COM4"  # เปลี่ยนให้ตรงกับพอร์ตของ Arduino Nano
BAUD_RATE = 115200
SCREEN_WIDTH = 21  # ความกว้างจอหลัก 21 ตัวอักษร


def format_boxed_line(label, value_percent):
    """บีบความกว้างเฉพาะกล่องข้อความลงเหลือ 19 ตัวอักษร เพื่อให้จอแสดงขอบขวา | ได้พอดี"""
    # โครงสร้าง: "  " (เว้นซ้าย 1 ช่องเพื่อให้กล่องอยู่กลาง) + "|" + เนื้อหา (15 ช่อง) + "|"
    # รวมความยาวบรรทัด: 1 + 1 + 15 + 1 = 18-19 ตัวอักษร (ไม่เกินขอบจอแน่นอน)
    
    # เนื้อหาด้านในกล่องกว้าง 15 ช่อง: ชื่อชิดซ้าย (7 ช่อง) + ตัวเลขชิดขวา (8 ช่อง)
    inner_content = f"{label:<7}{value_percent:>8.1f}%"
    
    return f" | {inner_content} |"


# รีเซ็ตค่าแรกของระบบ
psutil.cpu_percent(interval=None)

print(f"กำลังเชื่อมต่อกับ Arduino ที่พอร์ต {SERIAL_PORT} (เวอร์ชันปิดกรอบขวา)...")
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("เชื่อมต่อสำเร็จ! เริ่มส่งข้อมูล...")
except Exception as e:
    print(f"ไม่สามารถเชื่อมต่อ Serial Port ได้: {e}")
    exit()

try:
    while True:
        # 1. ดึงข้อมูลระบบ
        cpu_p = psutil.cpu_percent(interval=None)
        ram_p = psutil.virtual_memory().percent

        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_p = gpus[0].load * 100
            vram_p = (gpus[0].memoryUsed / gpus[0].memoryTotal) * 100
        else:
            gpu_p = 0.0
            vram_p = 0.0

        try:
            drive_c = psutil.disk_usage("C:")
            drive_c_p = drive_c.percent
        except:
            drive_c_p = 0.0

        # 2. จัดฟอร์แมตข้อความแบบหลบขอบจอ (ปิดกรอบซ้าย-ขวาได้ 100%)
        line_title = "==== SYS MONITOR ===="  # บรรทัดที่ 1 (21 ตัวอักษรเต็มจอ)
        line_top_border = " -------------------- "  # บรรทัดที่ 2 (ฝาปิดกล่องกว้าง 19 ช่อง)
        
        # บรรทัดที่ 3 - 7: ตีกรอบล้อมรอบ (แก้คำซ้ำจาก CPU เป็น GPU ให้แล้วครับ)
        line_cpu = format_boxed_line("CPU", cpu_p)
        line_ram = format_boxed_line("RAM", ram_p)
        line_gpu = format_boxed_line("GPU", gpu_p)    # แก้ไขตรงนี้ให้แสดง GPU ถูกต้อง
        line_vram = format_boxed_line("VRAM", vram_p)
        line_drive = format_boxed_line("DRIVE C", drive_c_p)

        # 3. ประกอบแพ็กเกจข้อมูลส่งไปหา Arduino
        packet = f"<{line_title},{line_top_border},{line_cpu},{line_ram},{line_gpu},{line_vram},{line_drive}>\n"
        ser.write(packet.encode("utf-8"))

        # แสดงผลจำลองบนหน้าจอคอมพิวเตอร์
        os.system("cls" if os.name == "nt" else "clear")
        print("Python Fixed Box-Border UI...")
        print(f"Raw Packet: {packet.strip()}")
        print("-" * 30)
        print(f"{line_title}")
        print(f"{line_top_border}")
        print(f"{line_cpu}")
        print(f"{line_ram}")
        print(f"{line_gpu}")
        print(f"{line_vram}")
        print(f"{line_drive}")
        print("-" * 30)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nปิดโปรแกรมคอมพิวเตอร์")
    ser.close()