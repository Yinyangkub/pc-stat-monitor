# PC Hardware Status Monitor 🖥️

A real-time PC hardware status monitor that fetches system metrics (CPU, RAM, GPU, VRAM, and Disk Usage) using **Python** and transmits the data via USB (Serial Communication) to an **Arduino Nano**. The microcontroller parses the incoming stream and drives a **1.3" OLED Display (SH1106 chip)** via I2C connection.

## 🚀 Features
- Monitors 5 core system metrics: CPU (%), RAM (%), GPU (%), VRAM (%), and Disk Drive C (%).
- Features a clean, boxed-line UI layout with fixed character constraints to perfectly fit the screen without wrapping or overflow.
- Optimized for low memory consumption on Arduino using the `SSD1306Ascii` library for ultra-fast text rendering.
- Implements robust Serial data packet framing using Start/End Markers (`< >`) and tokenization to prevent data loss or corruption.

## 🛠️ Hardware Components
- **Arduino Nano** (or any compatible AVR microcontroller)
- **1.3" SH1106 OLED Display** connected via I2C (Default Address: `0x3C`)
- USB Cable (for connecting the PC to the Arduino Nano)

## 📂 Project Structure
- `PC_Monitor/Python_sender/main.py` : Python script responsible for collecting system statistics and transmitting them over the Serial port (Baud rate: 115200).
- `PC_Monitor/arduino_receiver/src/main.cpp` : Arduino C++ source code developed using PlatformIO, handling incoming string tokenization via `strtok` and OLED rendering.
- `PC_Monitor/arduino_receiver/platformio.ini` : PlatformIO configuration file for board management and dependency tracking.

## 📦 Dependencies
### Python:
- `psutil` (System monitoring library)
- `GPUtil` (GPU status utility)
- `pyserial` (Serial communication interface)

### Arduino (VS Code / PlatformIO):
- `Wire.h` (Built-in I2C communication library)
- `SSD1306Ascii.h` & `SSD1306AsciiWire.h` (High-speed text-only OLED library)
