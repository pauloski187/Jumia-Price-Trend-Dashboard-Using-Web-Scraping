import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import os
import sys
import logging
import pandas as pd

# 1️⃣ Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36"
}

# 2️⃣ All 65 categories
categories = {
    "Smartphones": "https://www.jumia.com.ng/smartphones/",
    "Computers & Tablets": "https://www.jumia.com.ng/computing/",
    "Laptops & Computers": "https://www.jumia.com.ng/laptops/",
    "TV & Video": "https://www.jumia.com.ng/televisions/",
    "Audio & Video": "https://www.jumia.com.ng/headphones-speakers/",
    "Cameras & Photography": "https://www.jumia.com.ng/cameras-video/",
    "Mobile Accessories": "https://www.jumia.com.ng/mobile-accessories/",
    "Computing Accessories": "https://www.jumia.com.ng/computing-accessories/",
    "Home Appliances": "https://www.jumia.com.ng/home-appliances/",
    "Kitchen Appliances": "https://www.jumia.com.ng/kitchen-appliances/",
    "Health & Beauty": "https://www.jumia.com.ng/health-beauty/",
    "Health & Personal Care": "https://www.jumia.com.ng/health-beauty/",
    "Automobile & Tools": "https://www.jumia.com.ng/automobile-tools/",
    "Pet Supplies": "https://www.jumia.com.ng/pet-supplies/",
    "Men Fashion": "https://www.jumia.com.ng/men-clothing/",
    "Women Fashion": "https://www.jumia.com.ng/women-clothing/",
    "Kids & Baby": "https://www.jumia.com.ng/baby-products/",
    "Shoes": "https://www.jumia.com.ng/shoes/",
    "Bags & Luggage": "https://www.jumia.com.ng/bags-luggage/",
    "Jewelry & Watches": "https://www.jumia.com.ng/jewellery-watches/",
    "Home & Living": "https://www.jumia.com.ng/home-furniture/",
    "Home Decor & Furnishing": "https://www.jumia.com.ng/home-furniture-decor/",
    "Garden & Outdoors": "https://www.jumia.com.ng/garden-outdoors/",
    "Home Improvement": "https://www.jumia.com.ng/home-improvement/",
    "Office Supplies": "https://www.jumia.com.ng/office-furniture/",
    "Groceries": "https://www.jumia.com.ng/groceries/",
    "Toys & Games": "https://www.jumia.com.ng/toys-games/",
    "Baby & Toys": "https://www.jumia.com.ng/baby-products/",
    "Sports & Outdoors": "https://www.jumia.com.ng/sports-outdoors/",
    "Books & Stationery": "https://www.jumia.com.ng/books-stationery/",
    "Gaming Consoles": "https://www.jumia.com.ng/gaming-consoles/",
    "Video Games": "https://www.jumia.com.ng/video-games/",
    "Smart Home": "https://www.jumia.com.ng/smart-home/",
    "Networking": "https://www.jumia.com.ng/networking/",
    "Storage Devices": "https://www.jumia.com.ng/storage-devices/",
    "Printers & Scanners": "https://www.jumia.com.ng/printers-scanners/",
    "Projectors": "https://www.jumia.com.ng/projectors/",
    "Musical Instruments": "https://www.jumia.com.ng/musical-instruments/",
    "Beverages": "https://www.jumia.com.ng/beverages/",
    "Snacks & Confectionery": "https://www.jumia.com.ng/snacks-confectionery/",
    "Cleaning Supplies": "https://www.jumia.com.ng/cleaning-supplies/",
    "Baby Food": "https://www.jumia.com.ng/baby-food/",
    "Diapers & Wipes": "https://www.jumia.com.ng/diapers-wipes/",
    "Maternity": "https://www.jumia.com.ng/maternity/",
    "Stationery": "https://www.jumia.com.ng/stationery/",
    "Party Supplies": "https://www.jumia.com.ng/party-supplies/",
    "Lighting & Lamps": "https://www.jumia.com.ng/lighting/",
    "Kitchenware": "https://www.jumia.com.ng/kitchenware/",
    "Furniture": "https://www.jumia.com.ng/furniture/",
    "Decorative Items": "https://www.jumia.com.ng/decorative-items/",
    "Watches": "https://www.jumia.com.ng/watches/",
    "Handbags": "https://www.jumia.com.ng/handbags/",
    "Sunglasses": "https://www.jumia.com.ng/sunglasses/",
    "Fitness Equipment": "https://www.jumia.com.ng/fitness-equipment/",
    "Camping & Hiking": "https://www.jumia.com.ng/camping-hiking/",
    "Cycling": "https://www.jumia.com.ng/cycling/",
    "Swimming": "https://www.jumia.com.ng/swimming/",
    "Car Care": "https://www.jumia.com.ng/car-care/",
    "Tools": "https://www.jumia.com.ng/tools/",
    "Industrial Supplies": "https://www.jumia.com.ng/industrial-supplies/"
}

