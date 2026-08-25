import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from alert_manager import raise_alert, Severity

HONEYTOKEN_DIR = os.path.join(os.path.dirname(__file__), "honeytokens")

FAKE_CREDENTIALS_CONTENT = """\
# WARNING: internal use only
AWS_ACCESS_KEY_ID=AKIAFAKEKEYDONOTUSE00
AWS_SECRET_ACCESS_KEY=fAkEs3cr3tKeyForHoneytokenDemoPurpose0nly
DB_HOST=internal-db.local
DB_USER=svc_backup
DB_PASSWORD=SuperS3cretBackupPass!
"""


def deploy_honeytokens():
    """Buat folder + file umpan. Dipanggil sekali saat sistem start."""
    os.makedirs(HONEYTOKEN_DIR, exist_ok=True)
    path = os.path.join(HONEYTOKEN_DIR, "aws_credentials.txt")
    with open(path, "w") as f:
        f.write(FAKE_CREDENTIALS_CONTENT)
    print(f"[honeytoken] Decoy file deployed at: {path}")
    return path


class _HoneytokenEventHandler(FileSystemEventHandler):
    def _alert(self, event_type, path):
        raise_alert(
            source="honeytoken",
            event_type=event_type,
            detail=f"File umpan disentuh: {path}",
            severity=Severity.CRITICAL,
        )

    def on_modified(self, event):
        if not event.is_directory:
            self._alert("FILE_MODIFIED", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._alert("FILE_MOVED_OR_RENAMED", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self._alert("FILE_DELETED", event.src_path)


class HoneytokenMonitor:
    """Wrapper untuk start/stop observer watchdog di folder honeytoken."""

    def __init__(self, watch_dir=HONEYTOKEN_DIR):
        self.watch_dir = watch_dir
        self._observer = Observer()

    def start(self):
        os.makedirs(self.watch_dir, exist_ok=True)
        handler = _HoneytokenEventHandler()
        self._observer.schedule(handler, self.watch_dir, recursive=False)
        self._observer.start()
        print(f"[honeytoken] Monitoring folder: {self.watch_dir}")

    def stop(self):
        self._observer.stop()
        self._observer.join(timeout=2)


if __name__ == "__main__":
    deploy_honeytokens()
    monitor = HoneytokenMonitor()
    monitor.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()