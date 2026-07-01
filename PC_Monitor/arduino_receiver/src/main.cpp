#include <Arduino.h>
#include <Wire.h>
#include "SSD1306Ascii.h"
#include "SSD1306AsciiWire.h"

#define I2C_ADDRESS 0x3C

SSD1306AsciiWire oled;

const byte numChars = 180; // ขยายบัฟเฟอร์เพิ่มขึ้นเพื่อรองรับข้อความ 7 บรรทัด
char receivedChars[numChars];
boolean newData = false;
char lines[7][22]; // เปลี่ยนเป็นเก็บ 7 บรรทัด (ขนาดบรรทัดละ 21 ตัวอักษร + '\0')

void recvWithStartEndMarkers();
void showNewData();

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(400000L);

  // ตั้งค่าสำหรับจอ 1.3" ชิปจีน SH1106
  oled.begin(&SH1106_128x64, I2C_ADDRESS);
  oled.setFont(System5x7); 
  
  oled.clear();
  oled.println("Waiting Data...");
}

void loop() {
  recvWithStartEndMarkers();
  showNewData();
}

void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0';
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }
    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}

void showNewData() {
  if (newData == true) {
    memset(lines, 0, sizeof(lines));
    
    // แกะข้อมูลตัวแรก (TITLE)
    char *strtokIndx;
    strtokIndx = strtok(receivedChars, ",");
    if (strtokIndx != NULL) {
      strncpy(lines[0], strtokIndx, 21);
      lines[0][21] = '\0';
    }
    
    // วนลูปแกะข้อมูลที่เหลืออีก 6 บรรทัด (รวมในระบบเป็น 7 บรรทัดพอดี)
    for(int i = 1; i < 7; i++) { 
      strtokIndx = strtok(NULL, ",");
      if(strtokIndx != NULL) {
        strncpy(lines[i], strtokIndx, 21);
        lines[i][21] = '\0';
      } else {
        strcpy(lines[i], "");
      }
    }

    // --- แสดงผลบนหน้าจอ OLED พิมพ์ตรงๆ ชิปไม่เอ๋อ ---
    oled.home(); 
    
    // พิมพ์เรียงลงมาตามลำดับที่ส่งจาก Python ล็อคตำแหน่งเป๊ะๆ
    oled.print(lines[0]); oled.clearToEOL(); oled.println(); // บรรทัด 1: Title
    oled.print(lines[1]); oled.clearToEOL(); oled.println(); // บรรทัด 2: ว่าง
    oled.print(lines[2]); oled.clearToEOL(); oled.println(); // บรรทัด 3: CPU
    oled.print(lines[3]); oled.clearToEOL(); oled.println(); // บรรทัด 4: RAM
    oled.print(lines[4]); oled.clearToEOL(); oled.println(); // บรรทัด 5: GPU
    oled.print(lines[5]); oled.clearToEOL(); oled.println(); // บรรทัด 6: VRAM
    oled.print(lines[6]); oled.clearToEOL();                 // บรรทัด 7: DRIVE C
    
    newData = false;
  }
}