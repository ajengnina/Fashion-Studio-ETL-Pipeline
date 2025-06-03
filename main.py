# main.py
from utils import extract, transform, load

def main():
    print("📦 Extracting data...")
    raw_data = extract.scrape_all()  # Ambil data dari halaman web
    print(f"Jumlah data mentah: {len(raw_data)}")
    
    print("🔧 Transforming data...")
    transformer = transform.DataTransformer()
    clean_data = transformer.transform(raw_data)
    print(f"Jumlah data bersih: {len(clean_data)}")
    
    print("💾 Saving data to CSV...")
    load.load_to_csv(clean_data, "product.csv")
    
    print("☁️ Saving data to Google Sheets...")
    load.load_to_gsheet(
        clean_data,
        service_account_file='fashion-studio.json',
        spreadsheet_url='https://docs.google.com/spreadsheets/d/1bYSconAsDjXMf9Qhp1KgRlk7wGw9I1jNzxPd_GeFdbQ/edit?gid=0#gid=0'
    )

    print("🐘 Saving data to PostgreSQL...")
    db_url = 'postgresql://ajengnina12:123456@localhost:5432/fashion_db'
    load.load_to_postgresql(clean_data, db_url=db_url)


if __name__ == "__main__":
    main()
