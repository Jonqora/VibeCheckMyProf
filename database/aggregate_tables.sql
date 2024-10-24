-- Average Ratings by Professor
-- Create the table to hold the aggregated data
CREATE TABLE avg_ratings_by_professor AS
SELECT
    p.prof_name,
    AVG(r.quality) AS avg_quality,
    AVG(r.difficulty) AS avg_difficulty,
    COUNT(r.rating_id) AS rating_count
FROM
    professors p
JOIN
    ratings r ON p.prof_id = r.prof_id
GROUP BY
    p.prof_id, p.prof_name;

-- Schedule this query to run periodically (e.g., via MySQL event)
TRUNCATE TABLE avg_ratings_by_professor;
INSERT INTO avg_ratings_by_professor
SELECT
    p.prof_name,
    AVG(r.quality) AS avg_quality,
    AVG(r.difficulty) AS avg_difficulty,
    COUNT(r.rating_id) AS rating_count
FROM
    professors p
JOIN
    ratings r ON p.prof_id = r.prof_id
GROUP BY
    p.prof_id, p.prof_name;


-- Average Ratings by Course
-- Create the table to hold aggregated course rating data
CREATE TABLE avg_ratings_by_course AS
SELECT

    c.course_name,
    AVG(r.quality) AS avg_quality,
    AVG(r.difficulty) AS avg_difficulty,
    COUNT(r.rating_id) AS rating_count
FROM
    courses c
JOIN
    ratings r ON c.course_id = r.course_id
GROUP BY
    c.course_id, c.course_name;

-- Schedule to refresh the table periodically
TRUNCATE TABLE avg_ratings_by_course;
INSERT INTO avg_ratings_by_course
SELECT
    c.course_name,
    AVG(r.quality) AS avg_quality,
    AVG(r.difficulty) AS avg_difficulty,
    COUNT(r.rating_id) AS rating_count
FROM
    courses c
JOIN
    ratings r ON c.course_id = r.course_id
GROUP BY
    c.course_id, c.course_name;


-- Most Active Professors (Based on Rating Count)
-- Create the table
CREATE TABLE active_professors AS
SELECT
    p.prof_name,
    COUNT(r.rating_id) AS rating_count
FROM
    professors p
JOIN
    ratings r ON p.prof_id = r.prof_id
GROUP BY
    p.prof_id, p.prof_name
ORDER BY
    rating_count DESC;

-- Refresh the table periodically
TRUNCATE TABLE active_professors;
INSERT INTO active_professors
SELECT
    p.prof_name,
    COUNT(r.rating_id) AS rating_count
FROM
    professors p
JOIN
    ratings r ON p.prof_id = r.prof_id
GROUP BY
    p.prof_id, p.prof_name
ORDER BY
    rating_count DESC;


-- Sentiment Summary
-- Create the table to hold the sentiment summary for each professor
CREATE TABLE professor_sentiment_summary (
    prof_id         INT,
    prof_name       VARCHAR(100),
    emotion         VARCHAR(20),
    emotion_count   INT,
    rank            INT,
    PRIMARY KEY (prof_id, emotion)
);

-- Insert the top 3 emotions for each professor
INSERT INTO professor_sentiment_summary
SELECT
    p.prof_id,
    p.prof_name,
    s.emotion,
    COUNT(s.sent_id) AS emotion_count,
    ROW_NUMBER() OVER (PARTITION BY p.prof_id ORDER BY COUNT(s.sent_id) DESC) AS rank
FROM
    professors p
JOIN
    ratings r ON p.prof_id = r.prof_id
JOIN
    sentiments s ON r.rating_id = s.rating_id
GROUP BY
    p.prof_id, p.prof_name, s.emotion
HAVING
    rank <= 3; -- Filter only the top 3 emotions

-- Refresh the table periodically
TRUNCATE TABLE professor_sentiment_summary;
INSERT INTO professor_sentiment_summary
SELECT
    p.prof_id,
    p.prof_name,
    s.emotion,
    COUNT(s.sent_id) AS emotion_count,
    ROW_NUMBER() OVER (PARTITION BY p.prof_id ORDER BY COUNT(s.sent_id) DESC) AS rank
FROM
    professors p
JOIN
    ratings r ON p.prof_id = r.prof_id
JOIN
    sentiments s ON r.rating_id = s.rating_id
GROUP BY
    p.prof_id, p.prof_name, s.emotion
HAVING
    rank <= 3;
