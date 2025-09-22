import sqlite3
import csv
from urllib.parse import urlparse
import os

DB_FILE = "threats.db"
CSV_FILE = "malicious_phish.csv"

# Delete old database file if it exists
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

# Create an index for super-fast lookups
cursor.execute("CREATE INDEX idx_domain ON threats (domain);")

print(f"Loading data from {CSV_FILE} into {DB_FILE}...")
# Read the CSV and insert data into the database
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    count = 0
    for row in reader:
        try:
            url, threat_type = row
            if threat_type != "benign": # We only need to store the harmful ones
                domain = urlparse(url).netloc.lower()
                if domain:
                    # Use INSERT OR IGNORE to avoid errors on duplicate domains
                    cursor.execute("INSERT OR IGNORE INTO threats (domain, threat_type) VALUES (?, ?)", (domain, threat_type))
                    count += 1
        except Exception as e:
            # print(f"Skipping malformed row: {row}, error: {e}")
            continue

conn.commit()
conn.close()

print(f"Done. Loaded {count} harmful domains into the database.")