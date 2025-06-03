# utils/extract.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def extract_product_info(card):
    # Ambil title dari <h3 class="product-title">
    title_element = card.find("h3", class_="product-title")
    title = title_element.text.strip() if title_element else "Unknown Title"
    
    # Ambil price dari <span class="price"> di dalam <div class="price-container">
    price_container = card.find("div", class_="price-container")
    if price_container:
        price_element = price_container.find("span", class_="price")
        price = price_element.text.strip() if price_element else "Price Unavailable"
    else:
        price = "Price Unavailable"
    
    # Ambil informasi rating, colors, size, gender.
    # Misalnya asumsikan urutannya: rating, colors, size, gender dalam elemen <p>
    p_elements = card.find_all("p")
    rating = p_elements[0].text.strip() if len(p_elements) > 0 else "No Rating"
    colors = p_elements[1].text.strip() if len(p_elements) > 1 else "No Color Info"
    size = p_elements[2].text.strip() if len(p_elements) > 2 else "No Size Info"
    gender = p_elements[3].text.strip() if len(p_elements) > 3 else "No Gender Info"
    
    # Tambahkan timestamp
    timestamp = datetime.now().isoformat()
    
    return {
        "title": title,
        "price": price,
        "rating": rating,
        "colors": colors,
        "size": size,
        "gender": gender,
        "timestamp": timestamp
    }

def scrape_all(start_page=1, end_page=50):
    base_url = "https://fashion-studio.dicoding.dev/page{}"
    all_products = []
    for page in range(start_page, end_page + 1):
        url = base_url.format(page)
        print(f"Halaman {page}: Mulai scraping {url}")
        html = fetch_page_content(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            product_cards = soup.find_all("div", class_="collection-card")
            print(f"Halaman {page}: Ditemukan {len(product_cards)} produk")
            for card in product_cards:
                product = extract_product_info(card)
                all_products.append(product)
        else:
            print(f"Halaman {page}: Gagal mendapatkan konten.")
    return pd.DataFrame(all_products)
