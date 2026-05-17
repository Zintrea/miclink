"""Generate a self-signed certificate for miclink HTTPS/WSS.

Usage:
    python gen-cert.py

Output:
    certs/server.pem   — Combined cert + private key for Python ssl
    certs/server.crt   — Certificate only (for manual install on iPad)
"""
import os
import subprocess
import sys

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


def generate_cert():
    """Generate a self-signed cert with SAN for IP addresses (172.x, 192.168.x, 10.x)."""
    os.makedirs(CERT_DIR, exist_ok=True)

    # Config for Subject Alternative Name (required for IP access on iOS)
    config = """[req]
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
IP.1 = 0.0.0.0
IP.2 = 127.0.0.1
DNS.1 = localhost
"""

    config_path = os.path.join(CERT_DIR, "san.conf")
    with open(config_path, "w") as f:
        f.write(config)

    # Generate private key + self-signed cert in one command
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

    print(f"✅ Certificate generated!")
    print(f"   Server PEM: {CERT_PEM}")
    print(f"   Certificate: {CERT_CRT}")
    print(f"   Expires: 10 years")
    print()
    print("📱 On your iPad:")
    print("   1. Open Safari and go to https://<IP>:8443/web-client.html")
    print("   2. Tap 'Show Details' → 'Visit This Website' (accept the warning)")
    print("   3. Done! The cert warning only shows once.")


if __name__ == "__main__":
    if not check_openssl():
        print("❌ OpenSSL not found. Please install OpenSSL:")
        print("   - Windows: https://slproweb.com/products/Win32OpenSSL.html")
        print("   - Or use WSL (openssl is already installed)")
        sys.exit(1)

    if os.path.exists(CERT_PEM):
        print("📄 Certificate already exists. Delete certs/ to regenerate.")
    else:
        generate_cert()
