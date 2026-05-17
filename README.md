# 🎙️ miclink — ไมค์มือถือ ใช้บน PC แบบไร้สาย

> เปลี่ยน iPad / iPhone / Android ให้เป็นไมโครโฟนคุณภาพสูงสำหรับ Discord, OBS, Zoom โดยไม่ต้องซื้ออุปกรณ์เพิ่มเลยสักบาท
>
> ✅ **รองรับ iOS แล้ว!** — ต้องเปิดด้วย `--secure` mode (HTTPS + WSS) เท่านั้น

```
ไมค์ iPad → Safari → WebSocket (WSS) → Python Server → VB-Cable → Discord/OBS/Zoom
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

### ภาพรวม Architecture (ปัจจุบัน)

```
┌──────────────────────┐       WebSocket (WSS)        ┌──────────────────────────────┐
│  iPad / มือถือ        │  ◄────────────────────►     │  Windows PC                  │
│                      │     wss://IP:8443             │                              │
│  Safari/Chrome       │          เสียง PCM16 mono     │  Python Server (audio-server)│
│  (getUserMedia API)  │                               │  (port 8443 — all-in-one)    │
│                      │                               │                              │
│  จับเสียงจากไมค์       │                               │  mono → stereo convert      │
│  → ScriptProcessor    │                               │  + gain boost               │
│  → ส่ง raw PCM16      │                               │  → PyAudio → VB-Cable       │
│  → real-time          │                               │       → Discord / OBS / Zoom│
└──────────────────────┘                               └──────────────────────────────┘
```

### 1. 🧩 ฝั่ง Client — Browser (iPad / มือถือ)

**เทคโนโลยี:** `getUserMedia` + ScriptProcessorNode + WebSocket

- เปิด Safari → เข้า URL `https://<IP>:8443/web-client.html`
- Browser ถามขอใช้ไมค์ → กด Allow
- แปลง Float32 เป็น Int16 → ส่งผ่าน WebSocket

> **ทำไมไม่บีบอัด?** เพราะอยากให้ **หน่วงน้อยที่สุด + คุณภาพ lossless** — miclink ใช้ raw PCM16 ที่ 768 kbps

### 2. 🌐 ช่องทางส่งข้อมูล — WebSocket (WSS)

**เทคโนโลยี:** `websockets` v16 (Python library)

- ปัจจุบัน HTTP + WSS **ใช้ port 8443 เดียวกัน** (iOS cert trust ไม่แยก per-port)
- ใน --secure mode ทุกอย่าง run on same port

### 3. 🐍 ฝั่ง Server — Python

**เทคโนโลยี:** Python 3.10+ + PyAudio + websockets + python-dotenv

Server ทำหน้าที่:
1. รับ audio จาก WebSocket (PCM16 mono)
2. **Mono → Stereo** (VB-Cable ต้อง stereo ถึงจะชัด)
3. **Gain boost** (default 3.0x — แก้ปัญหา iPad mic quiet)
4. ส่งไปยัง PyAudio stream → VB-Cable

### 4. 🔌 ตัวเชื่อมต่อ — VB-Cable

[VB-Audio Virtual Cable](https://vb-audio.com/Cable/) (ฟรี)

> **Device Index:** `27` — CABLE Input (VB-Audio Virtual Cable) @ 48000Hz

---

## ไฟล์ในโปรเจกต์

| ไฟล์ | คำอธิบาย |
|------|---------|
| `audio-server.py` | Server หลัก — WebSocket + PyAudio + HTTPS/WSS on single port |
| `web-client.html` | หน้าเว็บสำหรับเปิดบนมือถือ |
| `test-pyaudio.py` | Test PyAudio playback (sine wave / WAV file) |
| `diagnostic.html` | Diagnostic tool สำหรับ ScriptProcessorNode |
| `certs/gen-cert.py` | สร้าง self-signed cert สำหรับ secure mode |
| `GUIDE.md` | คู่มือภาษาไทยฉบับละเอียด |
| `requirements.txt` | websockets, pyaudio, python-dotenv |

---

## วิธีรัน (iOS / Secure Mode)

### 1. ติดตั้ง VB-Cable
- https://vb-audio.com/Cable/ → **ต้อง Restart คอมหลังติดตั้ง!**

### 2. ลง Python dependencies
```cmd
pip install -r requirements.txt
```

### 3. สร้าง Certificate (ครั้งแรกครั้งเดียว)
```cmd
python certs/gen-cert.py
```

### 4. รัน Server
```cmd
python audio-server.py --secure --device 27 --gain 3.0
```

### 5. เปิดบน iPad
`https://172.20.10.2:8443/web-client.html` → ใส่ IP → Start

### 6. ใช้ใน Discord
Settings → Voice & Video → Input Device → **CABLE Input (VB-Audio Virtual Cable)**

---

## Commands ที่ใช้บ่อย

| คำสั่ง | ทำอะไร |
|-------|--------|
| `python audio-server.py --secure --device 27` | รัน secure mode (iOS) |
| `python audio-server.py --secure --device 27 --gain 4.0` | เพิ่ม gain ถ้าเสียงเบา |
| `python audio-server.py --secure --device 27 --record diag.wav` | บันทึกเสียงลง WAV |
| `python audio-server.py --list-devices` | ดูอุปกรณ์เสียงทั้งหมด |
| `python test-pyaudio.py` | ทดสอบ PyAudio กับ default output |
| `python test-pyaudio.py --device 27` | ทดสอบกับ VB-Cable |
| `python test-pyaudio.py --play diag.wav` | เล่นไฟล์ WAV ที่บันทึกไว้ |

---

## ปัญหาที่เจอและแก้แล้ว

| ปัญหา | อาการ | วิธีแก้ |
|-------|-------|--------|
| iOS mic pop-up ไม่ขึ้น | HTTP → getUserMedia ไม่ได้ | ใช้ `--secure` (HTTPS) |
| cert trust per-port | หน้าเว็บ open แต่ WebSocket fail | รวม HTTP+WSS port 8443 เดียว |
| streaming @ 0.0 kbps | iPad connect แต่ไม่มี data | เพิ่ม GainNode(0) ใน audio graph |
| Audio garbled | iOS ScriptProcessor data เสีย | Set onaudioprocess ก่อน connect graph |
| VB-Cable mono = แตก | ส่ง mono แล้วเสียงแตก | ส่ง stereo (L/R duplicate) |
| เสียงเบามาก | iPad mic raw level ต่ำ | `autoGainControl: true` + `--gain 3.0` |

> **รายละเอียดทั้งหมด + Technical Notes อยู่ใน** `knowledge/miclink/01-debugging-journey.md` (Obsidian vault)

---

## License

MIT — ทำอะไรก็ได้ตามสบาย 😊
