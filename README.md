# 🎙️ miclink — ไมค์มือถือ ใช้บน PC แบบไร้สาย

> เปลี่ยน iPad / iPhone / Android ให้เป็นไมโครโฟนคุณภาพสูงสำหรับ Discord, OBS, Zoom
> โดยไม่ต้องซื้ออุปกรณ์เพิ่มเลยสักบาท

```
ไมค์ iPad → Safari → WebSocket (WSS) → Python Server → VB-Cable → Discord/OBS/Zoom
```

---

## ⚡ Quick Start (iOS)

```
1. pip install -r requirements.txt
2. python certs/gen-cert.py                    # ครั้งแรกครั้งเดียว
3. python audio-server.py --secure --device 27  # รัน server
```

→ เปิด Safari ที่ `https://172.20.10.2:8443/web-client.html` บน iPad

> ดูวิธีละเอียด + แก้ปัญหา → [`docs/GUIDE.md`](docs/GUIDE.md)

---

## 🏗️ Tech Stack (หนึ่งบรรทัดต่อตัว)

| เทคโนโลยี | หน้าที่ |
|----------|--------|
| **Python + websockets** | รับเสียงผ่าน WebSocket, จัดการ HTTPS และ WSS ในพอร์ตเดียว |
| **PyAudio** | ส่งเสียงออกไปยัง VB-Cable |
| **VB-Cable** | สายเสียงเสมือน — ทำให้ Discord/OBS คิดว่ามีไมค์ใหม่เสียบ |
| **HTML5 Web Audio API** | จับเสียงจากไมค์ iPad ในเบราว์เซอร์ (ScriptProcessorNode) |

---

## 📖 Docs

| ไฟล์ | เนื้อหา |
|------|--------|
| [`docs/GUIDE.md`](docs/GUIDE.md) | **คู่มือผู้ใช้** — ตั้งค่า .env, เชื่อมต่อมือถือ, ใช้ใน Discord, แก้ปัญหา |
| [`docs/DEVELOP.md`](docs/DEVELOP.md) | **เบื้องหลัง** — เรื่องราวการพัฒนา + วิธีการทำงานของแต่ละเทคนิค |
| [`docs/KNOWLEDGE.md`](docs/KNOWLEDGE.md) | **ความรู้เทคนิคสั้น ๆ** — ปัญหาที่เจอและวิธีแก้ |

---

## 📜 License

MIT — ทำอะไรก็ได้ตามสบาย 😊
