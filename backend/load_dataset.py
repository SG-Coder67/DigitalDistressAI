import sqlite3
import csv
from urllib.parse import urlparse
import os

DB_FILE = "threats.db"
CSV_FILE = "malicious_phish.csv"

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# This CREATE TABLE command includes the 'source' column, which is essential.
cursor.execute("""
CREATE TABLE threats (
    domain TEXT PRIMARY KEY,
    threat_type TEXT NOT NULL,
    source TEXT NOT NULL  --  <-- This column must exist
);
""")
cursor.execute("CREATE INDEX idx_domain ON threats (domain);")

print(f"Loading data from {CSV_FILE} into {DB_FILE}...")
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    count = 0
    for row in reader:
        try:
            url, threat_type = row[0], row[1]
            if threat_type != "benign":
                domain = urlparse(url).netloc.lower()
                if domain:
                    # We add 'static_dataset' as the source for all initial threats
                    cursor.execute("INSERT OR IGNORE INTO threats (domain, threat_type, source) VALUES (?, ?, ?)", (domain, threat_type, 'static_dataset'))
                    count += 1
        except Exception:
            continue

conn.commit()
conn.close()

print(f"Done. Loaded {count} harmful domains into the database.")