from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --- User & Auth Schemas ---
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_author: bool = False

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UpdateBio(BaseModel):
    bio: str

# --- Content Schemas ---
class ArticleCreate(BaseModel):
    title: str
    slug: str
    content: str
    tags: Optional[List[str]] = []

class ArticleUpdate(BaseModel):
    title: str
    content: str

class TagLink(BaseModel):
    tag_id: int

# --- Diversity & Interaction Schemas ---
class InteractionLog(BaseModel):
    article_id: int
    interaction_type: str  
    reading_time_seconds: int

class TagMap(BaseModel):
    tag_id: int
    opposite_tag_id: int

class BookmarkCreate(BaseModel):
    article_id: int

class LikeCreate(BaseModel):
    article_id: int
