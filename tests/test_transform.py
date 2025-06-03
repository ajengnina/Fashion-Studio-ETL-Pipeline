import pandas as pd
from utils.transform import DataTransformer
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils import extract


def test_transform():
    dummy_data = pd.DataFrame({
        "title": ["T-shirt", "Unknown Product", None],
        "price": ["$10.0", "Price Unavailable", "$15.5"],
        "rating": ["4.5 stars", "5.0 stars", None],  # rating harus string karena ada regex di transform
        "colors": ["3 Colors", "5 Colors", "2 Colors"],
        "size": ["Size: M", "Size: L", None],
        "gender": ["Gender: Men", "Gender: Women", None]
    })

    transformer = DataTransformer()
    cleaned_df = transformer.transform(dummy_data)

    # Pastikan 'Unknown Product' sudah terhapus
    assert "Unknown Product" not in cleaned_df['title'].values
    
    # Pastikan price sudah jadi float dan dalam rupiah (minimal 10.0 * 16000)
    assert cleaned_df['price'].dtype == float
    assert cleaned_df['price'].min() >= 10.0 * 16000

    # Pastikan rating sudah jadi float
    assert cleaned_df['rating'].dtype == float

    # Pastikan kolom colors, size, gender sudah dibersihkan dari teks tambahan
    assert all("Colors" not in c for c in cleaned_df['colors'])
    assert all("Size:" not in s for s in cleaned_df['size'])
    assert all("Gender:" not in g for g in cleaned_df['gender'])

def test_transform_with_error_price():
    dummy_data = pd.DataFrame({
        "title": ["T-shirt", "Faulty Product"],
        "price": ["$10.0", "abc$"],  # 'abc$' bikin clean_price error
        "rating": ["4.5 stars", "5.0 stars"],
        "colors": ["3 Colors", "5 Colors"],
        "size": ["Size: M", "Size: L"],
        "gender": ["Gender: Men", "Gender: Women"]
    })

    transformer = DataTransformer()
    cleaned_df = transformer.transform(dummy_data)
    
    # Pastikan 'Faulty Product' hilang karena price error -> None
    assert "Faulty Product" not in cleaned_df['title'].values
