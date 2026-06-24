from fastapi import APIRouter, Depends
from db import get_db

router = APIRouter(prefix="/api", tags=["Diversity Engine (Algorithmic Core)"])

# Mock dependency for acquiring the logged-in user context
def get_current_user_id() -> int:
    return 42

@router.get("/recommendations/diversity")
async def recommendations_diversity(user_id: int = Depends(get_current_user_id)):
    """
    **Feature 12a: Diversity recommendations compatibility route**
    - **Query Parameter**: `user_id`
    - **Database Action**: `SELECT * FROM articles ORDER BY published_at DESC LIMIT 20`
    - **Returns**: A fallback article list for diversity feed consumers.
    """
    db = await get_db()
    try:
        rows = await db.fetch(
            "SELECT article_id, title, slug, content, view_count, published_at FROM articles ORDER BY published_at DESC LIMIT 20"
        )
        return [dict(row) for row in rows] if rows else []
    finally:
        await db.close()
