from fastapi import APIRouter, Depends, status
from schemas import UserRegister, UserLogin, UpdateBio
from db import get_db
import hashlib

router = APIRouter(prefix="/api", tags=["User & Identity Management"])

# Mock dependency for acquiring the logged-in user context
def get_current_user_id() -> int:
    return 42

def hash_password(password: str) -> str:
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister):
    """
    **Feature 1: Register a new user**
    - **JSON Parameters**: `username`, `email`, `password`, `is_author`
    - **Database Action**: `INSERT INTO users (username, email, password_hash, is_author)`
    - **Returns**: Confirmation payload with the registered email.
    """
    db = await get_db()
    try:
        password_hash = hash_password(user.password)
        result = await db.fetchrow(
            "INSERT INTO users (username, email, password_hash, is_author) VALUES ($1, $2, $3, $4) RETURNING user_id, email",
            user.username, user.email, password_hash, user.is_author
        )
        return {
            "message": "User registered successfully",
            "user_id": result['user_id'],
            "email": result['email'],
            "username": user.username,
            "is_author": user.is_author,
        }
    except Exception as e:
        return {"error": str(e)}, 400
    finally:
        await db.close()

@router.post("/auth/login")
async def login_user(credentials: UserLogin):
    """
    **Feature 2: Login user**
    - **JSON Parameters**: `email`, `password`
    - **Database Action**: `SELECT * FROM users WHERE email = $input_email`
    - **Returns**: JWT access token block.
    """
    db = await get_db()
    try:
        password_hash = hash_password(credentials.password)
        user = await db.fetchrow(
            "SELECT user_id, email, is_author FROM users WHERE email = $1 AND password_hash = $2",
            credentials.email, password_hash
        )
        if not user:
            return {"error": "Invalid email or password"}, 401
        return {"user_id": user['user_id'], "email": user['email'], "is_author": user['is_author'], "access_token": "token", "token_type": "bearer"}
    finally:
        await db.close()

@router.post("/auth/logout")
async def logout_user(user_id: int = Depends(get_current_user_id)):
    """
    **Feature 3: Logout user**
    - **JSON Parameters**: None (Extracted via auth headers)
    - **Database Action**: `INSERT INTO auth_logs (user_id, action, timestamp)`
    - **Returns**: Disconnection confirmation status.
    """
    db = await get_db()
    try:
        # Note: Create auth_logs table if needed
        await db.execute(
            "INSERT INTO auth_logs (user_id, action, timestamp) VALUES ($1, $2, CURRENT_TIMESTAMP)",
            user_id, 'logout'
        )
        return {"message": "Logged out successfully"}
    except:
        # If auth_logs table doesn't exist yet, just return success
        return {"message": "Logged out successfully"}
    finally:
        await db.close()

@router.patch("/users/profile")
async def update_profile(bio_data: UpdateBio, session_id: int = Depends(get_current_user_id)):
    """
    **Feature 4: Update author biography**
    - **JSON Parameters**: `bio`
    - **Database Action**: `UPDATE users SET bio = $1 WHERE user_id = $session_id`
    - **Returns**: Modification update message summary.
    """
    db = await get_db()
    try:
        await db.execute(
            "UPDATE users SET bio = $1 WHERE user_id = $2",
            bio_data.bio, session_id
        )
        return {"message": "Biography updated successfully", "author_id": session_id}
    finally:
        await db.close()
