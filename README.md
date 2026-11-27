# Study & Hackathon Buddy API

Backend REST API untuk menghubungkan mahasiswa yang mencari teman belajar kelompok (*study buddy*) maupun anggota tim lomba (*hackathon*). Dibangun menggunakan FastAPI dan terhubung ke database PostgreSQL di Supabase.

## Live Deployment
- **Base URL:** https://study-buddy-api-beta.vercel.app
- **Swagger UI (Dokumentasi & Uji Coba):** https://study-buddy-api-beta.vercel.app/docs

## Fitur Utama
- **Autentikasi Pengguna:** Registrasi akun baru (`POST /register`) dengan hashing password (`bcrypt`) serta login berbasis JWT Token (`POST /login`).
- **Manajemen Ajakan (Posts):** Membuat ajakan belajar/hackathon (`POST /posts`), melihat & memfilter daftar ajakan berdasarkan kategori atau mata kuliah (`GET /posts`), bergabung ke kelompok dengan validasi kuota (`POST /posts/{post_id}/join`), dan menghapus postingan milik sendiri (`DELETE /posts/{post_id}`).
- **Dokumentasi Interaktif:** Tersedia otomatis melalui Swagger UI (`/docs`).

## Daftar Endpoint

| Method | Endpoint | Akses | Deskripsi |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | Publik | Mendaftarkan akun mahasiswa baru |
| `POST` | `/login` | Publik | Login dan mendapatkan JWT `access_token` |
| `GET` | `/posts` | Publik | Menampilkan semua ajakan (mendukung filter `?category=` & `?subject=`) |
| `POST` | `/posts` | JWT Required | Membuat ajakan belajar kelompok / tim hackathon baru |
| `POST` | `/posts/{post_id}/join` | JWT Required | Bergabung ke kelompok belajar / tim hackathon |
| `DELETE` | `/posts/{post_id}` | JWT Required | Menghapus postingan milik sendiri |

## Teknologi yang Digunakan
- **Framework:** FastAPI & Uvicorn
- **Database & ORM:** PostgreSQL (Supabase) & SQLAlchemy
- **Validasi Data:** Pydantic
- **Keamanan:** OAuth2 Password Bearer, JWT (`python-jose`), & `bcrypt`
- **Deployment:** Vercel

## Struktur Proyek
```text
study-buddy-api/
├── database.py        # Konfigurasi koneksi database PostgreSQL (Supabase)
├── models.py          # Definisi tabel database (Users, Posts, & PostMembers)
├── schemas.py         # Skema validasi request dan response (Pydantic)
├── auth.py            # Logika hashing password & pembuatan/verifikasi JWT token
├── main.py            # Endpoint utama API dan routing
├── vercel.json        # Konfigurasi routing deployment Vercel
├── requirements.txt   # Daftar dependensi library Python
└── .env               # Variabel lingkungan (tidak di-push ke GitHub)
