from fastapi import APIRouter, Depends, status
from schemas import InteractionLog, TagMap, BookmarkCreate, LikeCreate
from db import get_db

router = APIRouter(prefix="/api", tags=["Diversity Engine & Engagement"])

def get_current_user_id() -> int:
    return 42

@router.post("/interactions/log")
async def log_user_interaction(interaction: InteractionLog, user_id: int = Depends(get_current_user_id)):
    """
    **Feature 10: Log user interaction (Bias Tracking)**
    - **JSON Parameters**: `article_id`, `interaction_type`, `reading_time_seconds`
    - **Database Action**: `INSERT INTO interactions (user_id, article_id, interaction_type, reading_time_seconds)`
    - **Returns**: System reception message.
    """
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO interactions (user_id, article_id, interaction_type, reading_time_seconds) VALUES ($1, $2, $3, $4)",
            user_id, interaction.article_id, interaction.interaction_type, interaction.reading_time_seconds
        )
        return {"message": "Interaction metrics recorded successfully"}
    finally:
        await db.close()


@router.post("/interactions")
async def register_interaction(interaction: InteractionLog, user_id: int = Depends(get_current_user_id)):
    """
    Compatibility endpoint: POST /api/interactions
    Forwards to the original interaction logging implementation.
    """
    return await log_user_interaction(interaction, user_id)

@router.get("/analytics/user-bias")
async def identify_user_bias(user_id: int = Depends(get_current_user_id)):
    """
    **Feature 11: Identify user's primary interest**
    - **JSON Parameters**: None
    - **Database Action**: `SELECT tag_id FROM interactions JOIN article_tags USING(article_id) WHERE user_id = $id GROUP BY tag_id ORDER BY COUNT(*) DESC LIMIT 1`
    - **Returns**: Object revealing the single highest interacted tag identity key.
    """
    db = await get_db()
    try:
        result = await db.fetchval(
            """
            SELECT at.tag_id 
            FROM interactions i 
            JOIN article_tags at ON i.article_id = at.article_id 
            WHERE i.user_id = $1 
            GROUP BY at.tag_id 
            ORDER BY COUNT(*) DESC 
            LIMIT 1
            """,
            user_id
        )
        primary_tag = result if result else 1
        return {"user_id": user_id, "primary_tag_id": primary_tag}
    finally:
        await db.close()

@router.get("/feed/pivot")
async def generate_contrarian_feed(user_bias_tag: int = 5):
    """
    **Feature 12: Generate contrarian feed (30% Mix)**
    - **Query Parameter**: `user_bias_tag`
    - **Database Action**: `SELECT article_id FROM article_tags WHERE tag_id = (SELECT opposite_tag_id FROM tag_mappings WHERE tag_id = $user_bias)`
    - **Returns**: Curated target feed containing structurally contrasting data perspectives.
    """
    db = await get_db()
    try:
        article_ids = await db.fetch(
            """
            SELECT DISTINCT at.article_id 
            FROM article_tags at 
            WHERE at.tag_id IN (
                SELECT opposite_tag_id FROM tag_mappings WHERE tag_id = $1
            )
            LIMIT 10
            """,
            user_bias_tag
        )
        ids = [row['article_id'] for row in article_ids]
        return {"feed_type": "pivot_diversity", "article_ids": ids}
    finally:
        await db.close()

@router.post("/admin/tags/map", status_code=status.HTTP_201_CREATED)
async def map_tag_opposites(mapping: TagMap):
    """
    **Feature 13: Define tag opposites (Admin)**
    - **JSON Parameters**: `tag_id`, `opposite_tag_id`
    - **Database Action**: `INSERT INTO tag_mappings (tag_id, opposite_tag_id)`
    - **Returns**: Status showing execution completion.
    """
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO tag_mappings (tag_id, opposite_tag_id) VALUES ($1, $2)",
            mapping.tag_id, mapping.opposite_tag_id
        )
        return {"message": f"Successfully mapped inverse relationship for tag {mapping.tag_id}"}
    finally:
        await db.close()

@router.post("/bookmarks", status_code=status.HTTP_201_CREATED)
async def bookmark_article(bookmark: BookmarkCreate, user_id: int = Depends(get_current_user_id)):
    """
    **Feature 14: Bookmark an article**
    - **JSON Parameters**: `article_id`
    - **Database Action**: `INSERT INTO bookmarks (user_id, article_id)`
    - **Returns**: Creation tracking string.
    """
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO bookmarks (user_id, article_id) VALUES ($1, $2)",
            user_id, bookmark.article_id
        )
        return {"message": f"Article {bookmark.article_id} bookmarked"}
    finally:
        await db.close()

@router.delete("/bookmarks/{article_id}")
async def remove_bookmark(article_id: int, user_id: int = Depends(get_current_user_id)):
    """
    **Feature 15: Remove bookmark**
    - **Path Parameter**: `article_id`
    - **Database Action**: `DELETE FROM bookmarks WHERE user_id = $id AND article_id = $article_id`
    - **Returns**: Removal execution status updates.
    """
    db = await get_db()
    try:
        await db.execute(
            "DELETE FROM bookmarks WHERE user_id = $1 AND article_id = $2",
            user_id, article_id
        )
        return {"message": f"Bookmark for article {article_id} removed"}
    finally:
        await db.close()

@router.post("/interactions/like")
async def like_article(like: LikeCreate, user_id: int = Depends(get_current_user_id)):
    """
    **Feature 16: Like an article**
    - **JSON Parameters**: `article_id`
    - **Database Action**: `INSERT INTO interactions (user_id, article_id, interaction_type='like')`
    - **Returns**: Status message verifying registered transaction execution.
    """
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO interactions (user_id, article_id, interaction_type, reading_time_seconds) VALUES ($1, $2, $3, $4)",
            user_id, like.article_id, 'like', 0
        )
        return {"message": f"Article {like.article_id} successfully liked"}
    finally:
        await db.close()
