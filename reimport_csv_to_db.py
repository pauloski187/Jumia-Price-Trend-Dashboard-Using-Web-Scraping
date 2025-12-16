
import sqlite3
import pandas as pd
import os

# Paths
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(_SCRIPT_DIR, "src/data/jumia_data.db")
csv_file = os.path.join(_SCRIPT_DIR, "data/raw/jumia_product.csv")

print("=" * 80)
print("RE-IMPORTING CSV TO DATABASE")
print("=" * 80)

# Read CSV
print(f"\n📂 Reading CSV: {csv_file}")
df = pd.read_csv(csv_file)
print(f"   CSV has {len(df)} rows")

# Check date distribution
print("\n📅 Date distribution in CSV:")
date_counts = df['Date Scraped'].value_counts().sort_index()
for date, count in date_counts.items():
    print(f"   {date}: {count} products")

# Connect to database
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Clear database (optional - only if you want fresh start)
answer = input("\n⚠️  Clear existing database before import? (yes/no): ").strip().lower()
if answer in ("y", "yes"):
    c.execute("DELETE FROM products")
    conn.commit()
    print(f"   Cleared {conn.total_changes} existing rows")

# Import CSV to database
print("\n📥 Importing CSV to database...")
inserted = 0
skipped = 0

for idx, row in df.iterrows():
    try:
        c.execute('''
            INSERT OR IGNORE INTO products 
            (category, name, url, current_price, original_price, discount, rating, stock, date_scraped)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
                      row['Category'],
                      row['Name'],
                      row['URL'],
                      row['Current Price'],
                      row['Original Price'],
                      row['Discount'],
                      row['Rating'] if pd.notna(row['Rating']) else 'N/A',
                      row['Stock'],
                      row['Date Scraped']
        ))

        if c.rowcount > 0:
            inserted += 1
        else:
            skipped += 1

    except Exception as e:
        print(f"   ⚠️  Error on row {idx}: {e}")

conn.commit()

# Verify import
c.execute("SELECT COUNT(*) FROM products")
total_db = c.fetchone()[0]

c.execute("""
    SELECT date_scraped, COUNT(*) 
    FROM products 
    GROUP BY date_scraped 
    ORDER BY date_scraped
""")
db_dates = c.fetchall()

conn.close()

print("\n" + "=" * 80)
print("IMPORT SUMMARY")
print("=" * 80)
print(f"✅ Rows inserted: {inserted}")
print(f"⏭️  Rows skipped (duplicates): {skipped}")
print(f"✅ Total in database: {total_db}")
print(f"\n📅 Date distribution in database:")
for date, count in db_dates:
    print(f"   {date}: {count} products")

print("\n✅ Import complete!")
