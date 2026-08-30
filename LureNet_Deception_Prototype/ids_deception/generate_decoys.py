import os
import csv
import random
import sqlite3

DECOY_DIR = os.path.join(os.path.dirname(__file__), "honeytokens")

FAKE_NAMES = [
    "Budi Santoso", "Siti Rahmawati", "Andi Wijaya", "Dewi Lestari",
    "Rian Pratama", "Nadia Putri", "Fajar Hidayat", "Maya Anggraini",
    "Teguh Setiawan", "Ika Kurniawati",
]

FAKE_DEPARTMENTS = ["Finance", "HR", "IT", "Sales", "Operations"]


def generate_fake_documents():
    """Bikin file dokumen palsu yang realistis di folder decoy."""
    os.makedirs(DECOY_DIR, exist_ok=True)
    created = []

    # 1. Data gaji karyawan (CSV)
    csv_path = os.path.join(DECOY_DIR, "Data_Gaji_Karyawan_2026.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["No", "Nama", "Departemen", "Gaji_Pokok", "Bonus"])
        for i, name in enumerate(FAKE_NAMES, start=1):
            writer.writerow([
                i, name, random.choice(FAKE_DEPARTMENTS),
                random.randint(6_000_000, 15_000_000),
                random.randint(0, 3_000_000),
            ])
    created.append(csv_path)
    print(f"[decoy] Fake document deployed at: {csv_path}")

    # 2. Laporan keuangan (TXT, biar kelihatan seperti draft internal)
    txt_path = os.path.join(DECOY_DIR, "Laporan_Keuangan_Q3_2026.txt")
    with open(txt_path, "w") as f:
        f.write(
            "INTERNAL - JANGAN DISEBARKAN\n"
            "Laporan Keuangan Kuartal 3 2026\n"
            "================================\n"
            f"Total Pendapatan: Rp {random.randint(800_000_000, 2_000_000_000):,}\n"
            f"Total Pengeluaran: Rp {random.randint(500_000_000, 1_500_000_000):,}\n"
            "Catatan: draft, belum diaudit. Hubungi tim finance untuk versi final.\n"
        )
    created.append(txt_path)
    print(f"[decoy] Fake document deployed at: {txt_path}")

    return created


def generate_fake_database():
    """Bikin database SQLite palsu berisi data customer dummy."""
    os.makedirs(DECOY_DIR, exist_ok=True)
    db_path = os.path.join(DECOY_DIR, "customers_backup.db")

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            nama TEXT,
            email TEXT,
            no_kartu TEXT,
            saldo INTEGER
        )
        """
    )
    for i, name in enumerate(FAKE_NAMES, start=1):
        email = name.lower().replace(" ", ".") + "@fakemail.com"
        fake_card = f"4{random.randint(100000000000000, 999999999999999)}"
        cur.execute(
            "INSERT INTO customers (id, nama, email, no_kartu, saldo) VALUES (?, ?, ?, ?, ?)",
            (i, name, email, fake_card, random.randint(1_000_000, 50_000_000)),
        )
    conn.commit()
    conn.close()

    print(f"[decoy] Fake database deployed at: {db_path}")
    return db_path


def deploy_all_document_decoys():
    """Dipanggil dari main.py saat startup, sejalan dengan deploy_honeytokens()."""
    docs = generate_fake_documents()
    db = generate_fake_database()
    return docs + [db]


if __name__ == "__main__":
    deploy_all_document_decoys()
