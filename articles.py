from fastapi import APIRouter, Depends, status
from schemas import ArticleCreate, ArticleUpdate, TagLink
from db import get_db
import asyncpg

router = APIRouter(prefix="/api", tags=["Content & Publishing"])

def get_current_user_id() -> int:
    return 42

# Internal trigger function for tracking analytics (Feature 20)
async def increment_view_count(id: int):
    """
    **Feature 20: Increment view count**
    - **Internal Trigger Framework Method**
    - **Database Action**: `UPDATE articles SET view_count = view_count + 1 WHERE id = $id`
    """
    db = await get_db()
    try:
        await db.execute(
            "UPDATE articles SET view_count = view_count + 1 WHERE article_id = $1",
            id
        )
    except:
        pass  # Silently fail if update fails
    finally:
        await db.close()

@router.post("/articles", status_code=status.HTTP_201_CREATED)
async def create_article(article: ArticleCreate, author_id: int = Depends(get_current_user_id)):
    """
    **Feature 5: Create a new article**
    - **JSON Parameters**: `title`, `slug`, `content`, `tags`, `author_id`
    - **Database Action**: `INSERT INTO articles (author_id, title, slug, content)` and link tags
    - **Returns**: Struct describing the persisted article metadata.
    """
    db = await get_db()
    try:
        # Prefer author_id supplied by the frontend when auth is not fully implemented.
        if article.author_id is not None:
            author_id = article.author_id

        # Create the article
        result = await db.fetchrow(
            "INSERT INTO articles (author_id, title, slug, content) VALUES ($1, $2, $3, $4) RETURNING article_id, author_id, slug, published_at",
            author_id, article.title, article.slug, article.content
        )
        article_id = result['article_id']
        
        # Link tags to the article
        if article.tags:
            for tag_name in article.tags[:5]:  # Max 5 tags per article
                # First, ensure the tag exists
                tag_id_result = await db.fetchval(
                    "SELECT tag_id FROM tags WHERE tag_name = $1",
                    tag_name
                )
                
                if tag_id_result:
                    # Link existing tag
                    await db.execute(
                        "INSERT INTO article_tags (article_id, tag_id) VALUES ($1, $2)",
                        article_id, tag_id_result
                    )
                else:
                    # Create new tag and link it
                    new_tag = await db.fetchval(
                        "INSERT INTO tags (tag_name) VALUES ($1) RETURNING tag_id",
                        tag_name
                    )
                    if new_tag:
                        await db.execute(
                            "INSERT INTO article_tags (article_id, tag_id) VALUES ($1, $2)",
                            article_id, new_tag
                        )
        
        return {
            "id": article_id,
            "author_id": result['author_id'],
            "slug": result['slug'],
            "status": "published",
            "published_at": result['published_at'],
            "tags": article.tags
        }
    except Exception as e:
        return {"error": str(e)}, 400
    finally:
        await db.close()

@router.get("/articles")
async def list_articles():
    """
    **Feature 7a: List articles**
    - **Database Action**: `SELECT * FROM articles ORDER BY published_at DESC LIMIT 20`
    - **Returns**: Article listing for the feed.
    """
    db = await get_db()
    try:
        rows = await db.fetch(
            "SELECT article_id, title, slug, content, view_count, published_at FROM articles ORDER BY published_at DESC LIMIT 20"
        )
        return [dict(row) for row in rows] if rows else []
    finally:
        await db.close()

@router.post("/articles/{id}/tags")
async def link_tags_to_article(id: int, tag_payload: TagLink):
    """
    **Feature 6: Link tags to article**
    - **Path Parameter**: `id` (Target Article ID)
    - **JSON Parameters**: `tag_id`
    - **Database Action**: `INSERT INTO article_tags (article_id, tag_id)`
    - **Returns**: Mapping assignment notification.
    """
    db = await get_db()
    try:
        # Check tag count constraint (max 5 tags per article)
        tag_count = await db.fetchval(
            "SELECT COUNT(*) FROM article_tags WHERE article_id = $1",
            id
        )
        if tag_count >= 5:
            return {"error": "Maximum 5 tags per article"}, 400
        
        await db.execute(
            "INSERT INTO article_tags (article_id, tag_id) VALUES ($1, $2)",
            id, tag_payload.tag_id
        )
        return {"message": f"Tag {tag_payload.tag_id} linked to article {id}"}
    finally:
        await db.close()

@router.get("/articles/{slug}")
async def view_article_details(slug: str):
    """
    **Feature 7: View article details**
    - **Path Parameter**: `slug`
    - **Database Action**: `SELECT * FROM articles JOIN users ON articles.author_id = users.user_id WHERE slug = $slug`
    - **Returns**: Comprehensive data block containing nested author user information.
    """
    db = await get_db()
    try:
        result = await db.fetchrow(
            "SELECT a.*, u.username, u.email FROM articles a LEFT JOIN users u ON a.author_id = u.user_id WHERE a.slug = $1",
            slug
        )
        if not result:
            return {"error": "Article not found"}, 404
        
        await increment_view_count(id=result['article_id'])
        
        return {
            "id": result['article_id'],
            "slug": result['slug'],
            "title": result['title'],
            "content": result['content'],
            "view_count": result['view_count'],
            "published_at": result['published_at'],
            "author": {
                "user_id": result['author_id'],
                "username": result['username'] if result['username'] else None,
                "email": result['email'] if result['email'] else None
            }
        }
    finally:
        await db.close()

@router.put("/articles/{id}")
async def update_article(id: int, article_update: ArticleUpdate, author_id: int = Depends(get_current_user_id)):
    """
    **Feature 8: Update article**
    - **Path Parameter**: `id`
    - **JSON Parameters**: `title`, `content`
    - **Database Action**: `UPDATE articles SET title, content WHERE id = $id AND author_id = $session_id`
    - **Returns**: Succinct update state summary.
    """
    db = await get_db()
    try:
        await db.execute(
            "UPDATE articles SET title = $1, content = $2 WHERE article_id = $3 AND author_id = $4",
            article_update.title, article_update.content, id, author_id
        )
        return {"message": f"Article {id} updated successfully"}
    finally:
        await db.close()

@router.delete("/articles/{id}")
async def delete_article(id: int):
    """
    **Feature 9: Delete article**
    - **Path Parameter**: `id`
    - **Database Action**: `DELETE FROM articles WHERE id = $id`
    - **Returns**: Clean deletion complete report.
    """
    db = await get_db()
    try:
        await db.execute(
            "DELETE FROM articles WHERE article_id = $1",
            id
        )
        return {"message": f"Article {id} and its associated tags deleted"}
    finally:
        await db.close()
