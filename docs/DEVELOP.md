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
│
├── 📝 README.md            ← คำอธิบายสั้น ๆ (ไว้ดูบน GitHub)
│
├── 📁 docs/                ← เอกสารทั้งหมด
│   ├── 📝 GUIDE.md         ← คู่มือการใช้งานภาษาไทย
│   ├── 📝 DEVELOP.md       ← เอกสารนี้ (เรื่องราวการพัฒนา)
│   └── 📝 KNOWLEDGE.md     ← ความรู้เทคนิค (สำหรับคนเขียนโปรแกรม)
│
├── 📁 debug/               ← เครื่องมือ debug & ทดสอบ
│   ├── 🔬 diagnostic.html  ← หน้าทดสอบไมค์ iPad
│   ├── 🧪 test-pyaudio.py  ← ทดสอบ PyAudio playback
│   ├── 🧪 stereo-test.py   ← ทดสอบ mono vs stereo
│   └── 🧪 rate-test.py     ← ทดสอบ sample rate
│
├── ⚙️ .env                 ← ไฟล์ตั้งค่า (port, device index)
├── 📋 requirements.txt     ← รายการของที่ต้องติดตั้ง
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
| `debug/test-pyaudio.py` — ทดสอบว่า PyAudio ทำงาน正常ไหม
| `debug/stereo-test.py` — ทดสอบ mono vs stereo ผ่าน VB-Cable
| `debug/rate-test.py` — ทดสอบ 44100 vs 48000 Hz
| `debug/diagnostic.html` — เปิดบน iPad เพื่อดูว่า ScriptProcessorNode 正常หรือไม่
- `--record diag.wav` — บันทึกเสียงไว้ฟังทีหลัง

### ระยะที่ 7: "บริการหลังการขาย" 📝

ใบเขียนเอกสาร:
- **docs/KNOWLEDGE.md** — สรุปปัญหาที่เจอ (ไว้ดูเร็ว ๆ)
- **docs/GUIDE.md v2.0.0** — คู่มือภาษาไทยละเอียด (589 บรรทัด!)
- **docs/DEVELOP.md** — เอกสารนี้ (ไว้เล่าเรื่อง)

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

## 7. เปิดกล่องเทคนิค — miclink ทำงานยังไง?

> ส่วนนี้จะอธิบาย **เบื้องหลังการทำงานของ miclink** ตั้งแต่เสียงเข้าไมค์ iPad จนถึง Discord
> ใช้ภาษาที่คนไม่เขียนโปรแกรมก็พอเก็ท — แต่ก็ลงรายละเอียดเทคนิคให้คนเขียนโค้ดอ่านสนุก

---

### 7.0 การเดินทางของเสียง 1 วินาที

ก่อนจะลงลึกแต่ละเทคนิค มาดู **เส้นทางของเสียง** ตั้งแต่พูดใส่ iPad จนถึง Discord:

```
พูดใส่ iPad
    ↓
① Safari จับเสียงด้วย getUserMedia() 
    → ไมค์ iPad แปลงคลื่นเสียงเป็นเลข (Float32)
    ↓
② AudioContext + ScriptProcessorNode
    → แปลง Float32 → Int16 (PCM16)
    → เก็บใน buffer (2048 ตัวอย่าง/ครั้ง)
    ↓
③ WebSocket (WSS) ส่งไปยังคอมผ่าน Wi-Fi
    → ส่งเป็น binary frame (raw bytes)
    → ไม่บีบอัด — 768 kbps ตลอดเวลา
    ↓
④ Python Server รับ data
    → ขยายเสียง (Gain × 3.0)
    → แปลง Mono → Stereo
    ↓
⑤ PyAudio ส่งไปยัง VB-Cable
    → VB-Cable Input (device index 27)
    ↓
⑥ Discord อ่านจาก VB-Cable (Recording ด้าน)
    → เพื่อนได้ยินเรา!!

พูด 1 ประโยค = ข้อมูลเดินทาง 6 จุดนี้
ทุกอย่างเกิดขึ้นภายใน ~50-100ms (หน่วงน้อยกว่าที่มนุษย์รู้สึก)
```

---

### 7.1 WebSocket — ทำไมต้องใช้ และมันคืออะไร?

#### HTTP vs WebSocket: เปรียบเทียบให้เห็นภาพ

**HTTP ปกติ** (เวลาคุณเปิดเว็บ):

