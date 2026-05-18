from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

# Initialize the main router for all features
router = APIRouter(prefix="/api", tags=["Pivot Core API"])


# =====================================================================
# Pydantic Schemas for Requests and Responses
# =====================================================================

class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_author: bool = False

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class ProfileUpdateRequest(BaseModel):
    bio: str

class ArticleCreateRequest(BaseModel):
    title: str
    slug: str
    content: str

class ArticleUpdateRequest(BaseModel):
    title: str
    content: str

class TagLinkRequest(BaseModel):
    tag_id: int

class InteractionLogRequest(BaseModel):
    article_id: int
    interaction_type: str  # e.g., 'view', 'scroll'
    reading_time_seconds: int

class TagMapRequest(BaseModel):
    tag_id: int
    opposite_tag_id: int

class BookmarkRequest(BaseModel):
    article_id: int


# =====================================================================
# 1. User & Identity Management
# =====================================================================

@router.post("/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterRequest):
    """
    Feature 1: Register a new user.
    
    - **JSON Parameters**:
        - `username` (str): Unique username.
        - `email` (str): Valid email address.
        - `password` (str): Plaintext password (will be hashed).
        - `is_author` (bool): Flag indicating if the user can publish content.
    
    - **Database Action**:
        `INSERT INTO users (username, email, password_hash, is_author)`
        
    - **Returns**: A success confirmation with user metadata.
    """
    # Inline comment: Database interaction to hash password and insert the user record
    return {"message": "User registered successfully", "username": user_data.username}


@router.post("/auth/login")
async def login_user(credentials: UserLoginRequest):
    """
    Feature 2: Login user.
    
    - **JSON Parameters**:
        - `email` (str): Registered email address.
        - `password` (str): User password.
        
    - **Database Action**:
        `SELECT * FROM users WHERE email = $input_email`
        
    - **Returns**: Access token and session type.
    """
    # Inline comment: Check email existence, verify password_hash, and issue a session/token
    return {"access_token": "mock_token_xyz", "token_type": "bearer"}


@router.post("/auth/logout")
async def logout_user(current_user_id: int = 1):  # Simulated dependency for active session
    """
    Feature 3: Logout user.
    
    - **JSON Parameters**: None (Relies on Authentication/Session Header).
    
    - **Database Action**:
        `INSERT INTO auth_logs (user_id, action, timestamp)`
        
    - **Returns**: Logged out confirmation message.
    """
    # Inline comment: Log the logout event into auth_logs table and invalidate token
    timestamp = datetime.utcnow().isoformat()
    return {"message": f"User {current_user_id} logged out successfully at {timestamp}"}


@router.patch("/users/profile")
async def update_profile(profile_data: ProfileUpdateRequest, current_user_id: int = 1):
    """
    Feature 4: Update author biography.
    
    - **JSON Parameters**:
        - `bio` (str): The updated biographical text.
        
    - **Database Action**:
        `UPDATE users SET bio = $1 WHERE user_id = $session_id`
        
    - **Returns**: Updated status notification.
    """
    # Inline comment: Authenticate session, confirm author privileges, and update bio field
    return {"message": "Biography updated successfully", "updated_bio": profile_data.bio}


# =====================================================================
# 2. Content & Publishing
# =====================================================================

@router.post("/articles", status_code=status.HTTP_201_CREATED)
async def create_article(article: ArticleCreateRequest, current_user_id: int = 1):
    """
    Feature 5: Create a new article.
    
    - **JSON Parameters**:
        - `title` (str): Headline of the article.
        - `slug` (str): URL-friendly unique identifier string.
        - `content` (str): Main body of text.
        
    - **Database Action**:
        `INSERT INTO articles (author_id, title, slug, content, status='published')`
        
    - **Returns**: Object details of the published article.
    """
    # Inline comment: Validate slug uniqueness and enforce default status='published' on insertion
    return {"message": "Article published successfully", "slug": article.slug, "author_id": current_user_id}


@router.post("/articles/{id}/tags")
async def link_tags_to_article(id: int, tag_data: TagLinkRequest):
    """
    Feature 6: Link tags to article.
    
    - **Path Parameters**:
        - `id` (int): Target article primary key.
    - **JSON Parameters**:
        - `tag_id` (int): ID of tag to associate.
        
    - **Database Action**:
        `INSERT INTO article_tags (article_id, tag_id)`
        
    - **Constraint**: Maximum of 5 tags per article.
    
    - **Returns**: Link completion status.
    """
    # Inline comment: Count existing rows in article_tags for this id; block insert if >= 5
    return {"message": f"Tag {tag_data.tag_id} linked successfully to article {id}"}


@router.get("/articles/{slug}")
async def view_article_details(slug: str):
    """
    Feature 7: View article details.
    
    - **Path Parameters**:
        - `slug` (str): Unique URL string of the article.
        
    - **Database Action**:
        `SELECT * FROM articles JOIN users ON articles.author_id = users.user_id WHERE slug = $slug`
        
    - **Returns**: Combined dictionary containing article content and author details.
    """
    # Inline comment: Join query fetches article metadata side-by-side with author profile details
    # Internal Trigger activation for View Count follows synchronously or asynchronously here
    await _internal_increment_view_count(id=101) 
    return {"slug": slug, "title": "Sample Title", "author": {"username": "JohnDoe", "bio": "Writer"}}


@router.put("/articles/{id}")
async def update_article(id: int, article_data: ArticleUpdateRequest, current_user_id: int = 1):
    """
    Feature 8: Update article.
    
    - **Path Parameters**:
        - `id` (int): Target article ID.
    - **JSON Parameters**:
        - `title` (str): Updated title.
        - `content` (str): Updated content body.
        
    - **Database Action**:
        `UPDATE articles SET title, content WHERE id = $id AND author_id = $session_id`
        
    - **Returns**: Status confirmation.
    """
    # Inline comment: Enforce that only the true author ($session_id) can edit this specific article ID
    return {"message": f"Article {id} updated successfully by Author {current_user_id}"}


@router.delete("/articles/{id}")
async def delete_article(id: int, current_user_id: int = 1):
    """
    Feature 9: Delete article.
    
    - **Path Parameters**:
        - `id` (int): Target article ID.
        
    - **Database Action**:
        `DELETE FROM articles WHERE id = $id`
        
    - **Note**: Cascades cleanly to the `article_tags` mapping table.
    
    - **Returns**: Deletion summary response.
    """
    # Inline comment: Fire deletion query; underlying foreign key constraints handle 'article_tags' cascade
    return {"message": f"Article {id} and its associated tags deleted successfully"}


# =====================================================================
# 3. Diversity Engine (The Algorithmic Core)
# =====================================================================

@router.post("/interactions/log")
async def log_user_interaction(log_data: InteractionLogRequest, current_user_id: int = 1):
    """
    Feature 10: Log user interaction (Bias Tracking).
    
    - **JSON Parameters**:
        - `article_id` (int): Target article ID.
        - `interaction_type` (str): The interaction type.
        - `reading_time_seconds` (int): Active time spent on page.
        
    - **Database Action**:
        `INSERT INTO interactions (user_id, article_id, type, reading_time_seconds)`
        
    - **Returns**: Acknowledgment.
    """
    # Inline comment: Write raw telemetry into interaction records for downstream personalization logic
    return {"status": "tracked", "user_id": current_user_id, "article_id": log_data.article_id}


@router.get("/analytics/user-bias")
async def identify_user_bias(current_user_id: int = 1):
    """
    Feature 11: Identify user's primary interest.
    
    - **Query/Session Parameters**: Implicit user session.
    
    - **Database Action**:
        `SELECT tag_id FROM interactions JOIN article_tags USING(article_id) 
         WHERE user_id = $id GROUP BY tag_id ORDER BY COUNT(*) DESC LIMIT 1`
         
    - **Returns**: Primary biased tag identity.
    """
    # Inline comment: Calculate tag frequencies from user's reading history to extract dominant category
    return {"user_id": current_user_id, "primary_tag_id": 42}


@router.get("/feed/pivot")
async def generate_contrarian_feed(user_bias_tag_id: int):
    """
    Feature 12: Generate contrarian feed (30% Mix).
    
    - **Query Parameters**:
        - `user_bias_tag_id` (int): The current calculated primary bias ID.
        
    - **Database Action**:
        `SELECT article_id FROM article_tags WHERE tag_id = 
         (SELECT opposite_tag_id FROM tag_mappings WHERE tag_id = $user_bias)`
         
    - **Returns**: Array of alternative/contrarian article IDs injected into user feeds.
    """
    # Inline comment: Pull mapped system opposites to intentionally break bubble filters (30% mix rule)
    return {"feed_type": "contrarian_pivot", "article_ids": [102, 204, 508]}


@router.post("/admin/tags/map", status_code=status.HTTP_201_CREATED)
async def define_tag_opposites(mapping: TagMapRequest):
    """
    Feature 13: Define tag opposites (Admin Portal).
    
    - **JSON Parameters**:
        - `tag_id` (int): System base tag.
        - `opposite_tag_id` (int): Inverted ideological/conceptual tag.
        
    - **Database Action**:
        `INSERT INTO tag_mappings (tag_id, opposite_tag_id)`
        
    - **Returns**: Status message matching the link.
    """
    # Inline comment: Admin configuration to explicitly define opposing semantic relationships
    return {"message": f"Mapped tag {mapping.tag_id} as polar opposite to {mapping.opposite_tag_id}"}


# =====================================================================
# 4. Engagement & Curation
# =====================================================================

@router.post("/bookmarks", status_code=status.HTTP_201_CREATED)
async def bookmark_article(bookmark: BookmarkRequest, current_user_id: int = 1):
    """
    Feature 14: Bookmark an article.
    
    - **JSON Parameters**:
        - `article_id` (int): Target article to save.
        
    - **Database Action**:
        `INSERT INTO bookmarks (user_id, article_id)`
        
    - **Returns**: Saved confirmation status.
    """
    # Inline comment: Insert unique pairing constraint into personal user bookmark library
    return {"message": "Article bookmarked successfully", "article_id": bookmark.article_id}


@router.delete("/bookmarks/{article_id}")
async def remove_bookmark(article_id: int, current_user_id: int = 1):
    """
    Feature 15: Remove bookmark.
    
    - **Path Parameters**:
        - `article_id` (int): Target article to un-bookmark.
        
    - **Database Action**:
        `DELETE FROM bookmarks WHERE user_id = $id AND article_id = $article_id`
        
    - **Returns**: Removal confirmation message.
    """
    # Inline comment: Delete matching entity row scoped tightly to current session owner
    return {"message": f"Bookmark for article {article_id} removed"}


@router.post("/interactions/like")
async def like_article(like_data: BookmarkRequest, current_user_id: int = 1):
    """
    Feature 16: Like an article.
    
    - **JSON Parameters**:
        - `article_id` (int): Targeted liked article.
        
    - **Database Action**:
        `INSERT INTO interactions (user_id, article_id, type='like')`
        
    - **Returns**: Interaction logged feedback.
    """
    # Inline comment: Insert generic interaction row hardcoded with a 'like' type descriptor
    return {"message": "Article liked", "article_id": like_data.article_id}


# =====================================================================
# 5. Discovery & Analytics
# =====================================================================

@router.get("/tags/{tag_name}/articles")
async def search_articles_by_tag(tag_name: str):
    """
    Feature 17: Search articles by tag name.
    
    - **Path Parameters**:
        - `tag_name` (str): Target textual tag string.
        
    - **Database Action**:
        `SELECT * FROM articles JOIN article_tags USING(article_id) 
         JOIN tags USING(tag_id) WHERE tag_name = $tag_name`
         
    - **Returns**: List of all articles tagged under that topic parameter.
    """
    # Inline comment: Multi-join matching query to pull items labeled with a specific semantic string
    return {"tag": tag_name, "articles": [{"id": 1, "title": "Sample Matching Article"}]}


@router.get("/users/me/diversity-index")
async def generate_diversity_score(current_user_id: int = 1):
    """
    Feature 18: Generate user Diversity Score index.
    
    - **Session Parameters**: Decoded user identity.
    
    - **Database Action**:
        `SELECT COUNT(DISTINCT tag_id) FROM interactions 
         JOIN article_tags USING(article_id) WHERE user_id = $id`
         
    - **Returns**: Calculated integer mapping distinct perspectives viewed.
    """
    # Inline comment: Aggregate mathematical count of entirely unique tags a user interacted with
    return {"user_id": current_user_id, "diversity_score": 14}


@router.get("/articles/trending")
async def view_trending_articles():
    """
    Feature 19: View trending articles (Global Feed).
    
    - **Query Parameters**: None.
    
    - **Database Action**:
        `SELECT * FROM articles ORDER BY view_count DESC LIMIT 10`
        
    - **Returns**: Top 10 hottest articles ranked strictly by view metric.
    """
    # Inline comment: Query ordered descending by flat view metrics with an optimization ceiling cut-off
    return {"trending_articles": [{"id": 99, "title": "Viral Post", "view_count": 15400}]}


# =====================================================================
# Internal System Triggers
# =====================================================================

async def _internal_increment_view_count(id: int):
    """
    Feature 20: Increment view count.
    
    - **Internal Trigger**: Executed internally behind the scenes during Feature 7 requests.
    
    - **Database Action**:
        `UPDATE articles SET view_count = view_count + 1 WHERE id = $id`
    """
    # Inline comment: Atomic operation incrementing the view tracker counter safely on read execution
    pass
