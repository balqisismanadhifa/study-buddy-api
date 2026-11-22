import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "rahasia_default")
ALGORITHM = "HS256"

# Alat untuk mengacak (hash) password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Penanda bahwa endpoint membutuhkan token login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 1. Mengubah password asli menjadi teks acak (hash)
def hash_password(password: str):
    return pwd_context.hash(password)

# 2. Mengecek apakah password yang diketik cocok dengan hash di database
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 3. Membuat tiket masuk (JWT Token) yang berlaku 24 jam
def create_token(user_id: int):
    expire = datetime.utcnow() + timedelta(hours=24)
    data = {"sub": str(user_id), "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# 4. Mengecek siapa user yang sedang login berdasarkan token yang dikirim
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Token tidak valid atau sudah kedaluwarsa")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")
    return user