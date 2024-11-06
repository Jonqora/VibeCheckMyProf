# Table Schemas - Basic Tables

## schools
| Column      | Data Type   | Description                                 |
|-------------|-------------|---------------------------------------------|
| school_id   | INT (PK)    | Unique identifier for the school (from RMP) |
| school_name | VARCHAR(85) | Name of the school                          |

## professors
| Column            | Data Type    | Description                                          |
|-------------------|--------------|------------------------------------------------------|
| prof_id           | INT (PK)     | Unique identifier for the professor (from RMP)       |
| prof_name         | VARCHAR(100) | Name of the professor                                |
| dept              | VARCHAR(100) | Department professor is affiliated with              | 
| avg_diff          | DECIMAL(2,1) | Average difficulty rating                            |
| avg_rating        | DECIMAL(2,1) | Average overall rating                               |
| would_retake_rate | DECIMAL(6,4) | Percentage of reviewers that would retake the course | 
| rating_count      | INT          | Number of ratings                                    |
| school_id         | INT (FK)     | Foreign key linking to `schools` table               |

## requests
| Column            | Data Type | Description                                      |
|-------------------|-----------|--------------------------------------------------|
| prof_id            | INT (FK)  | Foreign key linking to `professors` table        |
| request_date       | TIMESTAMP | Date the user request came in                    | 
| resulted_in_write  | BOOLEAN   | Whether the request resulted in a database write |
| requested_analysis | BOOLEAN   | Whether a new analysis was requested  |

## courses
| Column      | Data Type   | Description                                       |
|-------------|-------------|---------------------------------------------------|
| course_id   | INT (PK)    | Unique identifier for the course (Auto Increment) |
| school_id   | INT (FK)    | Foreign key linking to `schools` table            |
| course_name | VARCHAR(50) | Name of the course (e.g. MATH221)                 |

## ratings
| Column          | Data Type    | Description                                                       |
|-----------------|--------------|-------------------------------------------------------------------|
| rating_id       | INT (PK)     | Unique identifier for the rating (Auto Increment)                 |
| prof_id         | INT (FK)     | Foreign key linking to `professors` table                         |
| course_id       | INT (FK)     | Foreign key linking to `courses` table                            |
| review_date     | DATETIME     | Date the review was posted (e.g. "Nov 20th, 2018")                |
| quality         | DECIMAL(2,1) | Quality rating for the course                                     |
| difficulty      | DECIMAL(2,1) | Difficulty rating for the course                                  |
| comment         | TEXT         | Comment/textual review provided by the student                    |
| take_again      | BOOLEAN      | True if student would take the course again                       |
| grade_achieved  | VARCHAR(20)  | Final grade student achieved (e.g. "A+")                          |
| thumbs_up       | INT          | Count of viewers that gave the review a "thumbs-up"               |
| thumbs_down     | INT          | Count of viewers that gave the review a "thumbs-down"             |
| online_class    | BOOLEAN      | Indicates whether the course was delivered online                 |
| for_credit      | BOOLEAN      | Indicates whether the course was taken for credit                 |
| attendance_mand | BOOLEAN      | Indicates if performance in the course requires attending lecture |

## sentiments
| Column        | Data Type    | Description                                                                |
|---------------|--------------|----------------------------------------------------------------------------|
| sent_id       | INT (PK)     | Unique identifier for the sentiment analysis model output (Auto Increment) |
| rating_id     | INT (PK)     | Foreign key linking to `ratings` table                                     |
| sent_date     | TIMESTAMP    | The date and time the rating underwent sentiment analysis                  |
| polarity      | FLOAT        | Range [-1.0, 1.0], where -1 is negative and 1 is positive.                 |
| subjectivity  | FLOAT        | Range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective    |
| emotion       | VARCHAR(50)  | Predicted emotion of the given rating comment (e.g. "angry")               |
| sentiment     | VARCHAR(50)  | Polarity as a categorical construct (e.g. "positive")                      | 
| spell_error   | INT          | Count of spelling errors in the text                                       |
| spell_quality | DECIMAL(5,4) | Quality of text, where 1.0 indicates no error.                             |
