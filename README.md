# Study & Hackathon Buddy API

Backend REST API sederhana untuk menghubungkan mahasiswa yang mencari teman belajar kelompok (*study buddy*) maupun anggota tim lomba (*hackathon*). Dibangun menggunakan **FastAPI** dan terhubung ke database PostgreSQL di **Supabase**.

## Fitur Utama
- **Autentikasi Pengguna:** Registrasi akun baru (`POST /register`) dengan enkripsi password (`bcrypt`) serta login berbasis JWT Token (`POST /login`).
- **Manajemen Ajakan (Posts):** Membuat postingan ajakan belajar/hackathon (`POST /posts`) bagi pengguna yang sudah login dan melihat daftar ajakan aktif (`GET /posts`).
- **Dokumentasi Interaktif:** Tersedia otomatis melalui Swagger UI (`/docs`).

## Teknologi yang Digunakan
- **Framework:** FastAPI & Uvicorn
- **Database & ORM:** PostgreSQL (Supabase) & SQLAlchemy
- **Validasi Data:** Pydantic
- **Keamanan:** OAuth2 Password Bearer, JWT (`python-jose`), & `bcrypt`

## Struktur Proyek
```text
study-buddy-api/
├── database.py        # Konfigurasi koneksi database PostgreSQL (Supabase)
├── models.py          # Definisi tabel database (Users & Posts)
├── schemas.py         # Skema validasi request dan response (Pydantic)
├── auth.py            # Logika hashing password & pembuatan/verifikasi JWT token
├── main.py            # Endpoint utama API dan routing
├── requirements.txt   # Daftar dependensi library Python
└── .env               # Variabel lingkungan (DATABASE_URL & SECRET_KEY - tidak di-push ke GitHub)