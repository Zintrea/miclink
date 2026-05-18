# miclink — Debugging Knowledge

> ดูรายละเอียดทั้งหมด (ทุกปัญหาที่เจอ + วิธีแก้) ได้ที่ Obsidian vault:
>
> **`C:\Users\boony\Desktop\Iris\knowledge\miclink\01-debugging-journey.md`**
>
> หรือใน WSL: `/mnt/c/Users/boony/Desktop/Iris/knowledge/miclink/01-debugging-journey.md`

## สรุปสั้น ๆ — ปัญหาที่เจอ (3 sessions)

| # | ปัญหา | สาเหตุ | วิธีแก้ |
|---|-------|--------|--------|
| 1 | iOS mic pop-up ไม่ขึ้น | HTTP → getUserMedia ไม่ได้ | `--secure` (HTTPS) |
| 2 | WSS cert trust per-port | cert trust แยกตาม port | HTTP+WSS รวม port 8443 |
| 3 | streaming @ 0.0 kbps | iOS ScriptProcessor graph ไม่สมบูรณ์ | GainNode(0) ต่อ destination |
| 4 | Audio garbled (iOS) | onaudioprocess ตั้งช้า | callback ตั้งก่อน connect graph |
| 5 | VB-Cable mono = แตก | WASAPI mono→stereo แปลงห่วย | ส่ง stereo (L/R duplicate) |
| 6 | เสียงเบามาก | iPad mic raw level | autoGainControl + --gain 3.0 |