```mermaid
คุณ → ขอข้อมูล → เซิฟเวอร์
              → ส่งกลับมา → ปิดสาย
คุณ → ขอข้อมูล → เซิฟเวอร์  
              → ส่งกลับมา → ปิดสาย
```

— เปิดสายเวลาโหลด ปิดเมื่อได้ข้อมูล  
— เรียกเปิดใหม่ทุกครั้งที่ต้องการข้อมูล  
— เหมือนโทรสั่งพิซซ่า: โทร→สั่ง→ได้รับ→วางสาย→เวลา餓โทรใหม่

**WebSocket** (miclink ใช้):

```mermaid
คุณ → ขอเปิดสาย → เซิฟเวอร์
              → ── data ──→ data ──→ data ──→ ...
              → ── data ──→ data ──→ data ──→ ...
              → เปิดสายไว้ตลอดไม่ปิด!!
```

— เปิดสายครั้งเดียว  
— ข้อมูลไหลตลอดเวลา **ทั้งสองทิศทาง**  
— เหมือนสายยางฉีดน้ำ: เปิดก๊อกแล้วน้ำไหลตลอด จนกว่าจะปิด

> **ถ้าใช้ HTTP ส่งเสียง:** คุณต้องส่ง request → รอ response → ปิด → เปิดใหม่ → ส่งอีก   
> → หน่วงมหาศาล! เพราะทุกครั้งที่เปิดสายมี overhead (ของแถม) เยอะ
>
> **ใช้ WebSocket:** เปิดสายครั้งเดียว → ส่ง data ได้ตลอด  
> → latency (ค่าหน่วง) ต่ำมาก — เหมาะกับ real-time audio

#### Handshake — การจับมือเปิดเส้นทาง

WebSocket ไม่ได้เปิดสายมั่ว ๆ มีพิธีเปิดเส้นทางที่เรียกว่า **Handshake**:

```
iPad → ขอเปิด WebSocket (HTTP Upgrade header)
     → "เฮ้ย Server! ฉันอยากเปลี่ยน protocol เป็น WebSocket นะ"

Server → ตรวจสอบว่าเป็น WebSocket จริง
       → "OK! เปลี่ยน protocol ให้"

iPad → OK! ส่งข้อมูล binary ได้เลย!
     → *ส่ง PCM16 audio bytes ไปตลอด*
```

ในโค้ดเราดูจาก header:

```python
# audio-server.py
if request.headers.get("Upgrade", "").lower() == "websocket":
    return None  # ให้ websockets library จัดการ
```

#### Binary vs Text Frames

WebSocket ส่งข้อมูลได้ 2 แบบ:

| ประเภท | ใช้กับ | ขนาด |
|--------|-------|------|
| **Text frame** | JSON metadata | เล็ก (ไม่กี่ byte) |
| **Binary frame** | เสียง PCM16 | ใหญ่ (4096 bytes ทุก 42ms) |

miclink ใช้ทั้งสองแบบ:
1. ส่ง **JSON text frame** (`{"sample_rate": 48000}`) เป็นข้อความแรก
2. จากนั้นส่ง **binary frame** (PCM16 audio data) ตลอดไป

ข้อความแรก = metadata, หลังจากนั้น = raw audio bytes

#### WSS — WebSocket ที่เข้ารหัส

- `ws://` = WebSocket ปกติ (ไม่เข้ารหัส — เหมือนพูดกันสด ๆ)
- `wss://` = WebSocket + SSL (เข้ารหัส — เหมือนกระซิบใส่เครื่องส่งวิทยุ)

iOS บังคับว่าเว็บที่ใช้ไมค์ได้ ต้องเป็น HTTPS → WSS เท่านั้น!

---

### 7.2 getUserMedia + Web Audio API — จับเสียงจากเบราว์เซอร์

นี่คือ **หัวใจของฝั่ง client** — ทำไม browser ถึงจับเสียงจากไมค์ได้?

#### getUserMedia — ขออนุญาตใช้ไมค์

```javascript
const constraints = {
    audio: {
        sampleRate: 48000,         // ขอคุณภาพ 48kHz
        channelCount: 1,           // mono (ไมค์คนเดียวพอ)
        echoCancellation: false,   // ปิดตัดเสียงก้อง — ไม่อยากให้เสีย quality
        noiseSuppression: false,   // ปิดตัดเสียงรบกวน
        autoGainControl: true,     // เปิดปรับระดับอัตโนมัติ
    }
};

navigator.mediaDevices.getUserMedia(constraints)
```

