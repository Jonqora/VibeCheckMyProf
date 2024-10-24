# Table Schemas - Basic Tables

## professors
| Column        | Data Type    | Description                                          |
|---------------|--------------|------------------------------------------------------|
| prof_id       | INT (PK)     | Unique identifier for the professor (Auto Increment) |
| prof_name     | VARCHAR(100) | Name of the professor                                |
| school_id     | INT (FK)     | Foreign key linking to `schools` table               |
| rating_count  | INT          | Number of ratings                                    |
| avg_qual      | DECIMAL(3,2) | Average quality rating                               |
| avg_diff      | DECIMAL(3,2) | Average difficulty rating                            |
| last_reviewed | DATETIME     | The last time a rating was added                     |

## schools
| Column      | Data Type    | Description                                       |
|-------------|--------------|---------------------------------------------------|
| school_id   | INT (PK)     | Unique identifier for the school (Auto Increment) |
| school_name | VARCHAR(255) | Name of the school                                |

## courses
| Column      | Data Type   | Description                                       |
|-------------|-------------|---------------------------------------------------|
| course_id   | INT (PK)    | Unique identifier for the course (Auto Increment) |
| school_id   | INT (FK)    | Foreign key linking to `schools` table            |
| course_name | VARCHAR(50) | Name of the course (e.g. MATH221)                 |
| dept        | CHAR(4)     | Course department (e.g. MATH)                     |
| level       | INT         | Year-level of course (e.g. 100)                   |

## ratings 
_Denormalized to improve performance of frequently-anticipated queries._

| Column      | Data Type    | Description                                        |
|-------------|--------------|----------------------------------------------------|
| rating_id   | INT (PK)     | Unique identifier for the rating (Auto Increment)  |
| prof_id     | INT (FK)     | Foreign key linking to `professors` table          |
| prof_name   | VARCHAR(100) | Name of the professor                              |
| course_id   | INT (FK)     | Foreign key linking to `courses` table             |
| course_name | VARCHAR(50)  | Name of the course (e.g. MATH221)                  |
| sent_id     | INT (FK)     | Foreign key linking to `sentiments` table          |
| emotion     | VARCHAR(20)  | Predicted emotion of the given rating comment      |
| review_date | DATETIME     | Date the review was posted (e.g. "Nov 20th, 2018") |
| quality     | DECIMAL(3,2) | Quality rating for the course                      |
| difficulty  | DECIMAL(3,2) | Difficulty rating for the course                   |
| comments    | TEXT         | Comments provided by the student                   |

## sentiments
| Column       | Data Type    | Description                                                                |
|--------------|--------------|----------------------------------------------------------------------------|
| sent_id      | INT (PK)     | Unique identifier for the sentiment analysis model output (Auto Increment) |
| sent_date    | DATETIME     | The date and time the rating underwent sentiment analysis                  |
| ml_version   | CHAR(10)     | Version of the model used to perform sentiment analysis                    |
| emotion      | VARCHAR(20)  | Predicted emotion of the given rating comment                              |
| emotion_conf | DECIMAL(3,2) | Confidence of the model for the given prediction                           | 
| spell_error  | DECIMAL(3,2) | Percentage of comment containing poor spelling/grammar                     |

# Table Schemas - Aggregate Tables
## avg_ratings_by_professor
| Column         | Data Type    | Description                                                       |
|----------------|--------------|-------------------------------------------------------------------|
| prof_name      | VARCHAR(100) | Name of the professor                                             |
| avg_quality    | DECIMAL(3,2) | Average quality rating for all courses taught by the professor    |
| avg_difficulty | DECIMAL(3,2) | Average difficulty rating for all courses taught by the professor |
| rating_count   | INT          | Total number of reviews/ratings received for that professor       |

## avg_ratings_by_course
| Column         | Data Type    | Description                                                     |
|----------------|--------------|-----------------------------------------------------------------|
| course_name    | VARCHAR(50)  | Name of the course                                              |
| avg_quality    | DECIMAL(3,2) | Average quality rating for that course across all professors    |
| avg_difficulty | DECIMAL(3,2) | Average difficulty rating for that course across all professors |
| rating_count   | INT          | Total number of reviews/ratings received for that course        |

## active_professors 
_Professor activity measured based on rating count_

| Column         | Data Type    | Description                                                       |
|----------------|--------------|-------------------------------------------------------------------|
| prof_name      | VARCHAR(100) | Name of the professor                                             |
| rating_count   | INT          | Total number of reviews/ratings received for that professor       |

## sentiment_summary
| Column        | Data Type    | Description                                 |
|---------------|--------------|---------------------------------------------|
| prof_id       | INT (PK)     | Unique identifier for the professor         |
| prof_name     | VARCHAR(100) | Name of the professor                       |
| emotion       | VARCHAR(20)  | One of the top three most common emotions   |
| emotion_count | INT          | Count of ratings classified as that emotion |
| rank          | INT          | Ranking amongst the top three               |

