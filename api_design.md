

### **1. User & Identity Management**

* **Feature 1: Register a new user**
* **API Endpoint:** `POST /api/users/register`
* **Database Action:** `INSERT INTO users (username, email, password_hash, is_author)`


* **Feature 2: Login user**
* **API Endpoint:** `POST /api/auth/login`
* **Database Action:** `SELECT * FROM users WHERE email = $input_email`


* **Feature 3: Logout user**
* **API Endpoint:** `POST /api/auth/logout`
* **Database Action:** `INSERT INTO auth_logs (user_id, action, timestamp)`


* **Feature 4: Update author biography**
* **API Endpoint:** `PATCH /api/users/profile`
* **Database Action:** `UPDATE users SET bio = $1 WHERE user_id = $session_id`



---

### **2. Content & Publishing**

* **Feature 5: Create a new article**
* **API Endpoint:** `POST /api/articles`
* **Database Action:** `INSERT INTO articles (author_id, title, slug, content, status='published')`


* **Feature 6: Link tags to article**
* **API Endpoint:** `POST /api/articles/{id}/tags`
* **Database Action:** `INSERT INTO article_tags (article_id, tag_id)` (Max 5 per article)


* **Feature 7: View article details**
* **API Endpoint:** `GET /api/articles/{slug}`
* **Database Action:** `SELECT * FROM articles JOIN users ON articles.author_id = users.user_id WHERE slug = $slug`


* **Feature 8: Update article**
* **API Endpoint:** `PUT /api/articles/{id}`
* **Database Action:** `UPDATE articles SET title, content WHERE id = $id AND author_id = $session_id`


* **Feature 9: Delete article**
* **API Endpoint:** `DELETE /api/articles/{id}`
* **Database Action:** `DELETE FROM articles WHERE id = $id` (Cascades to `article_tags`)



---

### **3. Diversity Engine (The Algorithmic Core)**

* **Feature 10: Log user interaction (Bias Tracking)**
* **API Endpoint:** `POST /api/interactions/log`
* **Database Action:** `INSERT INTO interactions (user_id, article_id, type, reading_time_seconds)`


* **Feature 11: Identify user's primary interest**
* **API Endpoint:** `GET /api/analytics/user-bias`
* **Database Action:** `SELECT tag_id FROM interactions JOIN article_tags USING(article_id) WHERE user_id = $id GROUP BY tag_id ORDER BY COUNT(*) DESC LIMIT 1`


* **Feature 12: Generate contrarian feed (30% Mix)**
* **API Endpoint:** `GET /api/feed/pivot`
* **Database Action:** `SELECT article_id FROM article_tags WHERE tag_id = (SELECT opposite_tag_id FROM tag_mappings WHERE tag_id = $user_bias)`


* **Feature 13: Define tag opposites (Admin)**
* **API Endpoint:** `POST /api/admin/tags/map`
* **Database Action:** `INSERT INTO tag_mappings (tag_id, opposite_tag_id)`



---

### **4. Engagement & Curation**

* **Feature 14: Bookmark an article**
* **API Endpoint:** `POST /api/bookmarks`
* **Database Action:** `INSERT INTO bookmarks (user_id, article_id)`


* **Feature 15: Remove bookmark**
* **API Endpoint:** `DELETE /api/bookmarks/{article_id}`
* **Database Action:** `DELETE FROM bookmarks WHERE user_id = $id AND article_id = $article_id`


* **Feature 16: Like an article**
* **API Endpoint:** `POST /api/interactions/like`
* **Database Action:** `INSERT INTO interactions (user_id, article_id, type='like')`



---

### **5. Discovery & Analytics**

* **Feature 17: Search articles by tag**
* **API Endpoint:** `GET /api/tags/{tag_name}/articles`
* **Database Action:** `SELECT * FROM articles JOIN article_tags USING(article_id) JOIN tags USING(tag_id) WHERE tag_name = $tag_name`


* **Feature 18: Generate Diversity Score**
* **API Endpoint:** `GET /api/users/me/diversity-index`
* **Database Action:** `SELECT COUNT(DISTINCT tag_id) FROM interactions JOIN article_tags USING(article_id) WHERE user_id = $id`


* **Feature 19: View trending articles (Global)**
* **API Endpoint:** `GET /api/articles/trending`
* **Database Action:** `SELECT * FROM articles ORDER BY view_count DESC LIMIT 10`


* **Feature 20: Increment view count**
* **API Endpoint:** (Internal trigger)
* **Database Action:** `UPDATE articles SET view_count = view_count + 1 WHERE id = $id`





