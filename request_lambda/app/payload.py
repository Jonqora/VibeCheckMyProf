from datetime import datetime
from dataclasses import field, dataclass
from typing import Dict, Any


@dataclass
class Professor:
    """ Class to store professors table attributes. """
    prof_id: int
    prof_name: str
    school_id: int
    school_name: str
    dept: str
    avg_diff: float
    avg_rating: float
    would_retake_rate: float
    rating_count: int
    reviews: Dict[str, Any]

    def __init__(self, professor_dict: Dict[str, any]):
        self.prof_id = professor_dict["professor_id"]
        self.prof_name = professor_dict["name"]
        self.school_id = professor_dict["school_id"]
        self.school_name = professor_dict["school_name"]
        self.dept = professor_dict["department"]
        self.avg_diff = professor_dict["difficulty"]
        self.avg_rating = professor_dict["rating"]
        self.would_retake_rate = professor_dict["would_take_again"]
        self.rating_count = professor_dict["num_ratings"]
        self.reviews = professor_dict["reviews"]


@dataclass
class Rating:
    """ Class to store ratings table attributes. """
    rating_id: int = field(init=False)
    prof_id: int
    review_date: datetime
    quality: float
    difficulty: float
    comment: str
    take_again: bool
    grade_achieved: str
    thumbs_up: int
    thumbs_down: int
    online_class: bool
    for_credit: bool
    attendance_mand: bool
    course_id: int

    def __init__(self, review: Dict[str, any], prof_id: int, course_id: int):
        self.prof_id = prof_id
        self.review_date = datetime.strptime(review["date"],
                                             "%Y-%m-%d %H:%M:%S")
        self.quality = review["quality"]
        self.difficulty = review["difficulty"]
        self.comment = review["comment"]
        self.take_again = review["take_again"]
        self.grade_achieved = review["grade"]
        self.thumbs_up = review["thumbs_up"]
        self.thumbs_down = review["thumbs_down"]
        self.online_class = review["online_class"]
        self.for_credit = review["credit"]
        self.attendance_mand = review["attendance_mandatory"]
        self.course_id = course_id

    def __add__(self, rating_id):
        self.rating_id = rating_id


@dataclass
class Sentiment:
    """ Class to store sentiments table attributes. """
    polarity: float
    subjectivity: float
    emotion: str
    sentiment: str
    spell_error: int
    spell_quality: float
    rating_id: int

    def __init__(self, review: Dict[str, any], rating_id: int):
        self.rating_id = rating_id
        self.polarity = review["vcmp_polarity"]
        self.subjectivity = review["vcmp_subjectivity"]
        self.emotion = review["vcmp_emotion"]
        self.sentiment = review["vcmp_sentiment"]
        self.spell_error = review["vcmp_spellingerrors"]
        self.spell_quality = review["vcmp_spellingquality"]
