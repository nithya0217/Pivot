from fastapi import APIRouter, Depends, status
from schemas import UserRegister, UserLogin, UpdateBio

router = APIRouter(prefix="/api", tags=["User & Identity Management"])

# Mock dependency for acquiring the logged-in user context
def get_current_user_id() -> int:
    return 42

@router.post("/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister):
    """
    **Feature 1: Register a new user**
    - **JSON Parameters**: `username`, `email`, `password`, `is_author`
    - **Database Action**: `INSERT INTO users (username, email, password_hash, is_author)`
    - **Returns**: Confirmation payload with the registered email.
    """
    # Inline comment: Passwords must be hashed here prior to database execution
    return {"message": "User registered successfully", "email": user.email}

@router.post("/auth/login")
async def login_user(credentials: UserLogin):
    """
    **Feature 2: Login user**
    - **JSON Parameters**: `email`, `password`
    - **Database Action**: `SELECT * FROM users WHERE email = $input_email`
    - **Returns**: JWT access token block.
    """
    # Inline comment: Check email records against DB and verify hash matches
    return {"access_token": "mock_jwt_token", "token_type": "bearer"}

@router.post("/auth/logout")
async def logout_user(user_id: int = Depends(get_current_user_id)):
    """
    **Feature 3: Logout user**
    - **JSON Parameters**: None (Extracted via auth headers)
    - **Database Action**: `INSERT INTO auth_logs (user_id, action, timestamp)`
    - **Returns**: Disconnection confirmation status.
    """
    # Inline comment: Log an audit entry tracking the user's explicit logout action
    return {"message": "Logged out successfully"}

@router.patch("/users/profile")
async def update_profile(bio_data: UpdateBio, session_id: int = Depends(get_current_user_id)):
    """
    **Feature 4: Update author biography**
    - **JSON Parameters**: `bio`
    - **Database Action**: `UPDATE users SET bio = $1 WHERE user_id = $session_id`
    - **Returns**: Modification update message summary.
    """
    # Inline comment: Filter the UPDATE execution path to matches on the active session_id
    return {"message": "Biography updated successfully", "author_id": session_id}
