import os
import sys
import logging
import sqlite3
import pandas as pd

# One-time migration: import all existing CSV history into SQLite DB
# Assumptions per requirements:
# - Script is located in the same directory as the target DB file
# - DB file name: jumia_data.db
# - CSV relative path must remain: ../../data/raw/jumia_product.csv

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Keep DB file in the same directory as this script
DB_FILE = os.path.join(_SCRIPT_DIR, "jumia_data.db")
# Keep CSV path as ../../data/raw/jumia_product.csv relative to this script
CSV_FILE = os.path.normpath(os.path.join(_SCRIPT_DIR, "../../data/raw/jumia_product.csv"))


def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def setup_db(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            name TEXT,
            url TEXT,
            current_price TEXT,
            original_price TEXT,
            discount TEXT,
            rating TEXT,
            stock TEXT,
            date_scraped TEXT
        )
        '''
    )
    # Unique index to avoid duplicates for the same product on the same date
    c.execute(
        '''
        CREATE UNIQUE INDEX IF NOT EXISTS idx_products_unique
        ON products(name, url, date_scraped)
        '''
    )
    conn.commit()


def map_csv_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Map CSV columns to DB column names. CSV is expected to have Title Case headers.
    If columns are already snake_case, support them too."""
    # Try to detect column naming
    col_map_title = {
        "Category": "category",
        "Name": "name",
        "URL": "url",
        "Current Price": "current_price",
        "Original Price": "original_price",
        "Discount": "discount",
        "Rating": "rating",
        "Stock": "stock",
        "Date Scraped": "date_scraped",
    }
    if set(col_map_title.keys()).issubset(set(df.columns)):
        return df.rename(columns=col_map_title)

    # Fallback if already snake_case
    expected_snake = [
        "category",
        "name",
        "url",
        "current_price",
        "original_price",
        "discount",
        "rating",
        "stock",
        "date_scraped",
    ]
    if set(expected_snake).issubset(set(df.columns)):
        return df

    raise ValueError(
        "CSV headers are not recognized. Expected Title Case legacy headers or snake_case headers."
    )


def import_csv_to_db():
    if not os.path.exists(CSV_FILE):
        logging.error(f"CSV not found at {CSV_FILE}")
        sys.exit(1)

    conn = sqlite3.connect(DB_FILE)
    setup_db(conn)
    cur = conn.cursor()

    total_rows = 0
    inserted_rows = 0
    chunksize = 10_000
    logging.info("Starting migration from CSV to SQLite DB...")

    try:
        for i, chunk in enumerate(pd.read_csv(CSV_FILE, chunksize=chunksize)):
            chunk = map_csv_columns(chunk)
            # Ensure only required columns and fill NaNs with sensible defaults
            needed_cols = [
                "category",
                "name",
                "url",
                "current_price",
                "original_price",
                "discount",
                "rating",
                "stock",
                "date_scraped",
            ]
            chunk = chunk[needed_cols].fillna("")

            params = [
                (
                    r["category"],
                    r["name"],
                    r["url"],
                    r["current_price"],
                    r["original_price"],
                    r["discount"],
                    r["rating"],
                    r["stock"],
                    r["date_scraped"],
                )
                for _, r in chunk.iterrows()
            ]
            cur.executemany(
                '''
                INSERT OR IGNORE INTO products (
                    category, name, url, current_price, original_price, discount, rating, stock, date_scraped
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                , params
            )
            conn.commit()
            total_rows += len(chunk)
            # Count how many were newly inserted
            inserted = cur.rowcount if cur.rowcount is not None else 0
            inserted_rows += max(0, inserted)
            logging.info(f"Processed chunk {i+1}: {len(chunk)} rows (cumulative {total_rows})")

    except Exception as e:
        logging.exception(f"Migration failed: {e}")
        conn.close()
        sys.exit(1)

    # Final verification
    cur.execute("SELECT COUNT(1) FROM products")
    db_total = cur.fetchone()[0]
    cur.execute(
        "SELECT date_scraped, COUNT(1) FROM products GROUP BY date_scraped ORDER BY date_scraped"
    )
    breakdown = cur.fetchall()
    conn.close()

    logging.info("Migration complete.")
    logging.info(f"CSV rows seen: {total_rows}")
    logging.info(f"Rows inserted (new): {inserted_rows}")
    logging.info(f"Total rows in DB: {db_total}")
    logging.info("Breakdown by date:")
    for d, cnt in breakdown:
        logging.info(f" - {d}: {cnt}")


if __name__ == "__main__":
    init_logging()
    import_csv_to_db()
