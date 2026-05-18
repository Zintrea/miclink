# 🎙️ miclink — คู่มือการใช้งาน (ฉบับละเอียด)

**เวอร์ชัน:** 2.0.0  
**อัปเดตล่าสุด:** 18 พฤษภาคม 2569  
**ผู้จัดทำ:** Iris for Bai

> 📝 **อัปเดต 2.0.0:** --secure mode ใช้ single port (8443), mono→stereo conversion, --gain boost, websockets v16, test scripts, troubleshooting เพิ่มเติม

---

## สารบัญ

| หมวด | หัวข้อ |
|------|-------|
| [1](#1-miclink-คืออะไร) | miclink คืออะไร? |
| [2](#2-เทคโนโลยีที่ใช้) | เทคโนโลยีที่ใช้ |
| [3](#3-โครงสร้างไฟล์) | โครงสร้างไฟล์ |
| [4](#4-สิ่งที่ต้องมีก่อนรัน) | สิ่งที่ต้องมีก่อนรัน |
| [5](#5-การติดตั้ง) | การติดตั้ง |
| [6](#6-การตั้งค่า-env) | การตั้งค่า .env |
| [7](#7-การรัน-server) | การรัน Server |
| [8](#8-การเชื่อมต่อจาก-ipad-หรือมือถือ) | การเชื่อมต่อจาก iPad หรือมือถือ |
| [9](#9-การใช้งานกับ-discord-obs-หรือโปรแกรมอื่น) | การใช้งานกับ Discord / OBS หรือโปรแกรมอื่น |
| [10](#10-การปรับแต่ง) | การปรับแต่ง |
| [11](#11-การแก้ไขปัญหา) | การแก้ไขปัญหา |
| [12](#12-อธิบายศัพท์เทคนิค-glossary) | อธิบายศัพท์เทคนิค (Glossary) |

---

## 1. miclink คืออะไร?

**miclink** เป็นโปรแกรมที่เปลี่ยนคอมพิวเตอร์ Windows ของคุณให้เป็น ** receiver ไมโครโฟนแบบไร้สาย** 🎤

คุณสามารถ:
- ใช้ไมโครโฟนของ **iPad / iPhone / Android** มาพูดผ่านลำโพงคอม
- ใช้ไมโครโฟนมือถือเป็นไมค์คุยใน **Discord, Zoom, OBS, หรือโปรแกรมอะไรก็ได้**
- **เสียงคมชัด** 48kHz PCM16 (คุณภาพเทียบเท่าสตูดิโอ)
- **หน่วงต่ำมาก** เหมาะสำหรับพูดคุย สตรีม หรืออัดเสียง

**วิธีการทำงาน:**
```
ไมค์ iPad → Safari/Chrome → สัญญาณเสียง (WebSocket) → Python Server → VB-Cable → Discord/OBS/โปรแกรมอะไรก็ได้
```

---

## 2. เทคโนโลยีที่ใช้

| เทคโนโลยี | ใช้ทำอะไร | เปรียบเทียบกับของใกล้ตัว |
|-----------|----------|------------------------|
| **Python 3.10+** | ภาษาโปรแกรมที่ใช้เขียนตัว server | เหมือนเครื่องยนต์ของรถ |
| **WebSocket** | ช่องทางส่งข้อมูลเสียงแบบ real-time ระหว่างมือถือกับคอม | เหมือนสายยางส่งน้ำ — ข้อมูลไหลต่อเนื่องตลอดเวลา |
| **PyAudio** | ตัวกลางให้ Python ส่งเสียงออกไปยังลำโพงหรือ VB-Cable | เหมือนท่อต่อจากคอมไปหูฟัง |
| **VB-Cable** | สายเสียงเสมือน — ทำให้คอมคิดว่ามีไมโครโฟนตัวใหม่เสียบอยู่ | เหมือนสาย HDMI ปลอมที่หลอกคอมว่า "นี่คือไมค์" |
| **VB-Cable (สองทิศทาง)** | ฝั่ง Playback: `CABLE Input` = ที่ server ส่งเสียงไป<br>ฝั่ง Recording: `CABLE Input` = ที่ Discord/OBS อ่านเสียงมา | เหมือนท่อสองหัว — ด้านนึงเป่าเข้า อีกด้านลมออก |
| **python-dotenv** | อ่านค่าตั้งค่าจากไฟล์ `.env` | เหมือนสมุดโน้ตที่บอก server ว่าควรใช้ port อะไร, device อะไร |
| **pydub / PCM16** | รูปแบบเสียงดิจิตอลที่ไม่บีบอัด คุณภาพสูง | เหมือนไฟล์ WAV เทียบกับ MP3 — ใหญ่กว่าแต่ชัดเจนกว่า |

---

## 3. โครงสร้างไฟล์

```
📁 miclink/
├── 📄 audio-server.py      ← ตัว server หลัก (ไฟล์ที่รัน)
├── 📄 web-client.html       ← หน้าเว็บสำหรับเปิดบนมือถือ
├── 📄 README.md             ← คำอธิบายโปรเจกต์แบบสั้น
├── 📄 requirements.txt      ← รายการ dependencies ที่ต้องติดตั้ง
├── 📄 .env                  ← ค่าตั้งค่าต่าง ๆ (Port, Device, ฯลฯ)
├── 📄 .gitignore            ← บอก Git ว่าไม่ต้อง Track ไฟล์อะไรบ้าง
├──
├── 📁 docs/                 ← เอกสารทั้งหมด
│   ├── 📄 GUIDE.md          ← คู่มือนี้ (ที่คุณกำลังอ่าน)
│   ├── 📄 DEVELOP.md        ← เรื่องราวการพัฒนา
│   └── 📄 KNOWLEDGE.md      ← ความรู้เทคนิค
│
├── 📁 debug/                ← เครื่องมือทดสอบและ debug
│   ├── 📄 diagnostic.html   ← หน้าทดสอบ ScriptProcessorNode
│   ├── 📄 test-pyaudio.py   ← ทดสอบ PyAudio playback
│   ├── 📄 stereo-test.py    ← ทดสอบ mono vs stereo
│   └── 📄 rate-test.py      ← ทดสอบ sample rate
│
├── 📁 certs/                ← ใบรับรอง SSL (สร้างครั้งแรกด้วย gen-cert.py)
│
└── 📁 .git/                 ← โฟลเดอร์ของ Git (ไม่ต้องแตะ)
```

### อธิบายแต่ละไฟล์

| ไฟล์ | เอาไว้ทำอะไร | ต้องแก้ไหม? |
|------|-------------|------------|
| `audio-server.py` | ตัว server หลัก — ฟัง WebSocket แล้วส่งเสียงออก VB-Cable | ❌ ไม่ต้องแก้ (เว้นแต่จะแก้บั๊ก) |
| `web-client.html` | หน้าเว็บที่เปิดบน iPad/มือถือเพื่อส่งเสียงมา | ❌ ไม่ต้องแก้ |
| `requirements.txt` | รายการ Python package ที่ต้อง `pip install` | ❌ ไม่ต้องแก้ |
| `.env` | ตั้งค่าต่าง ๆ เช่น Port, Device | ✅ **ต้องแก้** ให้ตรงกับเครื่องคุณ |
| `.gitignore` | บอก Git ว่าไม่ต้องอัปโหลดไฟล์อะไร (เช่น `.env`) | ❌ ไม่ต้องแก้ |
| `README.md` | คำอธิบายสั้น ๆ สำหรับคนเปิด GitHub เจอ | ❌ ไม่ต้องแก้ |
| `docs/` | โฟลเดอร์รวมเอกสาร (GUIDE.md, DEVELOP.md, KNOWLEDGE.md) | ❌ ไม่ต้องแก้ |
| `debug/` | โฟลเดอร์รวมเครื่องมือทดสอบและ debug | ❌ ไม่ต้องแก้ |

---

## 4. สิ่งที่ต้องมีก่อนรัน

ก่อนจะใช้ miclink ได้ คุณต้องมีสิ่งเหล่านี้:

### 4.1 คอมพิวเตอร์ Windows

- ✅ Windows 10 หรือ 11
- ✅ Python 3.10 หรือสูงกว่า (เช็คโดยพิมพ์ `python --version` ใน Command Prompt)
- ✅ มี Wi-Fi หรือ สายแลน (คอมกับมือถือต้องอยู่เครือข่ายเดียวกัน)

### 4.2 VB-Cable (สำคัญมาก!)

VB-Cable เป็นโปรแกรมจำลองสายเสียง ที่ทำให้ Discord/OBS คิดว่าคุณมีไมโครโฟนตัวใหม่เสียบอยู่

**VB-Cable มี 2 ด้านให้เข้าใจ:**

```
┌──────────────────────────────────────────────┐
│              VB-Cable (สายเสียงเสมือน)          │
│                                              │
│  🎯 ด้าน Playback (ส่งเสียงเข้า)               │
│      ชื่อ: "CABLE Input" (ใน list device)     │
│      ← Server ของเราส่งเสียงมาตรงนี้           │
│                                              │
│      ════ สายเดินผ่านด้านใน ════               │
│                                              │
│  🎤 ด้าน Recording (อ่านเสียงออก)              │
│      ชื่อ: "CABLE Input" (ใน Discord/OBS)     │
│      → Discord/OBS อ่านเสียงจากตรงนี้          │
└──────────────────────────────────────────────┘
```

> 🤔 **ชื่ออาจดูงง:** ใน PyAudio device list จะเห็น "CABLE Input" โผล่ในหมวด Output devices — นั่นคือ **ด้าน Playback** ที่ server ใช้ส่งเสียงเข้านะคะ
> ส่วนด้าน Recording (ที่ Discord/OBS อ่าน) จะเห็นชื่อ "CABLE Input" เหมือนกัน แต่อยู่คนละที่กัน

**วิธีติดตั้ง VB-Cable:**
1. เปิดเว็บ https://vb-audio.com/Cable/
2. กดปุ่ม **Download** (ตัวฟรีก็ใช้ได้ ไม่ต้องเสียเงิน)
3. เปิดไฟล์ที่โหลดมา แล้วกด **Install** (หรือ Next → Next → Install)
4. ⚠️ **ต้อง Restart คอม** หลังติดตั้ง!
5. หลัง Restart แล้ว — ทดสอบโดยรัน `python audio-server.py --list-devices` ถ้าเห็นคำว่า `CABLE` แสดงว่าติดตั้งสำเร็จ!

> 💡 ไม่ต้องกลัว — VB-Cable ปลอดภัย ใช้กันทั่วโลก ไม่มีไวรัส

### 4.3 iPad / iPhone / Android

- ✅ เชื่อมต่อ Wi-Fi **เครื่องเดียวกับคอม**
- ✅ มี Browser (Safari สำหรับ iPad/iPhone, Chrome สำหรับ Android)

---

## 5. การติดตั้ง

### 5.1 ติดตั้ง Python dependencies

เปิด **Command Prompt** หรือ **Terminal** แล้วพิมพ์:

```cmd
cd C:\Host\02 Projects\08 miclink
pip install -r requirements.txt
```

รอจนกว่าจะขึ้นว่า `Successfully installed` ทั้ง 3 ตัว:
- `websockets`
- `pyaudio`
- `python-dotenv`

> ⚠️ ถ้าเจอ error เกี่ยวกับ `pip` ไม่รู้จัก ให้ลองใช้ `python -m pip install -r requirements.txt` แทน

### 5.2 ตรวจสอบว่าไฟล์ครบ

ในโฟลเดอร์ `C:\Host\02 Projects\08 miclink\` ต้องมีไฟล์เหล่านี้:

```
✅ audio-server.py
✅ web-client.html
✅ requirements.txt
✅ .env
```

---

## 6. การตั้งค่า .env

เปิดไฟล์ `.env` (ใช้ Notepad ก็ได้) แล้วปรับค่าตามนี้:

```ini
# --- WebSocket Server ---
HOST=0.0.0.0
PORT=8765

# --- Audio Settings ---
SAMPLE_RATE=48000
CHANNELS=1
CHUNK_SIZE=2048

# --- VB-Cable Device ---
DEVICE_INDEX=
DEVICE_NAME=CABLE Output
```

### อธิบายแต่ละตัวแปร

| ตัวแปร | ค่าปกติ | ความหมาย | ควรเปลี่ยนไหม? |
|--------|---------|---------|--------------|
| `HOST` | `0.0.0.0` | IP ที่ server ฟังอยู่ — `0.0.0.0` = ฟังทุกช่องทาง | ❌ ไม่ต้องเปลี่ยน |
| `PORT` | `8765` | พอร์ต WebSocket ถ้าชนกับโปรแกรมอื่นก็เปลี่ยนได้ | 🔄 เปลี่ยนได้ถ้าจำเป็น |
| `SAMPLE_RATE` | `48000` | คุณภาพเสียง 48000 Hz = ระดับสตูดิโอ | ❌ ไม่ต้องเปลี่ยน |
| `CHANNELS` | `1` | 1 = Mono เสียงเดียว เหมาะกับไมค์ | ❌ ไม่ต้องเปลี่ยน |
| `CHUNK_SIZE` | `2048` | ขนาดบัฟเฟอร์ — ยิ่งสูง = เสียงคงที่แต่หน่วงขึ้น, ยิ่งต่ำ = หน่วงน้อยแต่กระตุกง่าย | 🔄 เปลี่ยนได้ถ้าเสียงกระตุก |
| `DEVICE_INDEX` | `27` | **เลข index** ของอุปกรณ์ที่ server จะส่งเสียงออกไป | ✅ **สำคัญ! ต้องตั้งให้ถูก** |
| `DEVICE_NAME` | *(ว่าง)* | ชื่ออุปกรณ์ ให้ server หาอัตโนมัติ (ถ้าไม่ใช้ DEVICE_INDEX) | 🔄 ใช้แทน DEVICE_INDEX ก็ได้ |

---

### วิธีหา DEVICE_INDEX ที่ถูกต้อง (สำคัญที่สุด!)

server ของเราต้อง **ส่งเสียงออกไป** (playback/output) ยังอุปกรณ์ที่ต่อกับ VB-Cable
ดังนั้นเราต้องดูว่า device ตัวไหนคือ **VB-Cable ด้าน Playback**

เปิด Command Prompt แล้วรัน:

```cmd
cd C:\Host\02 Projects\08 miclink
python audio-server.py --list-devices
```

คุณจะเห็น device list เยอะมาก — **ไม่ต้องตกใจ!** มีวิธีเลือกง่าย ๆ ค่ะ

### วิธีเลือก: มองหาคำว่า "CABLE" และ 48000 Hz

จาก device list จริงของ Bai ค่ะ (18 พ.ค. 2569):

```
  [6]  Microsoft Sound Mapper - Output                    ← ❌ ไม่เกี่ยวกับ CABLE
  [7]  Speakers (AB13X USB Audio)                         ← ❌ ลำโพง USB
  [8]  Speakers (NVIDIA Broadcast)                        ← ❌ NVIDIA
  [9]  CABLE In 16ch (VB-Audio Virtual (...)              ← 🔍 44100 Hz
  [10] CABLE Input (VB-Audio Virtual C (...)               ← 🔍 44100 Hz, 16 ch
  [11] Speaker (Realtek(R) Audio)                         ← ❌ ลำโพง onboard
  ... (อุปกรณ์อื่น ๆ ที่ไม่เกี่ยวกับ CABLE)
  [26] CABLE In 16ch (VB-Audio Virtual Cable) (2 ch, 48000 Hz)  ← 🔍 48000 Hz
  [27] CABLE Input (VB-Audio Virtual Cable) (2 ch, 48000 Hz)     ← ✅ ตัวนี้!
  [28] Speaker (Realtek(R) Audio) (2 ch, 48000 Hz)              ← ❌
  ... (NVIDIA, Headphones, Bluetooth ฯลฯ)
```

**ขั้นตอนการเลือก:**

#### 👉 ขั้นที่ 1: หาเฉพาะตัวที่ขึ้นต้นด้วย "CABLE"
จาก list ด้านบน CABLE มีอยู่ 6 ตัว: [9], [10], [21], [22], [26], [27]

#### 👉 ขั้นที่ 2: เลือกตัวที่ Sample Rate ตรงกับที่ตั้งไว้ใน `.env`
ใน `.env` เราตั้ง `SAMPLE_RATE=48000` ไว้
- [9], [10], [21], [22] → 44100 Hz ❌ ไม่ตรง
- [26] CABLE In 16ch → 48000 Hz ✅ แต่ชื่อ "In 16ch"
- **[27] CABLE Input → 48000 Hz ✅ ตรง!**

#### 👉 ขั้นที่ 3:ใช้ DEVICE_INDEX = 27
เปิด `.env` แล้วตั้ง:
```ini
DEVICE_INDEX=27
```

> **สรุป:** ใช้ index [27] เพราะเป็น CABLE Input ที่ 48000 Hz ตรงกับ SAMPLE_RATE ที่เราตั้งไว้พอดี!

---

### วิธีที่ 2: ใช้ DEVICE_NAME (auto-detect)

ถ้าไม่อยากจำเลข index ก็ใช้ชื่อแทนได้:
```ini
DEVICE_INDEX=
DEVICE_NAME=CABLE Input
```

⚠️ แต่ข้อเสีย: คำว่า "CABLE Input" อาจ match หลายตัว (44100 Hz ก่อน 48000 Hz) — ถ้า auto-detect แล้วได้ index ไม่ตรง ให้กลับไปใช้ `DEVICE_INDEX=27` แทนนะคะ

---

### สรุป: ใช้ตัวไหนดี?

| วิธี | ข้อดี | ข้อเสีย |
|------|------|--------|
| `DEVICE_INDEX=27` | แน่นอน เลือก device ที่ SAMPLE_RATE ตรงได้เป๊ะ | ถ้าเสียบอุปกรณ์ใหม่ index อาจเปลี่ยน |
| `DEVICE_NAME=CABLE Input` | ไม่ต้องจำเลข หาให้อัตโนมัติ | อาจ match ผิดตัวถ้ามีหลาย CABLE |

> 💡 **แนะนำ:** เริ่มจาก `DEVICE_INDEX=27` ก่อน แล้วถ้าต่อมา index เปลี่ยน (เช่น เสียบอุปกรณ์ใหม่) ค่อย改用 `DEVICE_NAME`

---

## 7. การรัน Server

### 7.1 รันแบบปกติ (ใช้ค่าใน .env)

เปิด Command Prompt แล้วพิมพ์:

```cmd
cd C:\Host\02 Projects\08 miclink
python audio-server.py
```

คุณจะเห็นข้อความแบบนี้ (โดยใช้ `DEVICE_INDEX=27` ของ Bai):

```
==================================================
  🎙️  miclink — High-Quality Audio Server
==================================================
  Host: 0.0.0.0
  Port: 8765
  Audio: 48000 Hz, 1 ch, PCM16
  Output device: [27] CABLE Input (VB-Audio Virtual Cable)
  Stream ready — waiting for connections...

  🌐 WebSocket: ws://0.0.0.0:8765
  💡 Open web-client.html on your iPad/phone and connect!
```

> ✅ ถ้าขึ้น `Output device: [27] CABLE Input` แปลว่า server กำลังส่งเสียงไปยัง VB-Cable ถูกต้องแล้ว!

🎉 **แสดงว่า server พร้อมทำงานแล้ว!** อย่าปิดหน้าต่างนี้

### 7.2 รันแบบกำหนดค่าเอง (ไม่ใช้ .env)

```cmd
python audio-server.py --port 9000 --device 2
```

| คำสั่ง | ความหมาย |
|-------|---------|
| `--port 9000` | เปลี่ยนพอร์ตเป็น 9000 (แทน 8765) |
| `--device 2` | ใช้อุปกรณ์เสียง index 2 (แทนค่าใน .env) |
| `--list-devices` | แสดงรายการอุปกรณ์เสียงทั้งหมด |
| `--find-device "CABLE"` | ค้นหาอุปกรณ์ที่มีคำว่า CABLE แล้วบอก index |

> ⚠️ คำสั่ง `--port` หรือ `--device` จะ **แทนที่** ค่าใน `.env` เสมอ

### 7.3 วิธีปิด Server

กด `Ctrl + C` ในหน้าต่าง Command Prompt — server จะปิดเองอย่างเรียบร้อย

## 7.4 🔒 โหมด Secure (HTTPS + WSS) — ใช้กับ iOS โดยเฉพาะ

ถ้า `getUserMedia()` ไม่แสดง pop-up ให้ Allow ไมค์บน iPad (เพราะ iOS บังคับ HTTPS) — ให้ใช้โหมดนี้

### 7.4.1 Generate Certificate (ทำครั้งแรกครั้งเดียว)

```cmd
cd C:\Host\02 Projects\08 miclink
python certs\gen-cert.py
```

หรือ (WSL):
```bash
cd "/mnt/c/Host/02 Projects/08 miclink"
python3 certs/gen-cert.py
```

จะได้ไฟล์:
- `certs/server.pem` — ใช้เป็น SSL certificate + private key
- `certs/server.crt` — สำหรับติดตั้งบน iPad (ถ้าต้องการ)

### 7.4.2 รัน Server แบบ Secure

```cmd
python audio-server.py --secure
```

หรือรันพร้อมกำหนด device:
```cmd
python audio-server.py --secure --device 27
```

คุณจะเห็น:
```
  🔒 SSL: certs\server.pem
  🌍 HTTPS: https://0.0.0.0:8443/web-client.html
  🌐 WebSocket: wss://0.0.0.0:8765
```

### 7.4.3 เชื่อมต่อจาก iPad

1. บน iPad เปิด Safari → ไปที่ `https://172.20.10.2:8443/web-client.html`
2. Safari จะเตือนว่า certificate ไม่น่าเชื่อถือ (self-signed) — กด **Show Details**
3. กด **Visit This Website** (หรือ tap ลิงค์)
4. ใส่ IP: `172.20.10.2`
5. กด **Start Microphone**
6. ✅ **iOS ควรขึ้น pop-up ถาม Allow แล้ว!**

| ⚠️ คำเตือน cert warning จะขึ้นแค่ครั้งแรก หลังจาก accept แล้วจะไม่ขึ้นอีก

### 7.4.4 พอร์ตที่ใช้ (เปลี่ยนเป็น single port!)

| พอร์ต | โปรโตคอล | ใช้ทำอะไร |
|-------|----------|----------|
| **8443** | HTTPS + WSS | **ทุกอย่างในพอร์ตเดียว** — เปิดหน้าเว็บ + ส่งเสียง |

> **สำคัญ:** ปัจจุบัน HTTPS (web-client.html) และ WSS (audio streaming) **ใช้ port 8443 เดียวกัน** เพื่อแก้ปัญหา iOS Safari cert trust per-port — ถ้าแยก port กัน iOS จะไม่ trust cert ของ WSS port

> 💡 ถ้าพอร์ต 8443 ชนกับโปรแกรมอื่น ก็เปลี่ยนได้:
> `python audio-server.py --secure --https-port 9443`

### 7.4.5 ปรับ Gain (เพิ่มความดัง)

ถ้าเสียงจาก iPad เบาเกินไป ให้เพิ่ม gain:

```cmd
python audio-server.py --secure --device 27 --gain 3.0
```

| --gain | เหมาะกับ |
|--------|---------|
| 1.0 | เสียงปกติ ไม่ต้องเพิ่ม |
| 2.0 | เสียงเบานิดหน่อย |
| **3.0** | **default — iPad mic เงียบ** |
| 4.0 | เสียงเบามาก |
| 5.0 | เสียงเบาสุด (เสี่ยง clipping) |

> ระวัง — gain สูงเกินไป + input ดัง = clipping (เสียงแตก)

---

## 8. การเชื่อมต่อจาก iPad หรือมือถือ

### 8.1 หา IP Address ของคอม

เปิด Command Prompt แล้วพิมพ์:

```cmd
ipconfig
```

หาเส้นที่เขียนว่า **IPv4 Address** — มักเป็น `192.168.x.x` เช่น `192.168.1.100`

> หรืออีกวิธี: กด Wi-Fi icon → Properties → มองหา IPv4 address

### 8.2 เปิด web-client.html

ใน Command Prompt **อีกหน้าต่างนึง** (ไม่ต้องปิด server) พิมพ์:

```cmd
cd C:\Host\02 Projects\08 miclink
python -m http.server 8000
```

### 8.3 เชื่อมต่อจากมือถือ

1. บน iPad / iPhone / Android เปิด **Safari** (หรือ Chrome)
2. ไปที่ `http://<IP คอม>:8000/web-client.html`
   - ตัวอย่าง: `http://192.168.1.100:8000/web-client.html`
3. จะเห็นหน้าเว็บมีช่องให้ใส่ **Server Address**
4. ใส่ **IP Address ของคอม** เช่น: `172.20.10.2`
   - หรือใส่แบบมี port: `172.20.10.2:8765`
   - หรือใส่แบบ URL เต็ม: `ws://172.20.10.2:8765`
   - ✅ รับได้หมด!
5. ✅ ถ้าเชื่อมต่อสำเร็จ ปุ่มจะเปลี่ยนเป็น **Start Microphone** — กดเลย!
6. 😱 ระบบขออนุญาตใช้ไมค์ — กด **Allow**
7. พูดอะไรสักอย่าง — ถ้าเสียงออกลำโพงคอม แสดงว่าใช้ได้!

### 8.4 ใช้ใน Discord / OBS / Zoom (ขั้นตอนสำคัญ!)

หลังจาก server ทำงานและมือถือเชื่อมต่อแล้ว เสียงจากมือถือจะเดินทางผ่าน VB-Cable
แต่ **Discord/OBS/Zoom ยังไม่รู้** ว่าต้องใช้ไมค์ตัวไหน!

**วิธีตั้งค่า:**

#### ใน Discord:
1. เปิด Discord → ไปที่ **Settings** (รูปเฟือง ⚙️ มุมล่างซ้าย)
2. เลือกเมนู **Voice & Video** (เสียงและวิดีโอ)
3. หัวข้อ **Input Device** (อุปกรณ์นำเข้าเสียง) — คลิก dropdown
4. เลือก: **CABLE Input (VB-Audio Virtual Cable)**
5. พูดทดสอบ — ถ้าเห็นกรอบสีเขียวขยับ แสดงว่าใช้ได้! ✅

> ถ้าไม่เห็นกรอบเขียว → server ปิดอยู่ หรือมือถือยังไม่ได้กด Start Microphone

#### ใน OBS:
1. เปิด OBS → ไปที่ **Settings** (ปุ่ม Settings ล่างขวา)
2. เลือก **Audio**
3. หัวข้อ **Mic/Auxiliary Audio Device** → เลือก **CABLE Input**
4. ✅ เสร็จ!

#### ใน Zoom:
1. เปิด Zoom → คลิก **Settings** (รูปเฟือง) หรือเข้า **Audio** settings
2. หัวข้อ **Microphone** → เลือก **CABLE Input (VB-Audio Virtual Cable)**
3. ✅ เสร็จ!

### 8.5 ตรวจสอบว่าเสียงมาถึงคอมจริง (Troubleshooting Step)

ถ้าเซ็ตทุกอย่างแล้วแต่ยังไม่ได้ยินเสียง ให้เช็คตามนี้:

```mermaid
 flowchart LR
    A[มือถือกด<br>Start Mic?] -->|yes| B[Server<br>device index ถูก?]
    B -->|yes| C[VB-Cable<br>ติดตั้งถูก?]
    C -->|yes| D[Discord<br>เลือก CABLE Input?]
    D -->|yes| E[✅ ใช้ได้!]
```

| เช็ค | วิธีเช็ค |
|------|---------|
| 📱 มือถือต่อ WebSocket แล้ว? | ดูหน้า server — ต้องมีข้อความ `📱 Connected:` |
| 🐍 Server device index ถูก? | ดูตอนรัน server — ต้องขึ้น `Output device: [27] CABLE Input` |
| 🎤 Discord เลือก CABLE Input? | Discord Settings → Voice & Video → Input Device |
| 🔊 Speaker test | พูดใส่ iPad → ถ้าได้ยินเสียงตัวเอง แสดงว่าวงจรสมบูรณ์!

---

## 9. การปรับแต่ง

### 9.1 ปรับคุณภาพเสียง

แก้ `.env`:
```ini
CHUNK_SIZE=2048    ← ถ้าเสียงกระตุก ให้เพิ่มเป็น 4096 (แต่หน่วงขึ้น)
SAMPLE_RATE=48000  ← 48000 = ดีที่สุด, 44100 = ธรรมดา, 22050 = ต่ำ
```

### 9.2 เปลี่ยน Port

ถ้า Port 8765 ชนกับโปรแกรมอื่น:
```ini
PORT=9000
```

### 9.3 เปลี่ยน Output Device

ถ้าอยากให้เสียงออกลำโพง (ไม่ผ่าน VB-Cable):
```ini
DEVICE_NAME=
DEVICE_INDEX=
```

หรือให้ server หา device อัตโนมัติ:
```cmd
python audio-server.py --find-device "Speakers"
```

---

## 10. การแก้ไขปัญหา

| อาการ | สาเหตุ | วิธีแก้ |
|-------|--------|-------|
| ❌ `'pip' ไม่รู้จัก` | ยังไม่ได้ติดตั้ง Python หรือไม่ได้ Add to PATH | ติดตั้ง Python ใหม่ แล้วติ๊ก ✅ **Add Python to PATH** |
| ❌ `ModuleNotFoundError: No module named 'dotenv'` | ลืม `pip install python-dotenv` | รัน `pip install -r requirements.txt` |
| ❌ `OSError: [WinError - ใช้ VB-Cable ไม่ได้` | ยังไม่ได้ติดตั้ง VB-Cable หรือยังไม่ Restart | ติดตั้ง VB-Cable แล้ว **Restart คอม** |
| ❌ `Output device: [27] ไม่มีเสียง` | CABLE device 48000Hz ยังไม่พร้อม หรือ choice ผิด | ลอง `DEVICE_NAME=CABLE Input` หรือ `DEVICE_NAME=CABLE In 16ch` |
| ❌ `เชื่อมต่อจากมือถือไม่ได้` | คอมกับมือถือคนละ Wi-Fi | เช็คว่าทั้งสองเครื่องอยู่เครือข่ายเดียวกัน |
| ❌ `สะดุด / กระตุก` | WiFi ไม่เสถียร หรือ CHUNK_SIZE เล็กไป | ใช้ 5GHz WiFi หรือเพิ่ม `CHUNK_SIZE=4096` |
| ❌ `Discord ไม่เห็น CABLE Input` | (1) VB-Cable ไม่ได้ติดตั้ง<br>(2) ยังไม่ได้เลือกใน Discord Settings | (1) ติดตั้ง VB-Cable + Restart<br>(2) Discord Settings → Voice & Video → Input Device → CABLE Input |
| ❌ `Discord เห็น CABLE Input แต่ไม่มีเสียง` | Server ยังไม่ได้รัน หรือมือถือยังไม่ Connect | ดูที่ console server — ต้องเห็น `📱 Connected:` |
| ❌ **iOS ไม่ขึ้น pop-up Allow ไมค์** | iOS บังคับ HTTPS — HTTP ไม่ทำงาน | ใช้ `--secure` แล้วเปิด `https://IP:8443/web-client.html` |
| ❌ `Safari: "Cannot Verify Identity"` | Self-signed cert ปกติที่ต้อง accept | กด Show Details → Visit This Website |
| ❌ `Server ปิดไม่ลง` | Windows ตีความ Ctrl+C ไม่ปกติ | กด Ctrl+C ซ้ำ หรือปิดหน้าต่าง Command Prompt |
| ❌ `--list-devices ไม่เจอ CABLE` | ยังไม่ได้ Restart หลังติดตั้ง VB-Cable | Restart คอม แล้วลองใหม่ |
| ❌ `WebSocket Connection Failed` | ใส่ IP หรือ Port ผิด | เช็ค IP คอม (ใช้ `ipconfig`) และ Port (ปัจจุบันใช้ 8443 ใน --secure mode) |
| ❌ **"CABLE Output" ไม่มีใน list** | ปกติ! ของ Bai จะขึ้นเป็น **"CABLE Input"** แทน | ใช้ `DEVICE_INDEX=27` หรือ `DEVICE_NAME=CABLE Input`
| ❌ **เสียงแตก/ยับ (ผ่าน VB-Cable)** | ส่ง mono ไปยัง VB-Cable ที่ 48000 Hz → WASAPI mono→stereo แปลงห่วย | Server แก้ให้แล้ว — mono→stereo convert อัตโนมัติ |
| ❌ **เสียงเบามากแม้เปิด autoGainControl** | iPad mic raw level ต่ำมาก | เพิ่ม `--gain 3.0` หรือมากกว่า |
| ❌ **iOS เชื่อมต่อแล้ว แต่ streaming @ 0.0 kbps** | ScriptProcessorNode ไม่ยิง onaudioprocess (iOS bug) | Server แก้ให้แล้ว (GainNode + callback timing)
| ❌ **เสียงเพี้ยน/ฟังไม่รู้เรื่อง (iOS)** | onaudioprocess callback ตั้งช้า → iOS accumulate buffer | Server แก้ให้แล้ว (callback ตั้งก่อน connect audio graph)
| ❌ **เปิดหน้าเว็บได้ แต่ WSS connection fail** | iOS cert trust per-port (cert ยอมรับแค่ port 8443) | Server แก้ให้แล้ว — HTTP+WSS ใช้ port 8443 เดียวกัน

---

## 11. อธิบายศัพท์เทคนิค (Glossary)

| คำศัพท์ | คำอ่าน | ความหมาย |
|---------|--------|---------|
| **Python** | ไพธอน | ภาษาโปรแกรมชนิดหนึ่ง |
| **WebSocket** | เว็บซอคเก็ต | ช่องทางส่งข้อมูลแบบ real-time ระหว่างเครื่อง |
| **VB-Cable** | วีบี เคเบิล | โปรแกรมจำลองสายเสียงเสมือน |
| **.env** | ดอท อีเอ็นวี | ไฟล์ตั้งค่าที่เก็บค่าต่าง ๆ ที่แต่ละคนอาจไม่เหมือนกัน |
| **Port** | พอร์ต | เลขช่องทางการสื่อสาร (เหมือนประตูบ้าน) |
| **IP Address** | ไอพี แอดเดรส | เลขที่อยู่ของคอมในเครือข่าย |
| **PCM16** | พีซีเอ็ม สิบหก | รูปแบบเสียงที่ไม่บีบอัด คุณภาพสูง |
| **Sample Rate** | แซมเพิล เรต | จำนวนตัวอย่างเสียงต่อวินาที — ยิ่งสูงยิ่งคมชัด |
| **Buffer** | บัฟเฟอร์ | พื้นที่พักข้อมูลชั่วคราว — ยิ่งใหญ่ยิ่งเสถียรแต่หน่วง |
| **Dependency** | ดีเพนเดนซี | โปรแกรมย่อยที่โปรแกรมหลักต้องพึ่งพา |
| **pip** | พิป | โปรแกรมติดตั้ง dependency ของ Python |
| **Command Prompt** | คอมมานด์ พรอมพ์ | หน้าต่างดำ ๆ สำหรับพิมพ์คำสั่ง (cmd) |
| **localhost** | โลคัลโฮสต์ | การเรียกตัวเอง — ใช้ตอนทดสอบในเครื่องเดียว |
| **Wi-Fi 5GHz** | ไวไฟ ห้ากิกะเฮิรตซ์ | คลื่น Wi-Fi ความถี่สูง เร็วกว่า 2.4GHz แต่ระยะสั้นกว่า |
| **Git** | กิท | โปรแกรมจัดการเวอร์ชันของโค้ด |

---

## Quick Reference

| อยากทำอะไร | เปิดไฟล์ไหน | ทำยังไง |
|------------|------------|---------|
| เปลี่ยน Port / Device | `.env` | แก้ค่า `DEVICE_INDEX=27` หรือ `DEVICE_NAME=CABLE Input` |
| ดูว่ามีอุปกรณ์เสียงอะไรบ้าง | Terminal | `python audio-server.py --list-devices` |
| รัน server | Terminal | `python audio-server.py` |
| เชื่อมต่อจากมือถือ | Safari → URL | `http://<IP>:8000/web-client.html` |
| ใช้ใน Discord | Discord Settings | Input Device → CABLE Input (VB-Audio) |
| ติ๊กต่อ dependencies | Terminal | `pip install -r requirements.txt` |
| หา IP คอม | Terminal | `ipconfig` → ดู IPv4 Address |

---

**🎉 ขอให้สนุกกับการใช้ miclink นะคะ!** ถ้ามีปัญหาอะไรเพิ่มเติม ถาม Iris ได้ตลอดค่าา~
