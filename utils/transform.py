# utils/transform.py
import pandas as pd
import re

class DataTransformer:
    def transform(self, raw_data):
        df = raw_data.copy()
        if df.empty:
            print("[WARNING] ❌ Data kosong, tidak ada yang akan di-transformasi.")
            return df

        # Hapus entri dengan title yang tidak valid
        df = df[~df['title'].isin(["Unknown Product", "Unknown Title"])].drop_duplicates()

        # Bersihkan dan konversi harga: hapus simbol '$' dan karakter non-digit lainnya, lalu konversi ke float dan hitung nilai dalam Rupiah
        def clean_price(p):
            try:
                cleaned = re.sub(r'[^\d.]', '', p)
                return float(cleaned) * 16000 if cleaned else None
            except Exception:
                return None

        df['price'] = df['price'].apply(clean_price)
        df = df.dropna(subset=['price'])

        # Bersihkan dan konversi rating: ambil angka pertama dari string rating
        def clean_rating(r):
            if not isinstance(r, str) or not r:
                return None
            match = re.search(r"(\d+\.?\d*)", r)
            return float(match.group(1)) if match else None

        df['rating'] = df['rating'].apply(clean_rating)
        df = df.dropna(subset=['rating'])

        # Bersihkan kolom colors, size, dan gender (opsional)
        df['colors'] = df['colors'].str.replace('Colors', '').str.strip()
        df['size'] = df['size'].str.replace('Size:', '').str.strip()
        df['gender'] = df['gender'].str.replace('Gender:', '').str.strip()

        df.reset_index(drop=True, inplace=True)
        return df

transformer = DataTransformer()

def transform(df):
    return transformer.transform(df)


