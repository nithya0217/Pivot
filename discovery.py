from fastapi import APIRouter, Depends
from db import get_db

router = APIRouter(prefix="/api", tags=["Discovery & Analytics"])

def get_current_user_id() -> int:
    return 42

@router.get("/tags/{tag_name}/articles")
async def search_articles_by_tag(tag_name: str):
    """
    **Feature 17: Search articles by tag**
    - **Path Parameter**: `tag_name`
    - **Database Action**: `SELECT * FROM articles JOIN article_tags USING(article_id) JOIN tags USING(tag_id) WHERE tag_name = $tag_name`
    - **Returns**: Collection tracking entries matching this specific string classification.
    """
    db = await get_db()
    try:
        articles = await db.fetch(
            """
            SELECT a.article_id, a.title, a.slug, a.content, a.view_count, a.published_at
            FROM articles a
            JOIN article_tags at ON a.article_id = at.article_id
            JOIN tags t ON at.tag_id = t.tag_id
            WHERE t.tag_name = $1
            """,
            tag_name
        )
        return articles if articles else []
    finally:
        await db.close()

@router.get("/users/me/diversity-index")
async def get_diversity_score(user_id: int = Depends(get_current_user_id)):
    """
    **Feature 18: Generate Diversity Score**
    - **JSON Parameters**: None
    - **Database Action**: `SELECT COUNT(DISTINCT tag_id) FROM interactions JOIN article_tags USING(article_id) WHERE user_id = $id`
    - **Returns**: Calculated score object.
    """
    db = await get_db()
    try:
        score = await db.fetchval(
            """
            SELECT COUNT(DISTINCT at.tag_id)
            FROM interactions i
            JOIN article_tags at ON i.article_id = at.article_id
            WHERE i.user_id = $1
            """,
            user_id
        )
        return {"user_id": user_id, "diversity_score": score if score else 0}
    finally:
        await db.close()

@router.get("/articles/trending")
async def view_trending_articles():
    """
    **Feature 19: View trending articles (Global)**
    - **Database Action**: `SELECT * FROM articles ORDER BY view_count DESC LIMIT 10`
    - **Returns**: Collection slice containing the top viewed articles worldwide.
    """
    db = await get_db()
    try:
        articles = await db.fetch(
            """
            SELECT a.article_id, a.title, a.slug, a.view_count, a.published_at, a.content,
                   u.user_id AS author_id, u.username AS author_username
            FROM articles a
            LEFT JOIN users u ON a.author_id = u.user_id
            ORDER BY a.view_count DESC
            LIMIT 10
            """
        )
        return articles if articles else []
    finally:
        await db.close()
