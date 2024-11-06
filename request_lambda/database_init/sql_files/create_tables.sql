# SQL Commands to Create App Tables
CREATE TABLE schools (
    school_id   INT PRIMARY KEY,
    school_name VARCHAR(85) NOT NULL
);

CREATE TABLE professors (
    prof_id             INT PRIMARY KEY,
    prof_name           VARCHAR(100) NOT NULL,
    dept                VARCHAR(100),
    avg_diff            DECIMAL(2,1),
    avg_rating          DECIMAL(2,1),
    would_retake_rate   DECIMAL(6,4),
    rating_count        INT,
    school_id           INT,
    FOREIGN KEY (school_id) REFERENCES schools(school_id)
);

CREATE TABLE requests (
    prof_id             INT PRIMARY KEY NOT NULL,
    request_date        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resulted_in_write   BOOL,
    requested_analysis  BOOL,
    FOREIGN KEY (prof_id) REFERENCES professors(prof_id)
);

CREATE TABLE courses (
    course_id       INT AUTO_INCREMENT PRIMARY KEY,
    school_id       INT,
    course_name     VARCHAR(50) NOT NULL,
    FOREIGN KEY (school_id) REFERENCES schools(school_id)
);

CREATE TABLE ratings (
    rating_id       INT AUTO_INCREMENT PRIMARY KEY,
    prof_id         INT NOT NULL,
    course_id       INT,
    review_date     DATETIME,
    quality         DECIMAL(2,1),
    difficulty      DECIMAL(2,1),
    comment         TEXT,
    take_again      BOOLEAN,
    grade_achieved  VARCHAR(20),
    thumbs_up       INT,
    thumbs_down     INT,
    online_class    BOOLEAN,
    for_credit      BOOLEAN,
    attendance_mand BOOLEAN,
    FOREIGN KEY (prof_id) REFERENCES professors(prof_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE sentiments (
    sent_id         INT AUTO_INCREMENT PRIMARY KEY,
    rating_id       INT,
    sent_date       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    polarity        FLOAT,
    subjectivity    FLOAT,
    emotion         VARCHAR(50),
    sentiment       VARCHAR(50),
    spell_error     INT,
    spell_quality   DECIMAL(5,4),
    FOREIGN KEY (rating_id) REFERENCES ratings(rating_id)
        ON DELETE CASCADE
);

