import sqlite3

db_file = "src/data/jumia_data.db"
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Count total rows
c.execute("SELECT COUNT(*) FROM products")
total = c.fetchone()[0]
print(f"Total rows: {total}")

# Count unique combinations
c.execute("""
    SELECT COUNT(*) FROM (
        SELECT DISTINCT name, url, date_scraped FROM products
    )
""")
unique = c.fetchone()[0]
print(f"Unique (name, url, date) combinations: {unique}")
print(f"Duplicates to remove: {total - unique}")

conn.close()