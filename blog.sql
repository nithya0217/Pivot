Pivot Digital Publishing Platform
Track B: Algorithmic Model (Diversity Routing)
Database: PostgreSQL


1. SCHEMA DEFINITION (TABLES)


Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    bio TEXT,
    is_author BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

 Articles Table
 Note: author_id is logically linked to users.user_id
CREATE TABLE articles (
    article_id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    view_count INTEGER DEFAULT 0,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Tags Table
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(50) UNIQUE NOT NULL
);

Article-Tag Mapping 
CREATE TABLE article_tags (
    article_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL
);

Diversity Engine: Opposite Tag Mapping
Logic: mapping tag_id to its contrarian counterpart
CREATE TABLE tag_mappings (
    tag_id INTEGER NOT NULL,
    opposite_tag_id INTEGER NOT NULL,
    mapping_type VARCHAR(20) DEFAULT 'contrarian'
);

 Interaction Tracking 
 Tracks clicks, likes, and reading time for the algorithm
CREATE TABLE interactions (
    interaction_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    interaction_type VARCHAR(20), -- 'click', 'like', 'bookmark'
    reading_time_seconds INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

 Bookmarks Table
CREATE TABLE bookmarks (
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


2. DUMMY DATA SEEDING


 Seed Users
INSERT INTO users (username, email, password_hash, is_author) VALUES
('tech_guru', 'alex@pivot.com', 'hash_123', TRUE),
('philosophy_queen', 'maya@pivot.com', 'hash_456', TRUE),
('reader_one', 'user1@gmail.com', 'hash_789', FALSE);

Seed Tags
INSERT INTO tags (tag_name) VALUES 
('Technology'), ('Philosophy'), ('Politics-Left'), ('Politics-Right'), ('Fitness'), ('Relaxation');

Seed Tag Mappings (The Diversity Engine Logic)
INSERT INTO tag_mappings (tag_id, opposite_tag_id) VALUES
(1, 2), -- Tech <-> Philosophy
(2, 1), -- Philosophy <-> Tech
(3, 4), -- Left <-> Right
(4, 3), -- Right <-> Left
(5, 6), -- Fitness <-> Relaxation
(6, 5); -- Relaxation <-> Fitness

 Seed Articles
INSERT INTO articles (author_id, title, slug, content) VALUES
(1, 'The Future of AI', 'future-of-ai', 'Content about neural networks...'),
(2, 'The Ethics of Being', 'ethics-of-being', 'Content about existentialism...'),
(1, 'Building a PC in 2026', 'building-pc-2026', 'Content about hardware...');

 Seed Article Tags
INSERT INTO article_tags (article_id, tag_id) VALUES
(1, 1), -- AI is Tech
(2, 2), -- Ethics is Philosophy
(3, 1); -- PC is Tech

 Seed Interactions 
INSERT INTO interactions (user_id, article_id, interaction_type, reading_time_seconds) VALUES
(3, 1, 'click', 120),
(3, 3, 'like', 45),
(3, 1, 'bookmark', 0);


 3. PERFORMANCE INDICES (For Track B Scale)

CREATE INDEX idx_interaction_user ON interactions(user_id);
CREATE INDEX idx_article_author ON articles(author_id);
CREATE INDEX idx_tag_mapping ON tag_mappings(tag_id);
