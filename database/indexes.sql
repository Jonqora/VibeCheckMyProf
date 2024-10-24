# TODO: work with team to strategize indexes

-- If we plan to frequently query professors by their name (for search/filtering)
CREATE INDEX idx_prof_name ON professors (prof_name);

-- Course name index for searching/filtering by course
CREATE INDEX idx_course_name ON courses (course_name);

-- If we plan to often query or filter by department (e.g., for analytics or dashboard filtering)
CREATE INDEX idx_dept ON courses (dept);

-- Foreign key index for prof_id (for joining with professors)
CREATE INDEX idx_prof_id ON ratings (prof_id);

-- Foreign key index for course_id (for joining with courses)
CREATE INDEX idx_course_id ON ratings (course_id);

-- If queries frequently filter or sort by date
CREATE INDEX idx_review_date ON ratings (review_date);

-- For faster queries on rating attributes
CREATE INDEX idx_quality ON ratings (quality);
CREATE INDEX idx_difficulty ON ratings (difficulty);

-- Foreign key index for rating_id (for joining with ratings)
CREATE INDEX idx_rating_id ON sentiments (rating_id);

-- Index on emotion if filtering or aggregating sentiment types
CREATE INDEX idx_emotion ON sentiments (emotion);

-- If queries often filter by emotion confidence
CREATE INDEX idx_emotion_conf ON sentiments (emotion_conf);

-- Index on prof_id to speed up lookups by professor
CREATE INDEX idx_prof_id ON professor_sentiment_summary (prof_id);

-- Index on emotion to quickly filter or aggregate based on emotion type
CREATE INDEX idx_emotion ON professor_sentiment_summary (emotion);

-- Index on rank to optimize sorting by rank (top emotions)
CREATE INDEX idx_rank ON professor_sentiment_summary (rank);