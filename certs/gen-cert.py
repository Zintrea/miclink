"""Generate a self-signed certificate for miclink HTTPS/WSS.

Usage:
    python certs/gen-cert.py [--ip 172.20.10.2]

If --ip is omitted, auto-detects from ipconfig output.

Output:
    certs/server.pem   — Combined cert + private key for Python ssl
    certs/server.crt   — Certificate only (for manual install on iPad)
"""
import os
import re
import subprocess
import sys
import argparse

CERT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "certs")
CERT_PEM = os.path.join(CERT_DIR, "server.pem")
CERT_CRT = os.path.join(CERT_DIR, "server.crt")
KEY_FILE = os.path.join(CERT_DIR, "server.key")


def check_openssl():
    try:
        subprocess.run(["openssl", "version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def detect_ip():
    """Auto-detect local IP address from ipconfig (Windows) or ip (Linux/WSL)."""
    try:
        # Try Windows ipconfig first
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            m = re.search(r"IPv4 Address[^:]*:\s*(\d+\.\d+\.\d+\.\d+)", line)
            if m:
                ip = m.group(1)
                parts = ip.split(".")
                if parts[0] in ("192", "10") or (parts[0] == "172" and 16 <= int(parts[1]) <= 31):
                    return ip
    except FileNotFoundError:
        pass

    # Fallback: try Linux/WSL ip command
    try:
        result = subprocess.run(["ip", "-4", "addr", "show"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            m = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", line)
            if m:
                ip = m.group(1)
                if ip.startswith("127."):
                    continue
                parts = ip.split(".")
                if parts[0] in ("192", "10") or (parts[0] == "172" and 16 <= int(parts[1]) <= 31):
                    return ip
    except FileNotFoundError:
        pass

    return None


def generate_cert(ip_addresses):
    """Generate a self-signed cert with SAN for the given IPs."""
    os.makedirs(CERT_DIR, exist_ok=True)

    ips = list(dict.fromkeys(ip_addresses))  # deduplicate, preserve order

    # Build SAN entries
    san_lines = []
    san_lines.append("IP.1 = 127.0.0.1")
    san_lines.append("DNS.1 = localhost")
    for i, ip in enumerate(ips, start=2):
        san_lines.append(f"IP.{i} = {ip}")
    san_str = "\n".join(san_lines)

    config = f"""[req]
default_bits = 2048
prompt = no
default_md = sha256
x509_extensions = v3_req
distinguished_name = dn

[dn]
C = TH
O = miclink
CN = miclink.local

[v3_req]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[alt_names]
{san_str}
"""

    config_path = os.path.join(CERT_DIR, "san.conf")
    with open(config_path, "w") as f:
        f.write(config)

    # Generate private key + self-signed cert
    subprocess.run(
        ["openssl", "req", "-x509", "-nodes", "-days", "3650",
         "-newkey", "rsa:2048",
         "-keyout", KEY_FILE,
         "-out", CERT_CRT,
         "-config", config_path],
        check=True,
    )

    # Combine into PEM (key + cert) for Python ssl
    with open(CERT_PEM, "wb") as out:
        with open(KEY_FILE, "rb") as key:
            out.write(key.read())
        with open(CERT_CRT, "rb") as crt:
            out.write(crt.read())

    # Clean up config
    os.remove(config_path)

    print(f"✅ Certificate regenerated! SAN IPs: {', '.join(ips)}")
    print(f"   Server PEM: {CERT_PEM}")
    print(f"   Expires: 10 years")
    print()
    print("📱 On your iPad:")
    print(f"   1. Open Safari → https://<IP>:8443/web-client.html")
    print(f"   2. Tap 'Show Details' → 'Visit This Website'")
    print(f"   3. Enter IP: {ips[0] if ips else '<YOUR_IP>'}")
    print(f"   4. Tap Start Microphone — pop-up should appear! ✅")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SSL cert for miclink")
    parser.add_argument("--ip", type=str, default=None,
                        help="Your PC's IP address (auto-detected if omitted)")
    args = parser.parse_args()

    if not check_openssl():
        print("❌ OpenSSL not found. Please install OpenSSL:")
        print("   - Windows: https://slproweb.com/products/Win32OpenSSL.html")
        print("   - Or use WSL (openssl is already installed)")
        sys.exit(1)

    ips = []
    if args.ip:
        ips.append(args.ip)
    detected = detect_ip()
    if detected:
        ips.append(detected)

    if not ips:
        print("❌ Could not detect IP. Please specify manually:")
        print("   python certs/gen-cert.py --ip 172.20.10.2")
        sys.exit(1)

    generate_cert(ips)
