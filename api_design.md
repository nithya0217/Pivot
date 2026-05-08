

### **1. User & Identity Management**

 **Feature:** Create a new user profile.
 **API Endpoint:** `POST /api/users/register`
 **Database Action:** `INSERT INTO users (username, email, password_hash)`


* **Feature:** Update author biography.
* **API Endpoint:** `PATCH /api/users/profile`
* **Database Action:** `UPDATE users SET bio = $1 WHERE user_id = $session_id`


* **Feature:** Validate credentials for login.
* **API Endpoint:** `POST /api/auth/login`
* **Database Action:** `SELECT user_id, password_hash FROM users WHERE email = $input_email`



---

### **2. Content & Taxonomy (The "Publishing" Side)**

* **Feature:** Save a new article.
* **API Endpoint:** `POST /api/articles`
* **Database Action:** `INSERT INTO articles (author_id, title, slug, content)`


* **Feature:** Link an article to a category.
* **API Endpoint:** `POST /api/articles/{id}/tags`
* **Database Action:** `INSERT INTO article_tags (article_id, tag_id)`


* **Feature:** Retrieve article metadata for a card view.
* **API Endpoint:** `GET /api/articles/{slug}`
* **Database Action:** `SELECT a.title, a.content, u.username FROM articles a JOIN users u ON a.author_id = u.user_id WHERE a.slug = $slug`


* **Feature:** Increment global popularity counter.
* **API Endpoint:** (Internal Trigger on Page Load)
* **Database Action:** `UPDATE articles SET view_count = view_count + 1 WHERE article_id = $target_id`



---

### **3. The Diversity Engine (Track B Logic)**

* **Feature:** Log a "Reading Interaction" for the algorithm.
* **API Endpoint:** `POST /api/interactions/log`
* **Database Action:** `INSERT INTO interactions (user_id, article_id, type='read', reading_time_seconds)`


* **Feature:** Identify a user's "Primary Interest" tag.
* **API Endpoint:** `GET /api/analytics/user-bias`
* **Database Action:** `SELECT tag_id FROM interactions JOIN article_tags USING(article_id) WHERE user_id = $id GROUP BY tag_id ORDER BY COUNT(*) DESC LIMIT 1`


* **Feature:** Fetch "Opposite" content for the feed.
* **API Endpoint:** `GET /api/feed/pivot`
* **Database Action:** `SELECT article_id FROM article_tags WHERE tag_id = (SELECT opposite_tag_id FROM tag_mappings WHERE tag_id = $user_bias)`



---

### **4. User Engagement & Curation**

* **Feature:** Bookmark an article for later.
* **API Endpoint:** `POST /api/bookmarks`
* **Database Action:** `INSERT INTO bookmarks (user_id, article_id)`


* **Feature:** Remove a saved bookmark.
* **API Endpoint:** `DELETE /api/bookmarks/{article_id}`
* **Database Action:** `DELETE FROM bookmarks WHERE user_id = $id AND article_id = $article_id`


* **Feature:** Like an article to boost its rank.
* **API Endpoint:** `POST /api/interactions/like`
* **Database Action:** `INSERT INTO interactions (user_id, article_id, type='like')`



---

### **5. Admin & Structural Logic**

* **Feature:** Create a new contrarian relationship.
* **API Endpoint:** `POST /api/admin/tags/map`
* **Database Action:** `INSERT INTO tag_mappings (tag_id, opposite_tag_id)`


* **Feature:** List all system tags for the UI picker.
* **API Endpoint:** `GET /api/tags`
* **Database Action:** `SELECT tag_id, tag_name FROM tags ORDER BY tag_name ASC`



---

Does this technical breakdown align with the specific architecture you're planning to build for the MVP?
