# miclink 🎙️

Stream your iPad/iPhone/Android microphone to your PC in high quality (48kHz PCM16)
via WebSocket — no cables, no compression, no paid apps.

```
iPad mic → Browser (getUserMedia) → WebSocket → Python Server → VB-Cable → Discord/OBS/etc.
```

## How it works

1. **Python server** runs on your Windows PC, listens for WebSocket connections
2. **Browser page** on your iPad/phone captures raw mic audio (48kHz, no processing)
3. Audio streams over WiFi as uncompressed PCM16
4. Server outputs to **Virtual Audio Cable (VB-Cable)**
5. Any Windows app sees VB-Cable as a microphone input

## Requirements

- **Windows PC** with Python 3.10+
- **VB-Cable** (free): https://vb-audio.com/Cable/
- iPad/iPhone/Android on the **same WiFi network**

## Quick Start

### 1. Install VB-Cable
Download from https://vb-audio.com/Cable/ → Run installer → Restart PC

### 2. Install Python dependencies
```cmd
pip install -r requirements.txt
```

### 3. Check available audio devices
```cmd
python audio-server.py --list-devices
```
Look for "CABLE Output" in the list and note its index number.

### 4. Start the server
```cmd
python audio-server.py --device <INDEX>
```
Or without `--device` to use your default output (for testing).

### 5. Serve the web client
```cmd
python -m http.server 8000
```

### 6. Connect from iPad/Phone
1. Open Safari/Chrome on your device
2. Go to `http://<PC_IP_ADDRESS>:8000/web-client.html`
3. Enter your PC's IP address
4. Tap **Start Microphone**
5. Allow microphone access

### 7. Use in your app
Set your app's microphone input to "CABLE Input".

## Commands

| Command | Description |
|---|---|
| `python audio-server.py` | Start with default output device |
| `python audio-server.py --device 3` | Start with specific device index |
| `python audio-server.py --find-device "CABLE"` | Find device index by name |
| `python audio-server.py --list-devices` | List all output devices |
| `python audio-server.py --port 9000` | Use a different port |

## Tips

- **For lowest latency:** Use a wired connection or 5GHz WiFi
- **iPad Safari:** Works great — just allow mic access when prompted
- **Android Chrome:** Also supported
- **Windows Firewall:** May ask to allow Python on first run — click Allow
- **Bitrate:** ~768 kbps (48kHz × 16-bit × 1 channel)
