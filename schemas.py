from pydantic import BaseModel
from typing import Optional

# Format data saat user daftar (Register)
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    major: Optional[str] = None

# Format data saat user login
class UserLogin(BaseModel):
    email: str
    password: str

# Format data user yang ditampilkan keluar (tanpa password)
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    major: Optional[str] = None

    class Config:
        from_attributes = True

# Format data saat membuat postingan baru
class PostCreate(BaseModel):
    category: str
    subject: str
    sub_topic: str
    description: Optional[str] = None
    max_members: int

# Format data postingan yang ditampilkan keluar
class PostOut(BaseModel):
    id: int
    creator_id: int
    category: str
    subject: str
    sub_topic: str
    description: Optional[str] = None
    max_members: int
    current_members: int
    status: str

    class Config:
        from_attributes = True