เวลาคุณกด **Allow** บน iPad → browser สร้าง **MediaStream** ที่มี audio track อยู่ข้างใน

#### Float32 → Int16 — ทำไมต้องแปลง?

ไมค์ดิจิตอลบันทึกเสียงเป็น **Float32** (เลขทศนิยม, มีค่าตั้งแต่ -1.0 ถึง 1.0)

แต่เราส่งผ่าน WebSocket ใช้ **Int16** (เลขจำนวนเต็ม 16-bit, -32768 ถึง 32767)

**ทำไมต้องแปลง?**

| รูปแบบ | ขนาด/ตัวอย่าง | แบบ |
|--------|-------------|------|
| Float32 | 4 bytes | -0.7342, 0.1234, -0.9921 |
| Int16 | 2 bytes | -24067, 4044, -32505 |

Int16 = ครึ่งหนึ่งของ Float32 = **แบนด์วิดท์น้อยลงครึ่งหนึ่ง**!

การแปลง (ใน `web-client.html`):

```javascript
processor.onaudioprocess = (e) => {
    const input = e.inputBuffer.getChannelData(0);  // Float32 [-1, 1]
    const pcm16 = new Int16Array(input.length);

    for (let i = 0; i < input.length; i++) {
        const sample = Math.max(-1, Math.min(1, input[i]));  // clamp
        pcm16[i] = sample < 0
            ? sample * 0x8000     // 0x8000 = 32768 (ค่าลบ)
            : sample * 0x7FFF;    // 0x7FFF = 32767 (ค่าบวก)
    }

    socket.send(pcm16.buffer);  // ส่ง raw binary!
};
```

**clamp** = ถ้าค่าเกิน -1 ถึง 1 → ตัดให้อยู่ในช่วง (กันเสียงแตก / clipping)

#### ScriptProcessorNode — ตัวกลางระหว่างเสียงกับโค้ด

```javascript
const bufferSize = 2048;
processor = audioContext.createScriptProcessor(bufferSize, 1, 1);
//                                     bufferSize  ↑ inputCh  ↑ outputCh

processor.onaudioprocess = (e) => {
    const input = e.inputBuffer.getChannelData(0);
    // ฟังก์ชันนี้ถูกเรียกทุกครั้งที่มี buffer ใหม่
    // bufferSize=2048 → ถูกเรียกทุก 2048/48000 = 42ms
};
```

| bufferSize | ถูกเรียกทุก | ข้อดี | ข้อเสีย |
|-----------|-----------|------|--------|
| 1024 | ~21ms | หน่วงน้อย | ใช้ CPU มาก, iPad อาจไม่ไหว |
| **2048** | **~42ms** | **สมดุล** | **ค่าเริ่มต้นของ miclink** |
| 4096 | ~85ms | เสถียรสุด | หน่วงมาก, รู้สึกได้ |

---

### 7.3 Sample Rate Synchronization — ทำไม iOS เสียงเพี้ยน?

#### ปัญหา

ไมค์ iPad อาจเก็บเสียงที่ **48000 Hz** แต่เบราว์เซอร์ **AudioContext** อาจคืนค่าแค่ **44100 Hz**

- iPad ส่ง 44100 Hz → คิดว่าส่ง 48000
- Server เล่นที่ 48000 → ได้รับ 44100 → เล่นเร็วเกินไป → เสียงสูง / เพี้ยน

#### วิธีแก้

miclink ไม่เดา — client ส่ง **metadata ก่อนข้อมูลเสียง**:

```javascript
// client → server (text frame แรก):
socket.send(JSON.stringify({ sample_rate: audioContext.sampleRate }));
```

```python
# server รับ metadata ก่อน:
info = json.loads(message)     # {"sample_rate": 44100}
new_rate = info.get("sample_rate")

if new_rate and new_rate != self.rate:
    self.stream.close()                 # ปิด stream เดิม
    self.rate = new_rate                # เปลี่ยน sample rate
    self.open_stream()                  # เปิด stream ใหม่ที่ rate ถูก
```

> ที่ใช้ **audioContext.sampleRate** แทน hardware rate (`track.getSettings().sampleRate`)
> เพราะ iOS Safari ไม่ให้ค่า hardware rate จริง (return undefined)!

---

### 7.4 GainNode(0) — iOS Safari Audio Graph Bug

#### ปัญหา

