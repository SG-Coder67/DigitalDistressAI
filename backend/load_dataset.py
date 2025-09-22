# Save this as: backend/load_dataset.py
import sqlite3
import csv
from urllib.parse import urlparse
import os

# Save the database in the same folder as the script
DB_FILE = "threats.db" 
CSV_FILE = "malicious_phish.csv"

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# Connect to SQLite database (it will be created)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create a table to store threats
cursor.execute("""
CREATE TABLE threats (
    domain TEXT PRIMARY KEY,
    threat_type TEXT NOT NULL
);
""")

# Create an index on the domain column for super-fast lookups
cursor.execute("CREATE INDEX idx_domain ON threats (domain);")

print(f"Loading data from {CSV_FILE} into {DB_FILE}...")
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    count = 0
    for row in reader:
        try:
            url, threat_type = row[0], row[1]
            if threat_type != "benign":
                domain = urlparse(url).netloc.lower()
                if domain:
                    cursor.execute("INSERT OR IGNORE INTO threats (domain, threat_type) VALUES (?, ?)", (domain, threat_type))
                    count += 1
        except Exception:
            # This will skip any malformed rows in your CSV file
            continue

conn.commit()
conn.close()

print(f"Done. Loaded {count} harmful domains into the database.")