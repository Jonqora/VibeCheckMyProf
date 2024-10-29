# test_frontend.py

# ----------------------------------------------------------------------------#
# NOTE: this is a test file stub, generated by ChatGPT. The stub functions in
# your file may not be easy or even possible to test. Instead, use this file
# to test smaller functions and helper functions where you can.
# ----------------------------------------------------------------------------#

import json
import os
import unittest
from collections import defaultdict

from app import frontend


class TestFrontend(unittest.TestCase):
    def setUp(self):
        # Example data for tests
        self.professor_data = {
            "reviews": [
                {
                    "quality": 5,
                    "difficulty": 4,
                    "comment": "His lectures are engaging and this class had tons of online resources available (mini-lecture videos covering specific topics, finals from different years, for example).  He's active on piazza and he's approachable during office hours and immediately after the lecture. Never made me feel dumb for having a question :) final was difficult tho lol",
                    "class_name": "MATH221",
                    "date": "2024-05-10 19:50:00",
                    "take_again": True,
                    "grade": "A+",
                    "thumbs_up": 0,
                    "thumbs_down": 2,
                    "online_class": False,
                    "credit": True,
                    "attendance_mandatory": False,
                    "vcmp_polarity": 0.1622,
                    "vcmp_subjectivity": 0.1567,
                    "vcmp_emotion": "nervousness",
                    "vcmp_sentiment": "negative",
                    "vcmp_spellingerrors": 1,
                    "vcmp_spellingquality": 0.9317
                },
                {
                    "quality": 4,
                    "difficulty": 4,
                    "comment": "221 is one of the easiest 200 level math courses, so it's relatively easy to do well on the midterms. However, the final was what knocked our grades down. IT WAS HARD. Ben only scaled those who missed a midterm and those who did so bad on the midterms that they're depending on the final to survive, so it was kinda unfair to other students.",
                    "class_name": "MATH221",
                    "date": "2024-05-05 18:37:21",
                    "take_again": True,
                    "grade": "B-",
                    "thumbs_up": 0,
                    "thumbs_down": 1,
                    "online_class": False,
                    "credit": True,
                    "attendance_mandatory": False,
                    "vcmp_polarity": 0.2042,
                    "vcmp_subjectivity": 0.7685,
                    "vcmp_emotion": "remorse",
                    "vcmp_sentiment": "negative",
                    "vcmp_spellingerrors": 0,
                    "vcmp_spellingquality": 0.9719
                },
                {
                    "quality": 5,
                    "difficulty": 4,
                    "comment": "As long as you review the class everyday, you will be ok. The professor is the best",
                    "class_name": "MATH220",
                    "date": "2024-04-23 21:36:42",
                    "take_again": True,
                    "grade": "B-",
                    "thumbs_up": 0,
                    "thumbs_down": 2,
                    "online_class": False,
                    "credit": True,
                    "attendance_mandatory": False,
                    "vcmp_polarity": 0.2283,
                    "vcmp_subjectivity": 0.3236,
                    "vcmp_emotion": "anger",
                    "vcmp_sentiment": "neutral",
                    "vcmp_spellingerrors": 1,
                    "vcmp_spellingquality": 0.9416
                },
            ],
            "num_ratings": 3,
        }


    def test_format(self):
        data = self.professor_data

        formatted_data = frontend.format(data)

        # Check if the courses are formatted correctly
        self.assertIn("courses", formatted_data)
        self.assertEqual(len(formatted_data["courses"]), 2)

        # Check if aggregate fields are calculated
        self.assertAlmostEqual(formatted_data["vcmp_polarity"], 0.198233, places=4)
        self.assertAlmostEqual(formatted_data["vcmp_subjectivity"], 0.416267, places=4)
        self.assertEqual(formatted_data["vcmp_sentiment"]["negative"], 2)
        self.assertEqual(formatted_data["vcmp_sentiment"]["neutral"], 1)

        # Check for course details
        MATH221 = next(
            course for course in formatted_data["courses"]
            if course["course_name"] == "MATH221"
        )
        self.assertEqual(MATH221["num_ratings"], 2)
        self.assertAlmostEqual(MATH221["difficulty"], 4.0)
        self.assertAlmostEqual(MATH221["rating"], 4.5)


    def test_init_prof(self):
        data = self.professor_data
        frontend.init_prof(data)
        self.assertEqual(data["sum_vcmp_polarity"], 0)
        self.assertEqual(data["sum_vcmp_subjectivity"], 0)
        self.assertIsInstance(data["sum_vcmp_emotion"], defaultdict)
        self.assertEqual(data["sum_vcmp_sentiment"], {
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0,
                    "mixed": 0
                    })
        self.assertEqual(data["sum_vcmp_spellingerrors"], 0)
        self.assertEqual(data["sum_vcmp_spellingquality"], 0)
        self.assertEqual(data["course_dict"], {})


    def test_sum_prof_from_review(self):
        data = self.professor_data
        review = data["reviews"][0]
        frontend.init_prof(data)
        frontend.sum_prof_from_review(data, review)
        self.assertEqual(data["sum_vcmp_polarity"], 0.1622)
        self.assertEqual(data["sum_vcmp_subjectivity"], 0.1567)
        self.assertIsInstance(data["sum_vcmp_emotion"], defaultdict)
        self.assertEqual(data["sum_vcmp_emotion"]["nervousness"], 1)
        self.assertEqual(data["sum_vcmp_sentiment"], {
                    "positive": 0,
                    "negative": 1,
                    "neutral": 0,
                    "mixed": 0
                    })
        self.assertEqual(data["sum_vcmp_spellingerrors"], 1)
        self.assertEqual(data["sum_vcmp_spellingquality"], 0.9317)


    def test_init_course(self):
        data = self.professor_data
        frontend.init_prof(data)
        frontend.init_course(data, "MATH221")
        self.assertIn("MATH221", data["course_dict"])
        self.assertEqual(
            data["course_dict"]["MATH221"]["course_name"],
            "MATH221"
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["num_ratings"],
            0
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_difficulty"],
            0
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_rating"],
            0
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_polarity"],
            0
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_subjectivity"],
            0
            )
        self.assertIsInstance(
            data["course_dict"]["MATH221"]["sum_vcmp_emotion"], 
            defaultdict
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_sentiment"], {
                "positive": 0,
                "negative": 0,
                "neutral": 0,
                "mixed": 0
                })
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_spellingerrors"],
            0
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_spellingquality"],
            0
            )


    def test_sum_course_from_review(self):
        data = self.professor_data
        frontend.init_prof(data)
        frontend.init_course(data, "MATH221")
        review = data["reviews"][0]
        frontend.sum_course_from_review(data, "MATH221", review)
        self.assertEqual(data["course_dict"]["MATH221"]["num_ratings"], 1)
        self.assertEqual(data["course_dict"]["MATH221"]["sum_difficulty"], 4)
        self.assertEqual(data["course_dict"]["MATH221"]["sum_rating"], 5)
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_polarity"], 0.1622
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_subjectivity"], 0.1567)
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_emotion"]["nervousness"], 
            1
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_sentiment"]["negative"], 
            1
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_spellingerrors"], 1)
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_spellingquality"], 
            0.9317
            )
        

    def test_sum_course_from_review_repeated(self):
        data = self.professor_data
        frontend.init_prof(data)
        frontend.init_course(data, "MATH221")
        review1 = data["reviews"][0]
        review2 = data["reviews"][1]
        frontend.sum_course_from_review(data, "MATH221", review1)
        frontend.sum_course_from_review(data, "MATH221", review2)
        self.assertEqual(data["course_dict"]["MATH221"]["num_ratings"], 2)
        self.assertEqual(data["course_dict"]["MATH221"]["sum_difficulty"], 8)
        self.assertEqual(data["course_dict"]["MATH221"]["sum_rating"], 9)
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_polarity"], 0.3664
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_subjectivity"], 0.9252)
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_emotion"]["nervousness"], 
            1
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_emotion"]["remorse"], 
            1
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_sentiment"]["negative"], 
            2
            )
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_spellingerrors"], 1)
        self.assertEqual(
            data["course_dict"]["MATH221"]["sum_vcmp_spellingquality"], 
            1.9036
            )


    def test_calculate_prof_and_cleanup(self):
        data = self.professor_data
        frontend.init_prof(data)
        frontend.init_course(data, "MATH221")
        frontend.init_course(data, "MATH220")
        review1 = data["reviews"][0]
        review2 = data["reviews"][1]
        review3 = data["reviews"][2]
        frontend.sum_prof_from_review(data, review1)
        frontend.sum_prof_from_review(data, review2)
        frontend.sum_prof_from_review(data, review3)
        frontend.sum_course_from_review(data, "MATH221", review1)
        frontend.sum_course_from_review(data, "MATH221", review2)
        frontend.sum_course_from_review(data, "MATH220", review3)
        frontend.calculate_prof_and_cleanup(data)
        
        self.assertNotIn("sum_vcmp_polarity", data)
        self.assertNotIn("sum_vcmp_subjectivity", data)
        self.assertNotIn("sum_vcmp_emotion", data)
        self.assertNotIn("sum_vcmp_sentiment", data)
        self.assertNotIn("sum_vcmp_spellingerrors", data)
        self.assertNotIn("sum_vcmp_spellingquality", data)

        self.assertAlmostEqual(data["vcmp_polarity"], 0.1982, 4)
        self.assertAlmostEqual(data["vcmp_subjectivity"], 0.4163, 4)
        self.assertEqual(data["vcmp_emotion"][0][0], "anger")
        self.assertEqual(data["vcmp_emotion"][0][1], 1)
        self.assertEqual(data["vcmp_emotion"][1][0], "nervousness")
        self.assertEqual(data["vcmp_emotion"][1][1], 1)
        self.assertEqual(data["vcmp_emotion"][2][0], "remorse")
        self.assertEqual(data["vcmp_emotion"][2][1], 1)
        self.assertEqual(data["vcmp_sentiment"]["negative"], 2)
        self.assertEqual(data["vcmp_sentiment"]["neutral"], 1)
        self.assertAlmostEqual(data["vcmp_spellingerrors"], 2 / 3, 4)
        self.assertAlmostEqual(data["vcmp_spellingquality"], 0.9484, 4)


    def test_calculate_course_and_cleanup(self):
        data = self.professor_data
        frontend.init_prof(data)
        frontend.init_course(data, "MATH221")
        review1 = data["reviews"][0]
        review2 = data["reviews"][1]
        frontend.sum_course_from_review(data, "MATH221", review1)
        frontend.sum_course_from_review(data, "MATH221", review2)
        frontend.calculate_prof_and_cleanup(data)
        courses = sorted(
            data["course_dict"].values(),
            key = lambda x : x["num_ratings"],
            reverse = True
            )
        data["courses"] = []
        course = courses[0]
        frontend.calculate_course_and_cleanup(course)

        self.assertNotIn("sum_difficulty", course)
        self.assertNotIn("sum_rating", course)
        self.assertNotIn("sum_vcmp_polarity", course)
        self.assertNotIn("sum_vcmp_subjectivity", course)
        self.assertNotIn("sum_vcmp_emotion", course)
        self.assertNotIn("sum_vcmp_sentiment", course)
        self.assertNotIn("sum_vcmp_spellingerrors", course)
        self.assertNotIn("sum_vcmp_spellingquality", course)

        self.assertEqual(course["difficulty"], 4.0)
        self.assertEqual(course["rating"], 4.5)
        self.assertEqual(course["vcmp_polarity"], 0.1832)
        self.assertEqual(course["vcmp_subjectivity"], 0.4626)
        self.assertEqual(course["vcmp_emotion"][0][0], "nervousness")
        self.assertEqual(course["vcmp_emotion"][0][1], 1)
        self.assertEqual(course["vcmp_emotion"][1][0], "remorse")
        self.assertEqual(course["vcmp_emotion"][1][1], 1)
        self.assertEqual(course["vcmp_sentiment"]["negative"], 2)
        self.assertEqual(course["vcmp_spellingerrors"], 0.5)
        self.assertEqual(course["vcmp_spellingquality"], 0.9518)



if __name__ == "__main__":
    unittest.main()