iOS Safari มีบั๊กที่ **ScriptProcessorNode จะไม่ยิง onaudioprocess เลย**
ถ้า audio graph ไม่สมบูรณ์

Audio graph คือสายต่อ:
```
Microphone → MediaStreamSource → ScriptProcessor → Destination (ลำโพง)
```

แต่ถ้าเราต่อ processor → destination ตรง ๆ:
- iPad จะได้ยินเสียงตัวเองผ่านลำโพง **ดังมาก** (Audio Feedback!)
- วน loop ไมค์→ลำโพง→ไมค์→ลำโพง → หวีด !

#### วิธีแก้ — GainNode(0)

```javascript
const silentGain = audioContext.createGain();
silentGain.gain.value = 0;        // ปิดเสียงสนิท (gain = 0)

source.connect(processor);         // source → processor
processor.connect(silentGain);     // processor → silent gain
silentGain.connect(audioContext.destination);  // → destination (แต่เงียบ)
```

เทียบกับชีวิตจริง:
```
GainNode(0) = สาย HDMI ต่อทีวี แต่กด mute
             → สัญญาณเดินทางครบวงจร
             → แต่ไม่มีเสียงออกลำโพง
```

#### ทำไมต้องตั้ง callback ก่อน connect?

iOS Safari มีพฤติกรรมถ้าคุณ:

```javascript
// ❌ ผิด — iOS จะ garbled:
source.connect(processor);        // ต่อ graph ก่อน
processor.onaudioprocess = fn;    // ตั้ง callback ทีหลัง
// → iOS เริ่มสะสม buffer ใน processor แล้ว
// → buffer ที่สะสมมา = garbage data

// ✅ ถูก:
processor.onaudioprocess = fn;    // ตั้ง callback ก่อน
source.connect(processor);        // แล้วค่อยต่อ graph
// → processor พร้อมทำงานตั้งแต่แรก
// → iOS ส่ง audio ที่ clean
```

---

### 7.5 process_request — รวม HTTP + HTTPS + WSS ในพอร์ตเดียว

#### ปัญหา

iOS Safari trust SSL certificate **แยกตาม port**

```
เปิด https://192.168.1.100:8443/  → accept cert (trust ไว้)
WebSocket wss://192.168.1.100:8765/ → ❌ ไม่ trust! cert คนละ port!
```

#### วิธีแก้ — Single Port

ถ้า HTTP และ WSS **ใช้ port เดียวกัน** → cert trust ตรงกัน → iOS happy

ปกติ WebSocket library (`websockets`) รองรับแค่ WS บนพอร์ตของตัวเอง  
เราต้องเขียน **process_request** callback เพื่อดัก:

```python
async def handle_http_request(self, connection, request):
    # Check: นี่คือ WebSocket upgrade request หรือเปล่า?
    if request.headers.get("Upgrade", "").lower() == "websocket":
        return None  # → ให้ websockets library จัดการ WebSocket

    # ไม่ใช่ WebSocket → เป็น HTTP ปกติ → serve ไฟล์
    path = request.path.lstrip("/")
    if path == "" or path == "/":
        path = "web-client.html"

    body = full_path.read_bytes()
    return Response(200, "OK", headers, body)
```

ขั้นตอน:

```
iPad → ขอเปิดหน้า web-client.html (HTTP) → process_request → ส่ง HTML กลับ
iPad → ขอ upgrade เป็น WebSocket → process_request → ให้ library จัดการ
```

ทั้งสองอย่างบน **port 8443** เดียวกัน — cert ที่ trust ไว้ใช้ได้ทั้ง HTTP และ WebSocket

---

### 7.6 Mono → Stereo — เพราะ VB-Cable รับ mono ไม่ได้

#### ปัญหา

VB-Cable ที่ 48000 Hz มีบั๊กเมื่อรับ mono (1 channel)

สาเหตุคือ **WASAPI mixer** ของ Windows — เมื่อได้รับ mono PCM16 ที่ 48000 Hz
มันพยายามแปลงเป็น stereo อัตโนมัติ → แปลงห่วย → เสียงแตก / Garbled

> ส่ง 44100 Hz mono = OK  
> ส่ง 48000 Hz mono = ❌ แตก!  
> ส่ง 48000 Hz stereo = ✅ สมบูรณ์

#### วิธีแก้ — Bit-Level Conversion

miclink ส่ง stereo **โดยเอา mono แทรก L และ R เหมือนกัน**:

