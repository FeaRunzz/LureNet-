
import os
import shutil
import socket
import time

import urllib.request

SSH_PORT = 2222
HTTP_PORT = 8080
TARGET_HOST = "127.0.0.1"

HONEYTOKEN_DIR = os.path.join(os.path.dirname(__file__), "honeytokens")


def simulate_ssh_bruteforce():
    print("\n[attacker] Mencoba login ke fake SSH service...")
    creds = [("admin", "admin123"), ("root", "toor")]
    for user, pwd in creds:
        try:
            s = socket.create_connection((TARGET_HOST, SSH_PORT), timeout=3)
            s.recv(1024)  # banner
            s.sendall((user + "\n").encode())
            s.recv(1024)  # password prompt
            s.sendall((pwd + "\n").encode())
            s.recv(1024)
            s.close()
            print(f"[attacker]  -> mencoba {user}:{pwd}")
            time.sleep(0.5)
        except (ConnectionRefusedError, socket.timeout):
            print("[attacker] Gagal connect ke honeypot SSH. Pastikan main.py sudah jalan.")
            return


def simulate_http_probe():
    print("\n[attacker] Mengakses fake admin panel via HTTP...")
    try:
        urllib.request.urlopen(f"http://{TARGET_HOST}:{HTTP_PORT}/", timeout=3)
        data = b"user=admin&pass=letmein123"
        req = urllib.request.Request(
            f"http://{TARGET_HOST}:{HTTP_PORT}/login", data=data, method="POST"
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception as e:
        # 401 dari server juga masuk sini karena urllib treat non-2xx as error,
        # itu normal & tetap kecatat sebagai alert di sisi server.
        print(f"[attacker]  -> request terkirim (server merespon: {e})")


def simulate_honeytoken_theft():
    print("\n[attacker] Menemukan file mencurigakan, mencoba mengambilnya...")
    src = os.path.join(HONEYTOKEN_DIR, "aws_credentials.txt")
    dst = os.path.join(HONEYTOKEN_DIR, "aws_credentials_stolen.txt")
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"[attacker]  -> file dipindahkan ke {dst}")
        # kembalikan lagi biar demo bisa diulang
        time.sleep(1)
        shutil.move(dst, src)
    else:
        print("[attacker] Honeytoken tidak ditemukan. Pastikan main.py sudah jalan.")


if __name__ == "__main__":
    print("=" * 60)
    print(" SIMULASI SERANGAN (untuk demo deception-based IDS)")
    print("=" * 60)
    simulate_ssh_bruteforce()
    simulate_http_probe()
    simulate_honeytoken_theft()
    print("\n[attacker] Simulasi selesai. Cek terminal main.py untuk lihat alert.")