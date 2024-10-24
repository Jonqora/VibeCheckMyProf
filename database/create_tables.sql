CREATE TABLE professors (
    prof_id         INT AUTO_INCREMENT  PRIMARY KEY,
    prof_name       VARCHAR(100)        NOT NULL,
    school_id       INT,
    rating_count    INT,
    avg_quality     DECIMAL(3,2),
    avg_difficulty  DECIMAL(3,2),
    last_reviewed   DATETIME,
    FOREIGN KEY (school_id) REFERENCES schools(school_id)
);

CREATE TABLE schools (
    school_id   INT            AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(50)    NOT NULL
);

CREATE TABLE courses (
    course_id       INT           AUTO_INCREMENT PRIMARY KEY,
    school_id       INT,
    course_name     VARCHAR(50)   NOT NULL,
    dept            CHAR(4),
    level           INT,
    FOREIGN KEY (school_id) REFERENCES schools(school_id)
);

CREATE TABLE ratings (
    rating_id       INT AUTO_INCREMENT PRIMARY KEY,
    prof_id         INT,
    prof_name       VARCHAR(100),
    course_id       INT,
    course_name     VARCHAR(50),
    sent_id         INT,
    review_date     DATETIME,
    quality         DECIMAL(3,2),
    difficulty      DECIMAL(3,2),
    comments        TEXT,
    FOREIGN KEY (prof_id)   REFERENCES professors(prof_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (sent_id)   REFERENCES sentiments(sent_id)
);

CREATE TABLE sentiments (
    sent_id INT AUTO_INCREMENT PRIMARY KEY,
    sent_date DATETIME,
    ml_version CHAR(10),
    emotion VARCHAR(20),
    emotion_conf DECIMAL(3,2),
    spell_error DECIMAL(3,2),
    comments TEXT
);