from fastapi import APIRouter, Depends, status
from schemas import InteractionLog, TagMap
from db import get_db

router = APIRouter(prefix="/api", tags=["Diversity Engine (Algorithmic Core)"])

# Mock dependency for acquiring the logged-in user context
def get_current_user_id() -> int:
    return 42

@router.post("/interactions/log")
async def log_user_interaction(interaction: InteractionLog, user_id: int = Depends(get_current_user_id)):
    """
    **Feature 10: Log user interaction (Bias Tracking)**
    
    - **JSON Parameters**: `article_id`, `interaction_type`, `reading_time_seconds`
    - **Database Action**: `INSERT INTO interactions (user_id, article_id, interaction_type, reading_time_seconds)`
    - **Returns**: A success acknowledgment acknowledging telemetry footprint data receipt.
    """
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO interactions (user_id, article_id, interaction_type, reading_time_seconds) VALUES ($1, $2, $3, $4)",
            user_id, interaction.article_id, interaction.interaction_type, interaction.reading_time_seconds
        )
        return {"message": "Interaction telemetry footprint registered successfully"}
    finally:
        await db.close()

@router.get("/analytics/user-bias")
async def identify_user_bias(user_id: int = Depends(get_current_user_id)):
    """
    **Feature 11: Identify user's primary interest**
    
    - **JSON Parameters**: None
    - **Database Action**: `SELECT tag_id FROM interactions JOIN article_tags USING(article_id) WHERE user_id = $id GROUP BY tag_id ORDER BY COUNT(*) DESC LIMIT 1`
    - **Returns**: The single tag ID that represents the user's highest concentrated interaction bias.
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
    
    - **Query Parameter**: `user_bias_tag` (Passed down or evaluated implicitly)
    - **Database Action**: `SELECT article_id FROM article_tags WHERE tag_id = (SELECT opposite_tag_id FROM tag_mappings WHERE tag_id = $user_bias)`
    - **Returns**: A tailored collection of article IDs representing the complete opposite viewpoint.
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
        return {"feed_type": "pivot_diversity", "mix_ratio": "30%", "article_ids": ids}
    finally:
        await db.close()

@router.post("/admin/tags/map", status_code=status.HTTP_201_CREATED)
async def map_tag_opposites(mapping: TagMap):
    """
    **Feature 13: Define tag opposites (Admin)**
    
    - **JSON Parameters**: `tag_id`, `opposite_tag_id`
    - **Database Action**: `INSERT INTO tag_mappings (tag_id, opposite_tag_id)`
    - **Returns**: Confirmation payload establishing the algorithmic polarity link.
    """
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO tag_mappings (tag_id, opposite_tag_id) VALUES ($1, $2)",
            mapping.tag_id, mapping.opposite_tag_id
        )
        return {"message": f"Successfully mapped tag {mapping.tag_id} as the ideological opposite of tag {mapping.opposite_tag_id}"}
    finally:
        await db.close()
