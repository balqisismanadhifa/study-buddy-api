from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
import models, schemas, auth

app = FastAPI(title="Study & Hackathon Buddy API")


# 1. REGISTER: Mendaftarkan mahasiswa baru
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=auth.hash_password(user.password),
        major=user.major
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 2. LOGIN: Masuk dan mendapatkan JWT Token
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    token = auth.create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


# 3. CREATE POST: Membuat ajakan belajar bareng / tim hackathon (Wajib Login)
@app.post("/posts", response_model=schemas.PostOut)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if post.max_members <= 1:
        raise HTTPException(status_code=400, detail="Jumlah maksimal anggota harus lebih dari 1")

    new_post = models.Post(
        creator_id=current_user.id,
        category=post.category,
        subject=post.subject,
        sub_topic=post.sub_topic,
        description=post.description,
        max_members=post.max_members
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# 4. GET POSTS: Melihat semua daftar ajakan + filter kategori/mata kuliah (Publik)
@app.get("/posts", response_model=list[schemas.PostOut])
def get_posts(
    category: Optional[str] = None,
    subject: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Post)
    if category:
        query = query.filter(models.Post.category == category)
    if subject:
        query = query.filter(models.Post.subject.ilike(f"%{subject}%"))
    return query.all()


# 5. JOIN POST: Bergabung ke kelompok belajar / tim hackathon (Wajib Login)
@app.post("/posts/{post_id}/join")
def join_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Postingan tidak ditemukan")

    if post.creator_id == current_user.id:
        raise HTTPException(status_code=400, detail="Kamu adalah pembuat postingan ini")

    if post.status == "full" or post.current_members >= post.max_members:
        raise HTTPException(status_code=400, detail="Kuota kelompok sudah penuh")

    already_joined = db.query(models.PostMember).filter(
        models.PostMember.post_id == post_id,
        models.PostMember.user_id == current_user.id
    ).first()
    if already_joined:
        raise HTTPException(status_code=400, detail="Kamu sudah bergabung di kelompok ini")

    # Tambahkan anggota baru & perbarui jumlah anggota
    new_member = models.PostMember(post_id=post_id, user_id=current_user.id)
    db.add(new_member)
    post.current_members += 1

    if post.current_members >= post.max_members:
        post.status = "full"

    db.commit()
    return {"message": "Berhasil bergabung ke kelompok!", "current_members": post.current_members, "status": post.status}


# 6. DELETE POST: Menghapus postingan milik sendiri (Wajib Login)
@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Postingan tidak ditemukan")

    if post.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Kamu tidak berhak menghapus postingan orang lain")

    db.delete(post)
    db.commit()
    return {"message": "Postingan berhasil dihapus"}