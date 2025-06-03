import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from utils import extract
# tests/test_extract.py
import pytest
from utils import extract
from bs4 import BeautifulSoup

def test_scrape_data():
    df = extract.scrape_all(start_page=1, end_page=50)
    assert not df.empty

def extract_product_info(div):
    product = {}

    title = div.find("h2", class_="title")
    price = div.find("span", class_="price")
    rating = div.find("div", class_="rating")
    colors = div.find("div", class_="colors")
    size = div.find("div", class_="size")
    gender = div.find("div", class_="gender")

    product["title"] = title.text.strip() if title else "Unknown Title"
    product["price"] = price.text.strip() if price else "Unknown Price"
    product["rating"] = rating.text.strip() if rating else "No Rating"
    product["colors"] = colors.text.strip() if colors else "No Color Info"
    product["size"] = size.text.strip() if size else "No Size Info"
    product["gender"] = gender.text.strip() if gender else "Unspecified"

    return product