# 3️⃣ Database & CSV setup
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Keep DB in the same directory as this script regardless of current working directory
db_file = os.path.join(_SCRIPT_DIR, "jumia_data.db")
# Keep CSV path as ../../data/raw/jumia_product.csv relative to this script
csv_file = os.path.normpath(os.path.join(_SCRIPT_DIR, "../../data/raw/jumia_product.csv"))


def setup_db():
    """Create the products table if it doesn't exist and add a unique index
    to prevent duplicate rows for the same product on the same date."""
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS products
              (
                  id
                  INTEGER
                  PRIMARY
                  KEY
                  AUTOINCREMENT,
                  category
                  TEXT,
                  name
                  TEXT,
                  url
                  TEXT,
                  current_price
                  TEXT,
                  original_price
                  TEXT,
                  discount
                  TEXT,
                  rating
                  TEXT,
                  stock
                  TEXT,
                  date_scraped
                  TEXT
              )
              ''')

    # Check if the unique index already exists
    c.execute("""
              SELECT name
              FROM sqlite_master
              WHERE type = 'index'
                AND name = 'idx_products_unique'
              """)
    index_exists = c.fetchone() is not None

    if not index_exists:
        logging.info("Unique index does not exist. Cleaning duplicates before creating it...")

        # Remove duplicates - keep only the row with the highest id (most recent insert)
        c.execute('''
                  DELETE
                  FROM products
                  WHERE id NOT IN (SELECT MAX(id)
                                   FROM products
                                   GROUP BY name, url, date_scraped)
                  ''')

        deleted_count = conn.total_changes
        if deleted_count > 0:
            logging.info(f"Removed {deleted_count} duplicate rows from database")

        # Now create the unique index safely
        c.execute('''
                  CREATE UNIQUE INDEX idx_products_unique
                      ON products (name, url, date_scraped)
                  ''')
        logging.info("Created unique index successfully")

    conn.commit()
    conn.close()


def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

# 4️⃣ Scrape function
def _today_date():
    return datetime.now().strftime("%Y-%m-%d")


def _db_has_today(conn, today):
    c = conn.cursor()
    c.execute("SELECT COUNT(1) FROM products WHERE date_scraped = ?", (today,))
    return c.fetchone()[0] > 0


def _delete_today_from_db(conn, today):
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE date_scraped = ?", (today,))
    conn.commit()


def _delete_today_from_csv(today):
    if not os.path.exists(csv_file):
        return 0
    try:
        df = pd.read_csv(csv_file)
        # Support both legacy and snake_case headers
        date_col = "Date Scraped" if "Date Scraped" in df.columns else ("date_scraped" if "date_scraped" in df.columns else None)
        if date_col is None:
            logging.warning("CSV does not contain a recognizable date column. Skipping CSV cleanup for today.")
            return 0
        before = len(df)
        df = df[df[date_col] != today]
        removed = before - len(df)
        df.to_csv(csv_file, index=False, encoding="utf-8")
        return removed
    except Exception as e:
        logging.error(f"Failed to clean today's rows from CSV: {e}")
        return 0


def _append_daily_to_csv(daily_rows):
    if not daily_rows:
        return False
    # Use legacy headers to preserve current CSV schema
    df_new = pd.DataFrame(daily_rows, columns=[
        "Category", "Name", "URL", "Current Price",
        "Original Price", "Discount", "Rating", "Stock", "Date Scraped"
    ])
    if os.path.exists(csv_file):
        try:
            df_existing = pd.read_csv(csv_file)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(csv_file, index=False, encoding="utf-8")
        except Exception as e:
            logging.error(f"Failed to append to CSV: {e}")
            return False
    else:
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(csv_file), exist_ok=True)
            df_new.to_csv(csv_file, index=False, encoding="utf-8")
        except Exception as e:
            logging.error(f"Failed to create CSV: {e}")
            return False
    return True


def _db_summary(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(1) FROM products")
    total = c.fetchone()[0]
    c.execute("SELECT date_scraped, COUNT(1) FROM products GROUP BY date_scraped ORDER BY date_scraped")
    breakdown = c.fetchall()
    return total, breakdown


def scrape_and_store():
    init_logging()
    setup_db()

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    today = _today_date()
    # Duplicate prevention and optional re-scrape
    if _db_has_today(conn, today):
        logging.info(f"Data for today ({today}) already exists in the database.")
        try:
            answer = input("Today's data already exists. Re-scrape and replace today's data? (yes/no): ").strip().lower()
        except EOFError:
            answer = "no"
        if answer in ("y", "yes"):
            _delete_today_from_db(conn, today)
            removed_csv = _delete_today_from_csv(today)
            logging.info(f"Removed existing {today} rows from DB and {removed_csv} rows from CSV. Proceeding to re-scrape...")
        else:
            total, breakdown = _db_summary(conn)
            logging.info("Exiting without scraping.")
            logging.info(f"Database total rows: {total}")
            for d, cnt in breakdown:
                logging.info(f" - {d}: {cnt}")
            conn.close()
            return

    daily_data = []  # store daily data for CSV

    for category_name, base_url in categories.items():
        logging.info(f"Scraping category: {category_name}")
        for page in range(1, 6):
            url = base_url + f"?page={page}"
            try:
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code != 200:
                    logging.warning(f"{category_name} page {page} returned {response.status_code}")
                    break
            except Exception as e:
                logging.error(f"Failed to fetch {url}: {e}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find_all("article", class_="prd _fb col c-prd")
            if not products:
                break

            for product in products:
                try:
                    name_tag = product.find("a", class_="core")
                    name = name_tag.text.strip() if name_tag else "N/A"
                    link = "https://www.jumia.com.ng" + name_tag["href"] if (name_tag and name_tag.get("href")) else "N/A"
                    current_price = product.find("div", class_="prc").text.strip() if product.find("div", class_="prc") else "N/A"
                    original_price = product.find("div", class_="old").text.strip() if product.find("div", class_="old") else current_price
                    # Try to read discount badge; if missing or 0%, compute from prices
                    discount = product.find("div", class_="bdg _dsct").text.strip() if product.find("div", class_="bdg _dsct") else None
                    # Helper to parse price text like "₦ 10,500" -> 10500.0
                    def _parse_price(text):
                        if not text or text == "N/A":
                            return None
                        # Keep digits and dot
                        import re
                        cleaned = re.sub(r"[^0-9.]", "", text)
                        try:
                            return float(cleaned) if cleaned else None
                        except Exception:
                            return None
                    # Compute discount if needed
                    needs_compute = (discount is None) or (discount.replace(" ", "").lower() in ("0%", "0pct", "0percent"))
                    if needs_compute:
                        cur_v = _parse_price(current_price)
                        orig_v = _parse_price(original_price)
                        if cur_v is not None and orig_v is not None and orig_v > 0 and orig_v >= cur_v:
                            pct = round((orig_v - cur_v) / orig_v * 100)
                            # Clamp to sensible range
                            if pct < 0:
                                pct = 0
                            if pct > 99:
                                pct = 99
                            discount = f"{pct}%"
                            logging.debug(f"Inferred discount {discount} for '{name}' from prices {orig_v} -> {cur_v}")
                        else:
                            # Fallback to 0% text if computation not possible
                            discount = "0%"
                    rating = product.find("div", class_="rev").text.strip() if product.find("div", class_="rev") else "N/A"
                    stock = "In Stock"
                    date_scraped = today

                    # Insert into DB (skip duplicates for same product and date)
                    c.execute('''
                        INSERT OR IGNORE INTO products (category, name, url, current_price, original_price, discount, rating, stock, date_scraped)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (category_name, name, link, current_price, original_price, discount, rating, stock, date_scraped))

                    # Append to daily_data for CSV
                    daily_data.append([category_name, name, link, current_price, original_price, discount, rating, stock, date_scraped])
                except Exception as e:
                    logging.error(f"Failed to scrape product: {e}")

            time.sleep(1)

    conn.commit()
    # Gather post-scrape stats before closing connection
    total, breakdown = _db_summary(conn)
    conn.close()

    # 5️⃣ Append to CSV (create if doesn't exist)
    csv_ok = _append_daily_to_csv(daily_data)

    # 6️⃣ Summary output
    scraped_today = len(daily_data)
    logging.info("Scrape summary:")
    logging.info(f" - Date scraped: {today}")
    logging.info(f" - Products scraped today (before DB duplicate filtering): {scraped_today}")
    logging.info(f" - Total products in database: {total}")
    logging.info(" - Breakdown by date:")
    for d, cnt in breakdown:
        logging.info(f"    • {d}: {cnt}")
    logging.info(f" - CSV update: {'successful' if csv_ok else 'failed'} ({csv_file})")

# 6️⃣ Main
if __name__ == "__main__":
    scrape_and_store()

