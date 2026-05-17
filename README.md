# 🎙️ miclink — ไมค์มือถือ ใช้บน PC แบบไร้สาย

> เปลี่ยน iPad / iPhone / Android ให้เป็นไมโครโฟนคุณภาพสูงสำหรับ Discord, OBS, Zoom โดยไม่ต้องซื้ออุปกรณ์เพิ่มเลยสักบาท

```
ไมค์ iPad → Browser → WebSocket → Python Server → VB-Cable → Discord/OBS/Zoom
```

---

## เกิดมาได้ยังไง? (Origin Story)

เพื่อนก็รู้ว่าเวลาคุย Discord หรืออัดเสียง แล้วไมค์คอมไม่ดีหรือลืมเอาไมค์มา — แต่เรามี **iPad หรือมือถือ** อยู่แล้ว และไมค์ของพวกนี้คุณภาพดีมาก! (48kHz 16-bit = ระดับสตูดิโอ)

ปัญหาคือ:
❌ ซื้ออุปกรณ์ capture การ์ด = แพง  
❌ สายยาวเกะกะ  
❌ App ที่มีใน App Store ก็ต้องเสียเงิน  

**miclink** เลยเกิดมาเพื่อแก้ปัญหานี้ — ใช้แค่ **Wi-Fi + Web browser** ก็ใช้ไมค์มือถือบน PC ได้แล้ว!

---

## Tech Stack — ใช้ตัวไหนทำอะไร

### ภาพรวม Architecture

```
┌──────────────────────┐         WebSocket          ┌──────────────────────┐
│  iPad / มือถือ        │  ◄────────────────────►   │  Windows PC          │
│                      │     ws://192.168.x.x:8765  │                      │
│  Safari/Chrome       │          เสียง PCM16        │  Python Server       │
│  (getUserMedia API)  │                             │  (audio-server.py)   │
│                      │                             │         ↓            │
│  จับเสียงจากไมค์       │                             │  PyAudio → VB-Cable  │
│  → ส่ง raw audio      │                             │         ↓            │
│  → แบบ real-time      │                             │  Discord / OBS / Zoom│
└──────────────────────┘                             └──────────────────────┘
```

### 1. 🧩 ฝั่ง Client — Browser (iPad / มือถือ)

**เทคโนโลยี:** `getUserMedia` API + JavaScript WebSocket

เป็น API ที่ Browser มีอยู่แล้วในตัว — **ไม่ต้องติดตั้งแอปเพิ่ม!**

- เปิด Safari/Chrome → เข้า URL `http://<IP>:8000/web-client.html`
- Browser ถามขอใช้ไมค์ → กด Allow
- JavaScript ใช้ `navigator.mediaDevices.getUserMedia()` เพื่อดึงเสียงสดจากไมค์
- แปลงเสียงเป็น Raw PCM16 (เสียงที่ไม่บีบอัด) → ส่งผ่าน WebSocket ไปหา Server

> **ทำไมไม่บีบอัด?** เพราะเราอยากให้ **หน่วงน้อยที่สุด** — ถ้าบีบอัด (mp3/opus) จะช้าลงเพราะต้องรอ encode/decode

### 2. 🌐 ช่องทางส่งข้อมูล — WebSocket

**เทคโนโลยี:** `websockets` (Python library)

WebSocket เหมือน **ท่อส่งข้อมูลที่เปิดตลอดเวลา** — ไม่ต้องโทรหากันใหม่ทุกครั้ง เหมาะกับเสียงแบบ real-time มากกว่า HTTP ทั่วไป

- เปิด connection ครั้งเดียว
- ข้อมูลไหลตลอดจนกว่าจะปิด
- หน่วงต่ำมาก (real-time)

### 3. 🐍 ฝั่ง Server — Python

**เทคโนโลยี:** Python 3.10+ + `PyAudio` + `python-dotenv`

Server เป็นตัวกลางรับเสียงจากมือถือ แล้วส่งเข้าคอม:

1. `python-dotenv` — อ่านค่า config จาก `.env` (Port, Device ฯลฯ)
2. `websockets.serve()` — สร้าง WebSocket server รอรับ connection
3. พอมือถือต่อมา → server รับ raw audio bytes
4. ส่งต่อไปยัง `PyAudio` stream → เล่นเสียงออก VB-Cable

**ทำไมถึงใช้ Python?**
- เขียนง่าย อ่านเข้าใจได้
- PyAudio = ตัวต่อเสียงมาตรฐานของ Python
- ใช้ Library น้อยมาก แค่ 3 ตัว — ไม่มี external dependencies เยอะ
- Debug ง่าย (แก้ไข code แล้วรันใหม่ได้ทันที ไม่ต้อง compile)

