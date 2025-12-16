import sqlite3

db_file = "src/data/jumia_data.db"
conn = sqlite3.connect(db_file)

# Check dates in database
query = """
SELECT date_scraped, COUNT(*) as count 
FROM products 
GROUP BY date_scraped 
ORDER BY date_scraped
"""

import pandas as pd
df = pd.read_sql_query(query, conn)
print("Dates in database:")
print(df)

conn.close()