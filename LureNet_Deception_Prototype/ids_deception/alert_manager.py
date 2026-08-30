import logging
import os
from datetime import datetime
from enum import Enum


class Severity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Warna ANSI biar output di terminal gampang dibaca saat demo
_COLOR = {
    Severity.LOW: "\033[94m",       # biru
    Severity.MEDIUM: "\033[93m",    # kuning
    Severity.HIGH: "\033[91m",      # merah
    Severity.CRITICAL: "\033[95m",  # magenta
}
_RESET = "\033[0m"

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "alerts.log")

# Format timestamp dengan presisi milidetik -- penting supaya metrik
# time-to-detection di simulate_attack.py bisa dihitung akurat (sebelumnya
# cuma presisi detik, jadi banyak event yang keliatan "0 detik" padahal beda).
TS_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

# Logger file (plain text, tanpa warna, biar gampang diparse/dianalisis)
_file_logger = logging.getLogger("ids_deception.alerts")
_file_logger.setLevel(logging.INFO)
_fh = logging.FileHandler(LOG_FILE)
_fh.setFormatter(logging.Formatter("%(message)s"))
if not _file_logger.handlers:
    _file_logger.addHandler(_fh)


def raise_alert(source: str, event_type: str, detail: str,
                 severity: Severity = Severity.MEDIUM,
                 src_ip: str | None = None):
    """
    Catat satu alert intrusion/deception.

    source     : nama sensor yang mendeteksi, misal "honeypot-ssh", "honeytoken-document"
    event_type : jenis kejadian, misal "CONNECTION", "LOGIN_ATTEMPT", "FILE_ACCESS"
    detail     : deskripsi bebas (username yang dicoba, path file, dll)
    severity   : level keparahan (enum Severity)
    src_ip     : IP sumber kalau relevan (None kalau tidak ada, misal file access lokal)
    """
    timestamp = datetime.now().strftime(TS_FORMAT)[:-3]  # potong ke milidetik
    ip_part = f" | src={src_ip}" if src_ip else ""
    line = f"[{timestamp}] [{severity.value}] [{source}] {event_type}{ip_part} -> {detail}"

    # Tulis ke file log (permanen, buat laporan/analisis)
    _file_logger.info(line)

    # Tampilkan ke console dengan warna (buat demo real-time)
    color = _COLOR.get(severity, "")
    print(f"{color}{line}{_RESET}")


def read_recent_alerts(n: int = 20):
    """Ambil n alert terakhir dari file log, buat ditampilin di dashboard/CLI."""
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines[-n:]]
