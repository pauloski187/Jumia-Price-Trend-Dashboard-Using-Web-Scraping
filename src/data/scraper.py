import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import os
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
db_file = "jumia_data.db"
csv_file = "../../data/raw/jumia_product.csv"

def setup_db():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''
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
    ''')
    conn.commit()
    conn.close()

# 4️⃣ Scrape function
def scrape_and_store():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    daily_data = []  # store daily data for CSV

    for category_name, base_url in categories.items():
        print(f"Scraping category: {category_name}")
        for page in range(1, 6):
            url = base_url + f"?page={page}"
            try:
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code != 200:
                    print(f"Page {page} returned {response.status_code}")
                    break
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
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
                    discount = product.find("div", class_="bdg _dsct").text.strip() if product.find("div", class_="bdg _dsct") else "0%"
                    rating = product.find("div", class_="rev").text.strip() if product.find("div", class_="rev") else "N/A"
                    stock = "In Stock"
                    date_scraped = datetime.now().strftime("%Y-%m-%d")

                    # Insert into DB
                    c.execute('''
                        INSERT INTO products (category, name, url, current_price, original_price, discount, rating, stock, date_scraped)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (category_name, name, link, current_price, original_price, discount, rating, stock, date_scraped))

                    # Append to daily_data for CSV
                    daily_data.append([category_name, name, link, current_price, original_price, discount, rating, stock, date_scraped])
                except Exception as e:
                    print(f"Failed to scrape product: {e}")

            time.sleep(1)

    conn.commit()
    conn.close()

    # 5️⃣ Append to CSV (create if doesn't exist)
    df_new = pd.DataFrame(daily_data, columns=["Category", "Name", "URL", "Current Price",
                                               "Original Price", "Discount", "Rating", "Stock", "Date Scraped"])
    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(csv_file, index=False, encoding="utf-8")
    else:
        df_new.to_csv(csv_file, index=False, encoding="utf-8")

    print(f"Data appended to {csv_file} and database!")

# 6️⃣ Main
if __name__ == "__main__":
    setup_db()
    scrape_and_store()

