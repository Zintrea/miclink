# 🎙️ miclink — เรื่องราวการพัฒนา (Development Story)

> เอกสารนี้เล่าที่มา การเดินทาง และเทคโนโลยีของ miclink ตั้งแต่เริ่มจนถึงปัจจุบัน
> เขียนมาเพื่อให้คนที่ไม่เขียนโปรแกรมก็อ่านรู้เรื่อง

---

## สารบัญ

| หัวข้อ | เนื้อหา |
|--------|--------|
| [1](#1-ท--าไมต-องม-miclink) | ทำไมต้องมี miclink? |
| [2](#2-ช-วงแรก---idea-เร-มต-n) | ช่วงแรก — Idea เริ่มต้น |
| [3](#3-เทคโนโลย-ท-ใช-อธ-บายเหม-อนอธ-บายให-คนท-ว-ไปฟ-ง) | เทคโนโลยีที่ใช้ (อธิบายให้คนทั่วไปฟัง) |
| [4](#4-โครงสร-างของโปรแกรม) | โครงสร้างของโปรแกรม |
| [5](#5-การเด-nทางของโค-ด---จากเวอร-ช-นแรกถ-งป-จจ-b-น) | การเดินทางของโค้ด — จากเวอร์ชันแรกถึงปัจจุบัน |
| [6](#6-ป-ญหาท-เจอระหว-างทาง) | ปัญหาที่เจอระหว่างทาง |
| [7](#7-ของเล-นเทคน-ค---เทคน-คเจ-งๆ-ท-ใช-) | ของเล่นเทคนิค — เทคนิคเจ๋งๆ ที่ใช้ |
| [8](#8-ส-งท-ย-งอยากทำต-อ-roadmap) | สิ่งที่ยังอยากทำต่อ (Roadmap) |

---

## 1. ทำไมต้องมี miclink?

### ปัญหาที่เจอ

สองคำถามที่คุณ Bai (ใบ) ถามตัวเอง:

> **"ทำไมไมค์คอมพิวเตอร์ถึงห่วยจัง?"**
> **"ทำไมต้องซื้ออุปกรณ์เพิ่ม แค่ใช้ไมค์ iPad ก็พอ?"**

ใบเป็นคนที่ใช้ Discord คุยกับเพื่อนเป็นประจำ และบางครั้งก็ต้องอัดเสียงหรือสตรีม แต่ไมค์คอมพิวเตอร์ที่ใช้อยู่ให้คุณภาพเสียงที่ไม่ดีพอ — ฟังดูอู้อี้ ไม่คมชัด

ในขณะเดียวกัน **iPad มีไมโครโฟนคุณภาพสูงมาก** (48kHz 16-bit = ระดับเดียวกับอุปกรณ์อัดเสียงมืออาชีพ) และใบก็มี iPad อยู่แล้ว! แต่...

### อุปสรรคที่มีในตลาด

| วิธี | ข้อเสีย |
|------|---------|
| ซื้อ Capture Card | แพง — หลักพันถึงหมื่นบาท |
| สาย Audio Interface | สายยาวเกะกะ ต้องเดินสาย |
| แอพใน App Store | ต้องเสียเงิน แถมบางทีใช้ยาก |
| Discord บนมือถือ | ฟังเสียงเกม/คอมไม่ได้ |
| เอาไมค์ Bluetooth | หน่วงสูง เสียงไม่ดี |

### การกำเนิดของ miclink

**"ถ้าทำเองด้วย Web browser + Wi-Fi ล่ะ?"**

ใบกับ Iris (ไอริส) เลยมาช่วยกันทำ miclink — โปรแกรมเปิดฟรีที่ใช้แค่:
1. ✅ **คอมพิวเตอร์ Windows** (ที่ลง Python)
2. ✅ **iPad / iPhone / Android** (อะไรก็ได้ที่มี browser)
3. ✅ **Wi-Fi** (เครือข่ายเดียวกัน)
4. ✅ **VB-Cable** (โปรแกรมฟรีที่หลอกคอมว่ามีไมค์เสียบอยู่)

**โดยไม่ต้องซื้ออะไรเพิ่มเลยสักบาท!**

---

## 2. ช่วงแรก — Idea เริ่มต้น

### แนวคิด

```
ไมค์ iPad → Safari → สัญญาณเสียง (ผ่าน Wi-Fi) → คอมพิวเตอร์ → VB-Cable → Discord
```

ฟังดูเหมือนง่าย แต่มันมีอะไรซ่อนอยู่เยอะมาก!

### สิ่งที่ต้องทำให้ได้

1. ✅ **จับเสียงจากไมค์ iPad** ผ่านเว็บเบราว์เซอร์
2. ✅ **ส่งเสียงนั้นผ่าน Wi-Fi** แบบ real-time (ไม่กระตุก ไม่หน่วง)
3. ✅ **รับเสียงที่ฝั่งคอมพิวเตอร์** และส่งต่อไปยัง VB-Cable
4. ✅ **Discord / OBS / Zoom** คิดว่ามีไมค์ตัวใหม่เสียบอยู่

### ข้อจำกัดที่ต้องเจอ

- iOS (iPad/iPhone) **ห้ามเว็บ HTTP ใช้ไมค์** — ต้อง HTTPS เท่านั้น!
- iOS Safari **จัดการเสียงแปลกกว่า Chrome** — ต้องปรับแต่งเยอะ
- VB-Cable **เป็นโปรแกรมฟรีที่มีข้อจำกัด** — ต้องหาทาง绕过
- **ต้องหน่วงต่ำที่สุด** — ถ้าพูดไปแล้วได้ยินช้า จะคุยไม่รู้เรื่อง
- **คุณภาพเสียงต้องดี** — จะมาใช้ไมค์ 48kHz แต่เสียงเหมือนโทรศัพท์ก็ไม่คุ้ม

---

## 3. เทคโนโลยีที่ใช้ (อธิบายเหมือนอธิบายให้คนทั่วไปฟัง)

```
สายส่งเสียงของ miclink ทำงานยังไง?
====================================

iPad ของคุณ:
   🎤 ไมค์ → แปลงเป็นเลข 0 กับ 1 → ส่งผ่าน Wi-Fi → 🖥️ คอมพิวเตอร์

คอมพิวเตอร์ของคุณ:
   📥 รับเลข 0 กับ 1 → ขยายเสียง → ส่งไป VB-Cable → 🎮 Discord/OBS/Zoom
```

### แต่ละชิ้นส่วนคืออะไร?

#### 🐍 Python — "สมองของโปรแกรม"

Python ก็คือภาษาที่ใช้เขียนโปรแกรม เหมือนภาษาอังกฤษที่ใช้สั่งคอมพิวเตอร์
— ข้อดีคืออ่านง่ายและมีเครื่องมือให้ใช้ฟรีเยอะมาก
— ใน miclink, Python ทำหน้าที่เป็น **ตัวกลาง** คอยรับเสียงจาก Wi-Fi แล้วส่งต่อ

#### 🌐 WebSocket — "สายยางส่งข้อมูล"

ปกติเวลาเปิดเว็บ เช่น Facebook หรือ YouTube:
- คุณเปิด → ขอข้อมูล → เซิฟเวอร์ส่งมาให้ → จบ (แล้วค่อยขอใหม่)

แต่ WebSocket **ไม่จบ** — มันเปิดสายไว้ตลอด:
```
ปกติ:       เปิด → ขอ → ได้ → ปิด → เปิด → ขอ → ได้ → ปิด
WebSocket:  เปิด → ────── ข้อมูลไหลเรื่อย ๆ ────── → ปิด
```

นี่คือหัวใจของ miclink! เพราะเสียงต้องไหล **ตลอดเวลา** ไม่ใช่ส่งทีเดียวแล้วจบ

#### 🎤 PyAudio — "ท่อต่อเสียง"

PyAudio เป็นตัวกลางที่ทำให้ Python สามารถ **พูดคุยกับอุปกรณ์เสียง** ของคอมพิวเตอร์ได้
— เหมือนท่อที่ต่อจากโปรแกรม Python ของเราไปยังลำโพงหรือ VB-Cable

#### 🔌 VB-Cable — "สายเสียงปลอม" (สำคัญมาก!)

VB-Cable คือโปรแกรมที่สร้าง **อุปกรณ์เสียงเสมือน** ขึ้นมาในคอมพิวเตอร์ของคุณ
— มันทำให้ Windows คิดว่ามีการ์ดเสียงหรือไมโครโฟนตัวใหม่เสียบอยู่

```
VB-Cable มี 2 ด้าน:
┌─────────────────────────────────────┐
│                                     │
│  🎯 ด้านเข้า (Playback):            │
│      ← Server ของเราส่งเสียงมาตรงนี้  │
│                                     │
│      ════════ สายเดินผ่าน ════════   │
│                                     │
│  🎤 ด้านออก (Recording):            │
│      → Discord อ่านเสียงจากตรงนี้     │
└─────────────────────────────────────┘
```

#### 🔒 SSL / HTTPS — "กุญแจล็อคความปลอดภัย"

เว็บทั่วไปขึ้นต้นด้วย `http://` แต่ `https://` หมายถึงข้อมูลถูกเข้ารหัส
— **iOS บังคับ** ว่าเว็บที่จะใช้ไมค์ได้ ต้องเป็น HTTPS เท่านั้น
— miclink เลยสร้าง "กุญแจ" (Certificate) ของตัวเองขึ้นมา เพื่อเอาไว้ล็อคการส่งข้อมูล

---

## 4. โครงสร้างของโปรแกรม

```
📁 miclink/
│
├── 🐍 audio-server.py     ← ตัวหลัก! (ไฟล์เดียวจัดการทุกอย่าง)
├── 🌐 web-client.html      ← หน้าเว็บสำหรับเปิดบน iPad
├── 🔬 diagnostic.html      ← หน้าทดสอบ (ไว้เช็คว่าไมค์ iPad ใช้ได้ไหม)
│
├── 📝 README.md            ← คำอธิบายสั้น ๆ (ไว้ดูบน GitHub)
├── 📝 GUIDE.md             ← คู่มือการใช้งานภาษาไทย
├── 📝 DEVELOP.md           ← เอกสารนี้ (เรื่องราวการพัฒนา)
├── 📝 KNOWLEDGE.md         ← ความรู้เทคนิค (สำหรับคนเขียนโปรแกรม)
│
├── ⚙️ .env                 ← ไฟล์ตั้งค่า (port, device index)
├── 📋 requirements.txt     ← รายการของที่ต้องติดตั้ง
│
├── 🧪 test-pyaudio.py      ← เครื่องมือทดสอบเสียง (ไว้ debug)
├── 🧪 stereo-test.py       ← ทดสอบ mono vs stereo
├── 🧪 rate-test.py         ← ทดสอบ sample rate 44100 vs 48000
│
├── 📁 certs/               ← โฟลเดอร์เก็บกุญแจ SSL
│   └── gen-cert.py         ← ตัวสร้างกุญแจ (รันครั้งเดียว)
│
└── 📁 .git/                ← ระบบจัดการเวอร์ชัน (ไม่ต้องแตะ)
```

### ทำไม audio-server.py ไฟล์เดียว?

ใบกับ Iris เลือกทำ **ไฟล์เดียว** เพราะ:
1. **ติดตั้งง่าย** — ไม่ต้องรันหลายตัว
2. **debug ง่าย** — ไม่ต้องเปิดหลายหน้าต่าง
3. **พกพาง่าย** — ก็อปไปเครื่องอื่นก็รันได้เลย
4. **เท่านั้นที่จำเป็น** — ไม่อยากทำให้ใหญ่เกินความจำเป็น

---

## 5. การเดินทางของโค้ด — จากเวอร์ชันแรกถึงปัจจุบัน

> นี่คือไทม์ไลน์การพัฒนา miclink ตั้งแต่เริ่มต้น (เรียงจากเก่าไปใหม่)

### ระยะที่ 1: "แค่ให้มันส่งเสียงได้" 🎯

**1 มกราคม 2569**

ใบเริ่มเขียน miclink ครั้งแรกด้วย Python + WebSocket แบบง่ายมาก
— ได้เสียงจากไมค์เบราว์เซอร์ → ส่ง WebSocket → PyAudio เล่นออกลำโพง
— ยังไม่มีอะไรเลย แค่ mono ปกติ 48kHz

```
โค้ดตอนแรก: รับเสียง → ส่ง → เล่น  (ประมาณ 100 บรรทัด)
```

### ระยะที่ 2: "เพิ่มลูกเล่น" ⚙️

ใบเพิ่มระบบ `.env` ให้ตั้งค่า port และ device index ได้
— เพิ่ม `--list-devices` ให้ดูว่ามีอุปกรณ์เสียงอะไรบ้าง
— เพิ่ม `GUIDE.md` คู่มือภาษาไทย
— เริ่มเขียน README.md ภาษาไทย
— เริ่มใช้ Git จริงจัง

### ระยะที่ 3: "คุณลืม iOS ไปรึเปล่า?" 🍏

**‼️ จุดเปลี่ยนสำคัญ**

พอใบลองใช้ miclink จาก iPad ปัญหาทะลัก!

ปัญหาแรก: **iOS ไม่ยอมให้ใช้ไมค์ผ่าน HTTP**
— iPad/iPhone ทุกเครื่อง **บังคับ HTTPS** เพื่อใช้ getUserMedia (คำสั่งขอใช้ไมค์)
— ถ้าเปิดผ่าน HTTP → จะไม่มี pop-up ถาม Allow เลย!

วิธีแก้: ใบเพิ่ม `--secure` mode (HTTPS + WSS หรือ WebSocket ที่เข้ารหัส)
— สร้าง Self-signed Certificate (กุญแจที่เราทำเอง — ฟรี!)
— เปิด port 443 (หรือ 8443) สำหรับ HTTPS
— เปิดอีก port (8765) สำหรับ WebSocket ที่เข้ารหัส

### ระยะที่ 4: "ปัญหาลูกโซ่ของ iOS" 🔗

ปัญหาตามมาติด ๆ:

**4.1 — Certificate Trust Per-Port**
- เวลา accept cert ตอนเปิดหน้าเว็บที่ port 8443 → iOS จำไว้แค่ port 8443
- แต่ WebSocket ไปอีก port 8765 → iOS ไม่ยอมรับ cert → connection fail
- ✅ **วิธีแก้:** เอา HTTPS + WSS ไว้ port เดียวกัน (8443) โดยใช้ `process_request`

**4.2 — onaudioprocess ไม่เคยยิง**
- ScriptProcessorNode (ตัวแปลงเสียงของ JavaScript) **ไม่ทำงานเลย** บน iOS
- เพราะ iOS Safari ต้องการให้ audio graph ครบวงจร (source → processor → destination)
- ✅ **วิธีแก้:** ใช้ `GainNode(0)` — เหมือนต่อสายไฟแบบมีสวิตช์ปิด ไม่ให้เสียงเข้าหูตัวเอง แต่เปิดวงจรให้ processor ทำงาน

**4.3 — เสียง Garbled (ฟังไม่รู้เรื่อง)**
- พอ onaudioprocess ทำงาน เสียงที่ได้กลับมาแตก ๆ เพี้ยน ๆ
- ✅ **วิธีแก้:** ต้องตั้ง callback (`onaudioprocess`) **ก่อน** ต่อ audio graph — iOS สะสม buffer ไว้ถ้าไม่ตั้ง callback ให้พร้อมก่อน

**4.4 — Sample Rate ไม่ตรงกัน**
- iPad mic อาจเก็บเสียงที่ 48000 Hz แต่ AudioContext (ตัวจัดการเสียงของเบราว์เซอร์) คืนค่าเป็น 44100 Hz
- ถ้าส่ง 44100 ไปให้ server ที่เล่น 48000 → เสียงเพี้ยน
- ✅ **วิธีแก้:** ให้ client ส่ง `{sample_rate: 44100}` ไปเป็นข้อความแรกก่อนส่งเสียง — server จะปรับตาม

### ระยะที่ 5: "VB-Cable ก็มีปัญหาของมัน" 🔌

**5.1 — Mono = เสียงแตก**
- VB-Cable ที่ 48000 Hz มีบั๊ก — ส่ง mono (1 ช่อง) ไปแล้ว WASAPI (ระบบเสียง Windows) แปลงเป็น stereo ไม่ดี → เสียงแตก
- ✅ **วิธีแก้:** ให้ server **แปลง mono → stereo** ด้วยตัวเอง (ทำซ้ำ L และ R) — ใช้ CPU น้อยกว่า แถมเสียงชัด!

**5.2 — iPad เสียงเบามาก**
- iPad mic เก็บเสียงมาในระดับที่เบามาก แม้เปิด `autoGainControl` ก็ยังเบา
- ✅ **วิธีแก้:** เพิ่ม `--gain 3.0` — server ขยายเสียงให้ 3 เท่า (แต่ไม่เกิน 32767 เพื่อไม่ให้เสียงแตก / clipping)

### ระยะที่ 6: "เครื่องมือเสริม" 🧰

ใบเพิ่มเครื่องมือสำหรับ debug และทดสอบ:
- `test-pyaudio.py` — ทดสอบว่า PyAudio ทำงาน正常ไหม
- `stereo-test.py` — ทดสอบ mono vs stereo ผ่าน VB-Cable
- `rate-test.py` — ทดสอบ 44100 vs 48000 Hz
- `diagnostic.html` — เปิดบน iPad เพื่อดูว่า ScriptProcessorNode 正常หรือไม่
- `--record diag.wav` — บันทึกเสียงไว้ฟังทีหลัง

### ระยะที่ 7: "บริการหลังการขาย" 📝

ใบเขียนเอกสาร:
- **KNOWLEDGE.md** — สรุปปัญหาที่เจอ (ไว้ดูเร็ว ๆ)
- **GUIDE.md v2.0.0** — คู่มือภาษาไทยละเอียด (589 บรรทัด!)
- **DEVELOP.md** — เอกสารนี้ (ไว้เล่าเรื่อง)

### สรุปการเดินทางเป็นตัวเลข

| เมตริก | จำนวน |
|--------|-------|
| จำนวนครั้ง commit | 24 |
| จำนวนไฟล์ | 11 (ไม่รวม .git) |
| ระยะเวลา | ประมาณ 1 เดือน (ม.ค. – พ.ค. 2569) |
| ปัญหาที่เจอและแก้ | 14+ ครั้ง |
| บรรทัดโค้ดรวม | ~1,700 (audio-server.py ~373, web-client.html ~426) |
| branch ที่สร้าง | 2 (main + fix/ios-audio-graph) |

---

## 6. ปัญหาที่เจอระหว่างทาง

> ปัญหาทุกข้อในตารางนี้ **แก้ไขเรียบร้อยแล้ว**

| # | ปัญหา | อาการ | สาเหตุ (เทคนิค) | วิธีแก้ |
|---|-------|-------|----------------|--------|
| 1 | iOS ไม่ยอมให้ใช้ไมค์ | ไม่มี pop-up Allow | HTTP → getUserMedia ถูก iOS block | ใช้ `--secure` mode (HTTPS) |
| 2 | cert trust แยก port | เปิดหน้าเว็บได้ แต่ WebSocket fail | iOS trust cert per port | รวม HTTP+WSS ไว้ port 8443 เดียว |
| 3 | WebSocket upgrade ถูกจี้ | process_request ไป intercept WebSocket request | websockets v14+ แยก HTTP/WS request ผิด | ตรวจสอบ Upgrade header ก่อน |
| 4 | stream @ 0.0 kbps | iPad connect แต่ onaudioprocess ไม่ยิง | iOS ต้องการ GainNode ต่อ destination | ใช้ GainNode(0) |
| 5 | เสียง Garbled (iOS) | iOS ได้ยินเสียงแตก/ฟังไม่รู้เรื่อง | onaudioprocess callback ตั้งช้า | ตั้ง callback ก่อน connect graph |
| 6 | Sample Rate ไม่ตรง | iPhone mic 48000 → AudioContext 44100 | AudioContext.sampleRate ≠ hardware rate | ส่ง `{sample_rate}` จาก client |
| 7 | VB-Cable mono = แตก | ส่ง mono → VB-Cable ที่ 48000 → แตก | WASAPI mono-to-stereo conversion ห่วย | ส่ง stereo (L/R duplicate) |
| 8 | เสียงเบามาก | iPad mic raw level ต่ำ | autoGainControl ไม่พอ | `--gain 3.0` + autoGainControl |
| 9 | Ctrl+C ไม่ปิด server | Windows ไม่ support signal handler | Windows ≠ Linux | ใช้ try/except KeyboardInterrupt |
| 10 | ไม่มี .env | ต้อง hardcode ค่า | config embedded in code | เพิ่ม python-dotenv |

---

## 7. ของเล่นเทคนิค — เทคนิคเจ๋งๆ ที่ใช้

### 7.1 AudioContext.sampleRate (แก้ sample rate ไม่ตรง)

ตอนแรกใบใช้ `track.getSettings().sampleRate` (ค่า hardware) แต่ iOS Safari อาจคืนค่าเป็น undefined!

```javascript
// ❌ ไม่ได้ผลบน iOS:
const settings = track.getSettings();
const rate = settings.sampleRate;  // undefined!

// ✅ ใช้ AudioContext.sampleRate แทน:
const audioContext = new AudioContext();
const rate = audioContext.sampleRate;  // 44100 หรือ 48000
```

แล้วส่งค่า `{sample_rate: audioContext.sampleRate}` เป็นข้อความแรกให้ server
server ปรับ sample rate ตาม:

```python
new_rate = info.get("sample_rate")
if new_rate and new_rate != self.rate:
    self.stream.close()
    self.rate = new_rate
    self.open_stream()
```

### 7.2 process_request — รวม HTTP + WSS ในพอร์ตเดียว

ปกติ WebSocket และ HTTP ต้องแยก port กัน แต่ iOS ต้องการให้ cert trust ตรงกัน ใบเลยใช้ `process_request` callback เพื่อให้ server จัดการทั้ง HTTP และ WebSocket ในพอร์ตเดียว:

```python
async def handle_http_request(self, connection, request):
    # ถ้าเป็น WebSocket upgrade → return None (ให้ library จัดการ)
    if request.headers.get("Upgrade", "").lower() == "websocket":
        return None
    # ถ้าเป็น HTTP ปกติ → serve static file
    return Response(200, "OK", headers, body)
```

### 7.3 Mono → Stereo ด้วย Bit Manipulation

VB-Cable ที่ 48000 Hz มีปัญหาเวลาเล่น mono ใบเลยเขียนฟังก์ชันแปลงด้วยมือ:

```python
def mono_to_stereo(mono_bytes, gain=3.0):
    for i in range(0, len(mono_bytes), 2):
        sample = mono_bytes[i] | (mono_bytes[i + 1] << 8)
        # ... apply gain, clamp ...
        # Duplicate to L and R
        result[i * 2]     = sample & 0xFF       # L low byte
        result[i * 2 + 1] = (sample >> 8) & 0xFF # L high byte
        result[i * 2 + 2] = sample & 0xFF       # R low byte (same)
        result[i * 2 + 3] = (sample >> 8) & 0xFF # R high byte (same)
```

### 7.4 GainNode(0) — แก้ iOS Safari Audio Graph Bug

iOS Safari ต้องการให้ audio graph **ครบวงจร** (source → processor → destination) ถึงจะยิง onaudioprocess แต่ถ้าต่อ processor ตรงไป destination จะได้ยินเสียงตัวเองใน iPad ใบเลยใช้ GainNode(0) — เหมือนสวิตช์ปิด:

```javascript
const silentGain = audioContext.createGain();
silentGain.gain.value = 0;    // ปิดเสียง (ใบ้)
processor.connect(silentGain);
silentGain.connect(audioContext.destination);
```

---

## 8. สิ่งที่ยังอยากทำต่อ (Roadmap)

> miclink เวอร์ชัน 2.0.0 ใช้งานได้จริงและเสถียรแล้ว!
> แต่ใบกับ Iris ก็มีไอเดียเพิ่มเติมสำหรับอนาคต:

- [ ] **🔬 AudioWorklet** — แทน ScriptProcessorNode ที่ deprecated (คุณภาพดีกว่า, หน่วงน้อยกว่า)
- [ ] **📦 Docker/Portable** — ทำเป็นแพ็กเกจที่เปิดแล้วใช้ได้ทันที ไม่ต้องติดตั้ง Python
- [ ] **📊 VU Meter** — แสดงระดับเสียงบนเว็บหน้า iPad
- [ ] **🎛️ Volume Slider** — ปรับ gain จากหน้าเว็บ (ไม่ต้อง restart server)
- [ ] **📱 PWA** — ทำให้เป็น App-like บน iPad (เปิดแล้วใช้เหมือนแอพ)
- [ ] **🔇 Noise Gate** — ตัดเสียงพื้นหลังอัตโนมัติ
- [ ] **⏱️ Latency Monitor** — แสดงค่าหน่วงแบบ real-time
- [ ] **🌐 Discovery** — ค้นหา server อัตโนมัติ (Bonjour/mDNS)

---

> **miclink** เกิดจากปัญหาจริงที่ใบเจอ และแก้ด้วยโค้ดที่เขียนเอง — ตั้งแต่จับมือทำจนใช้งานได้จริง
>
> ถ้าอ่านแล้วมีคำถาม หรืออยากรู้เทคนิคเพิ่มเติม ถาม Iris (ไอริส) ได้ทุกเมื่อเลยนะคะ 💕

*— Iris & Bai, 18 พฤษภาคม 2569*
