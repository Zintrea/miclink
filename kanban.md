# 🎙️ miclink — Project Kanban

> Workflow: **Trige** → **Todo** → **Ready** → **In Process**
>
> - **Trige** (⚡) = ไอเดีย ยังต้อง proof / หาความเป็นไปได้
> - **Todo** (📋) = สิ่งที่อยากทำ
> - **Ready** (✅) = พร้อมเริ่มทำ (defined + validated)
> - **In Process** (🔄) = กำลังทำ

---

## ⚡ Trige — ต้อง proof ก่อน

- [ ] **🌐 Auto-discovery (mDNS/Bonjour)**
  ค้นหา server อัตโนมัติ — ไม่ต้องพิมพ์ IP
  `effort: ⭐⭐⭐` `impact: 🔥🔥🔥🔥🔥`
- [ ] **🌊 WebRTC**
  latency ต่ำกว่า WebSocket, ปรับ bitrate อัตโนมัติ, echo cancellation ในตัว
  `effort: ⭐⭐⭐⭐` `impact: 🔥🔥🔥🔥🔥`
- [ ] **👥 Multi-client**
  รองรับหลาย iPad / มือถือพร้อมกัน
  `effort: ⭐⭐⭐` `impact: 🔥🔥🔥🔥🔥`

---

## 📋 Todo — อยากทำ

- [ ] **🔬 AudioWorklet**
  แทน ScriptProcessorNode → latency ต่ำกว่า, CPU น้อยกว่า, iOS quirks หาย
  `effort: ⭐⭐` `impact: 🔥🔥🔥🔥🔥`
- [ ] **🔇 Noise Gate**
  ตัดเสียงเงียบ/พื้นหลังอัตโนมัติ — เพื่อนใน Discord ได้ยินชัดขึ้น
  `effort: ⭐⭐` `impact: 🔥🔥🔥🔥`
- [ ] **📦 Portable executable (PyInstaller)**
  .exe ไฟล์เดียว — ไม่ต้องติดตั้ง Python
  `effort: ⭐⭐` `impact: 🔥🔥🔥🔥`
- [ ] **🔗 Server Dashboard**
  แสดง clients, bitrate, audio level, status
  `effort: ⭐` `impact: 🔥🔥🔥`
- [ ] **🧠 Adaptive Buffer**
  ปรับ buffer size อัตโนมัติตาม network
  `effort: ⭐⭐⭐` `impact: 🔥🔥🔥`

---

## ✅ Ready — พร้อมทำ

- [ ] **🎚️ Volume Slider บน iPad**
  ปรับ gain แบบ real-time จากหน้าเว็บ — ไม่ต้อง restart server
  `effort: ⭐` `impact: 🔥🔥🔥`
- [ ] **📊 VU Meter**
  แสดงระดับเสียง animation บน iPad
  `effort: ⭐` `impact: 🔥🔥🔥🔥`
- [ ] **📱 PWA (Installable App)**
  manifest.json + service worker → Add to Home Screen
  `effort: ⭐` `impact: 🔥🔥🔥🔥🔥`

---

## 🔄 In Process — กำลังทำ

*— ไม่มีอะไรกำลังทำตอนนี้ —*