```python
def mono_to_stereo(mono_bytes, gain=3.0):
    result = bytearray(len(mono_bytes) * 2)  # ขนาดเท่าตัว

    for i in range(0, len(mono_bytes), 2):
        # อ่าน mono sample (16-bit little-endian)
        sample = mono_bytes[i] | (mono_bytes[i + 1] << 8)

        # ปรับ unsigned → signed
        if sample >= 32768:
            sample -= 65536

        # apply gain + clamp
        sample = int(sample * gain)
        if sample > 32767: sample = 32767
        if sample < -32768: sample = -32768

        # ปรับกลับเป็น unsigned
        if sample < 0: sample += 65536

        # เขียน L และ R ด้วยค่าเดียวกัน
        result[i * 2]     = sample & 0xFF       # L low byte
        result[i * 2 + 1] = (sample >> 8) & 0xFF # L high byte
        result[i * 2 + 2] = sample & 0xFF       # R low byte
        result[i * 2 + 3] = (sample >> 8) & 0xFF # R high byte

    return bytes(result)
```

มองเป็นภาพ: 
```
Mono:  [sample1] [sample2] [sample3] ...
Stereo: [L=s1] [R=s1] [L=s2] [R=s2] [L=s3] [R=s3] ...
```

VB-Cable ได้ stereo → mixer ไม่ต้องแปลง → เสียงชัด!

---

### 7.7 Gain Boost — ขยายเสียง iPad ที่เงียบ

#### ปัญหา

iPad / iPhone มีไมค์คุณภาพดี แต่ **raw level** (ระดับเสียงดิบ) ที่ browser ส่งมาให้
ต่ำมาก — เพราะ iOS ตั้ง auto gain control ไว้เผื่อที่ว่าง (headroom)

ถ้าไม่ขยาย → Discord เพื่อนได้ยินเสียงเบาเหมือนกระซิบ

#### วิธีแก้ — คูณเลข แล้ว clamp

```python
# --gain 3.0 = default
sample = int(sample * gain)    # คูณ 3.0

# Clamp — ไม่ให้เกิน limit 16-bit
if sample > 32767:
    sample = 32767
elif sample < -32768:
    sample = -32768
```

| --gain | volume | เหมาะกับ |
|--------|--------|---------|
| 1.0 | ปกติ | ไมค์ USB, ไมค์คอม |
| 2.0 | ดังขึ้นนิด | iPad พูดปกติ |
| **3.0** | **ดังขึ้น 3x** | **iPad ค่าเริ่มต้น (default)** |
| 4.0 | ดังมาก | iPad พูดเบา / อยู่ไกล |
| 5.0 | ดังสุด | เสี่ยง clipping |

**Clipping (เสียงแตก)** = เมื่อเราเพิ่ม gain แล้ว sample เกิน 32767 หรือ ต่ำกว่า -32768
→ ข้อมูลเสียงถูกตัดทิ้ง → เสียงแตก

```python
# clipping เกิดขึ้นเมื่อ:
sample = 20000
sample * 5.0 = 100000  # > 32767 → clamp → 32767
# ข้อมูล detail ที่เกิน 32767 หายไป!
```

miclink เลือก default **3.0** เพราะ iPad mic raw level ต่ำมาก
แต่ก็ปลอดภัยพอไม่ให้ clipping ถ้าพูดปกติ

---

### 7.8 ภาพรวม — ทุกเทคนิคทำงานร่วมกัน

```
iPad Safari:
  getUserMedia → Float32 audio → clamp → Int16
                                   ↓
                   ส่ง {sample_rate} (JSON) ก่อน
                                   ↓
                   ส่ง PCM16 bytes (binary frame)
                                   ↓
                   ต่อ GainNode(0) ให้ iOS happy
                                   ↓
                   onaudioprocess callback set ก่อน connect

Computer Server:
                   รับ metadata → ตั้ง sample rate
                   ↓
                   รับ PCM16 → gain 3.0x → clamp → mono→stereo
                   ↓
                   PyAudio → VB-Cable → Discord

HTTP + WSS ทั้งหมดบน port 8443 → iOS cert trust ตรงกัน
```

ทุกเทคนิคถูกออกแบบมาแก้ปัญหาเฉพาะที่เจอบน iOS + VB-Cable  
ไม่มีเทคนิคไหน "เว่อร์" — ทุกบรรทัดมีที่มาที่ไป 😊

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
