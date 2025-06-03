# utils/load.py
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine

def load_to_csv(df: pd.DataFrame, filename: str = "product.csv") -> None:
    try:
        df.to_csv(filename, index=False)
        print(f"✅ Data berhasil disimpan ke '{filename}'")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke CSV: {e}")

def load_to_gsheet(df: pd.DataFrame, service_account_file: str, spreadsheet_url: str) -> None:
    try:
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open_by_url(spreadsheet_url)
        worksheet = spreadsheet.sheet1
        
        # Bersihkan sheet sebelum update data baru
        worksheet.clear()
        
        # Konversi DataFrame ke list of lists (termasuk header)
        worksheet.update([df.columns.tolist()] + df.values.tolist())
        print("✅ Data berhasil disimpan ke Google Sheets!")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke Google Sheets: {e}")

def load_to_postgresql(df: pd.DataFrame, db_url: str, table_name='fashion_products'):
    """
    Simpan DataFrame ke PostgreSQL.
    """
    try:
        engine = create_engine(db_url)
        # Gunakan if_exists='append' kalau tabel sudah ada dan ingin tambah data
        df.to_sql(table_name, con=engine, index=False, if_exists='append')
        print(f"✅ Data berhasil disimpan ke tabel '{table_name}' di PostgreSQL.")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke PostgreSQL: {e}")