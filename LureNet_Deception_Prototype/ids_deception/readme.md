# Deception-based Intrusion Detection System (Prototype)

Prototype sederhana untuk project Intrusion Detection menggunakan **deception**
(honeypot + honeytoken). Ditujukan untuk demo lokal/local simulation.

## Arsitektur

```
ids_deception/
├── alert_manager.py       # Pusat logging & severity level semua alert
├── honeypot.py             # Fake SSH service (port 2222) + fake admin panel HTTP (port 8080)
├── honeytoken_monitor.py   # Membuat & memonitor file umpan (fake AWS credentials)
├── main.py                 # Entry point: menyalakan semua sensor
├── simulate_attack.py      # Script simulasi penyerang untuk demo
└── logs/alerts.log         # Log semua alert (dibuat otomatis saat main.py jalan)
```

**Prinsip deception:** semua "layanan" dan "file" di sini adalah umpan yang
tidak pernah dipakai user/aplikasi sah. Karena itu, SETIAP interaksi ke
komponen ini (siapapun yang connect, login, atau buka file) otomatis
dianggap indikasi kuat adanya intrusion — beda dari IDS berbasis
signature/anomaly biasa yang rawan false positive.

| Komponen | Jenis Deception | Yang dideteksi |
|---|---|---|
| `FakeSSHHoneypot` | Honeypot service | Koneksi & percobaan login (username/password) |
| `FakeAdminPanel` | Honeypot service | Akses halaman & percobaan login admin palsu |
| Honeytoken file (`aws_credentials.txt`) | Honeytoken | File dimodifikasi/dipindah/dihapus |

## Cara Menjalankan (Demo)

Butuh 2 terminal:

**Terminal 1 — jalankan sistem deteksi:**
```bash
cd ids_deception
python3 main.py
```

**Terminal 2 — simulasikan serangan:**
```bash
cd 
python3 simulate_attack.py
```

Di Terminal 1 kamu akan lihat alert muncul real-time dengan warna sesuai
severity (biru=LOW, kuning=MEDIUM, merah=HIGH, magenta=CRITICAL). Semua
alert juga tersimpan permanen di `logs/alerts.log`.

## Dependency

- Python 3.10+ (pakai `str | None` type hint)
- `watchdog` (`pip install watchdog`) — untuk monitoring file honeytoken

## Ide Pengembangan Lanjutan

Beberapa arah yang bisa dikembangkan sesuai kebutuhan laporan/kelompok:
- **Dashboard web** (Flask/FastAPI) untuk visualisasi alert real-time, bukan cuma CLI.
- **Notifikasi eksternal** (email/Telegram bot) saat alert CRITICAL muncul.
- **Lebih banyak jenis honeypot** (FTP, Telnet, database palsu/MySQL honeypot).
- **Integrasi dengan iptables/firewall** untuk auto-block IP penyerang.
- **Scoring/correlation engine** — kalau IP yang sama kena beberapa alert dalam
  waktu singkat, naikkan severity otomatis (indikasi serangan terkoordinasi).
- **Containerize** tiap honeypot pakai Docker biar lebih realistis & terisolasi.