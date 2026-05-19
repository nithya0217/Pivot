from fastapi import APIRouter, Depends, status
from schemas import InteractionLog, TagMap

router = APIRouter(prefix="/api", tags=["Diversity Engine (Algorithmic Core)"])

# Mock dependency for acquiring the logged-in user context
def get_current_user_id() -> int:
    return 42

@router.post("/interactions/log")
async def log_user_interaction(interaction: InteractionLog, user_id: int = Depends(get_current_user_id)):
    """
    **Feature 10: Log user interaction (Bias Tracking)**
    
    - **JSON Parameters**: `article_id`, `interaction_type`, `reading_time_seconds`
    - **Database Action**: `INSERT INTO interactions (user_id, article_id, type, reading_time_seconds)`
    - **Returns**: A success acknowledgment acknowledging telemetry footprint data receipt.
    """
    # Inline comment: Track raw metrics and dwell time to feed the behavioral bias calculations
    return {"message": "Interaction telemetry footprint registered successfully"}

@router.get("/analytics/user-bias")
async def identify_user_bias(user_id: int = Depends(get_current_user_id)):
    """
    **Feature 11: Identify user's primary interest**
    
    - **JSON Parameters**: None
    - **Database Action**: `SELECT tag_id FROM interactions JOIN article_tags USING(article_id) WHERE user_id = $id GROUP BY tag_id ORDER BY COUNT(*) DESC LIMIT 1`
    - **Returns**: The single tag ID that represents the user's highest concentrated interaction bias.
    """
    # Inline comment: Heavily aggregates user history to find their current echo-chamber topic vector
    return {"user_id": user_id, "primary_tag_id": 5}

@router.get("/feed/pivot")
async def generate_contrarian_feed(user_bias_tag: int = 5):
    """
    **Feature 12: Generate contrarian feed (30% Mix)**
    
    - **Query Parameter**: `user_bias_tag` (Passed down or evaluated implicitly)
    - **Database Action**: `SELECT article_id FROM article_tags WHERE tag_id = (SELECT opposite_tag_id FROM tag_mappings WHERE tag_id = $user_bias)`
    - **Returns**: A tailored collection of article IDs representing the complete opposite viewpoint.
    """
    # Inline comment: Injects an adversarial mix of content to deliberately pivot the user's information diet
    return {"feed_type": "pivot_diversity", "mix_ratio": "30%", "article_ids": [201, 204, 305]}

@router.post("/admin/tags/map", status_code=status.HTTP_201_CREATED)
async def map_tag_opposites(mapping: TagMap):
    """
    **Feature 13: Define tag opposites (Admin)**
    
    - **JSON Parameters**: `tag_id`, `opposite_tag_id`
    - **Database Action**: `INSERT INTO tag_mappings (tag_id, opposite_tag_id)`
    - **Returns**: Confirmation payload establishing the algorithmic polarity link.
    """
    # Inline comment: Explicitly used by administrators to train the recommendation balance weights
    return {"message": f"Successfully mapped tag {mapping.tag_id} as the ideological opposite of tag {mapping.opposite_tag_id}"}