### 4. 🔌 ตัวเชื่อมต่อ — VB-Cable

**เทคโนโลยี:** [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) (ฟรี)

VB-Cable เป็นโปรแกรมที่ **จำลองการ์ดเสียงเสมือน** — ทำให้ Windows คิดว่ามีไมโครโฟนตัวใหม่เสียบอยู่

- ติดตั้งครั้งเดียว
- Restart คอมครั้งเดียว
- หลัง Restart → ใน Discord/OBS/Zoom จะเห็น **"CABLE Input"** เป็นตัวเลือกไมค์
- Server ส่งเสียงไปที่ "CABLE Output" → ข้อมูลวิ่งผ่านสายเสมือน → ออกที่ "CABLE Input" → App เห็นเป็นไมค์

---

## ไฟล์ในโปรเจกต์ — เอาไว้ทำอะไร

| ไฟล์ | ภาษาที่ใช้ | เอาไว้ทำอะไร |
|------|-----------|-------------|
| `audio-server.py` | 🐍 Python (163 บรรทัด) | ตัว server หลัก — รับ WebSocket → ส่งเสียงเข้า VB-Cable |
| `web-client.html` | 🌐 HTML + JS (1 ไฟล์) | หน้าเว็บสำหรับเปิดบนมือถือ — จับไมค์ → ส่ง WebSocket |
| `requirements.txt` | 📦 pip list | รายการ library ที่ต้องลง (websockets, pyaudio, python-dotenv) |
| `.env` | 🔧 Config | ตั้งค่าต่าง ๆ — port, device, sample rate |
| `GUIDE.md` | 📘 คู่มือ | คู่มือภาษาไทยฉบับละเอียด (คนไม่เขียนโปรแกรมก็อ่านได้) |

---

## การพัฒนาที่ผ่านมา (Development Journey)

```
Phase 1 — Scaffold (commit 1)
├── ✅ audio-server.py + web-client.html พร้อมใช้งาน
├── ✅ โครงสร้างพื้นฐาน: WebSocket → PyAudio → VB-Cable
└── ✅ README.md ภาษาอังกฤษ

Phase 2 — Production Hardening (commit 2-3)
├── ✅ .env config — ไม่ต้องแก้ code เวลาเปลี่ยน port/device
├── ✅ python-dotenv — โหลดค่าจาก .env อัตโนมัติ
├── ✅ Auto-detect VB-Cable — ใส่ชื่อ device ใน .env ก็หาให้
├── ✅ --host / --port / --device CLI ยัง override .env ได้
├── ✅ Fix: Windows signal handler bug (add_signal_handler ไม่ support บน Windows)
├── ✅ .env → .gitignore (ป้องกัน secret รั่วไหล)
├── ✅ GUIDE.md — คู่มือภาษาไทย 12 หมวด
└── ✅ README.md ภาษาไทย — อันนี้แหละ!
```

---

## วิธีรัน (ฉบับย่อ)

### 1. ติดตั้ง VB-Cable
- ดาวน์โหลดฟรี → https://vb-audio.com/Cable/
- **ต้อง Restart คอมหลังติดตั้ง!**

### 2. ลง Python dependencies
```cmd
pip install -r requirements.txt
```

### 3. ตั้งค่า .env (ใช้ Notepad ก็ได้)
เปิด `.env` → เช็คว่า `DEVICE_NAME=CABLE Output`

### 4. รัน Server
```cmd
python audio-server.py
```

### 5. เปิดหน้าเว็บบนมือถือ
```cmd
python -m http.server 8000
```
แล้วเปิด Safari ที่ iPad → `http://<IP>:8000/web-client.html`

### 6. ใช้ใน Discord
- Settings → Voice & Video → Input Device → **CABLE Input**

> **คู่มือละเอียดมากอยู่ที่ `GUIDE.md` น้าา — มี troubleshooting ครบ!**

---

## Commands ที่ใช้บ่อย

| คำสั่ง | ทำอะไร |
|-------|--------|
| `python audio-server.py` | รัน server (ใช้ค่าใน .env) |
| `python audio-server.py --port 9000` | รันด้วย port อื่น |
| `python audio-server.py --list-devices` | ดูรายการอุปกรณ์เสียงที่มี |
| `python audio-server.py --find-device "CABLE"` | หา CABLE device index |

---

## License

MIT — ทำอะไรก็ได้ตามสบาย 😊
