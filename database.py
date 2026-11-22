import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Membaca isi file .env agar DATABASE_URL bisa diakses
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Membuat mesin penghubung utama ke PostgreSQL (Supabase)
engine = create_engine(DATABASE_URL)

# 3. Membuat pabrik sesi (session) untuk transaksi baca/tulis data
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Cetakan dasar untuk mendefinisikan struktur tabel di Python
Base = declarative_base()

# 5. Fungsi pembuka dan penutup jalur database otomatis setiap ada request masuk
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()