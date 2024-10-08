# api.py
# scratch work for working with the RateMyProfessorsAPI
# see documentation at https://github.com/Nobelz/RateMyProfessorAPI/blob/master/ratemyprofessor/professor.py

import ratemyprofessor

school = ratemyprofessor.get_school_by_name("University of British Columbia")
prof = ratemyprofessor.get_professor_by_school_and_name(school, "Gregor Kiczales") 
professor = ratemyprofessor.Professor(1835982)

print("%s works in the %s Department of %s." % (professor.name, professor.department, professor.school.name))
print("Rating: %s / 5.0" % professor.rating)
print("Difficulty: %s / 5.0" % professor.difficulty)
print("Total Ratings: %s" % professor.num_ratings)

ratings = professor.get_ratings()
for rating in ratings[:5]:
    # print(rating.date, rating.comment)
    print(rating.rating)
    print(rating.difficulty)
    print(rating.comment)
    print(rating.class_name)
    print(rating.date)
    print(rating.take_again)
    print(rating.grade)
    print(rating.thumbs_up)
    print(rating.thumbs_down)
    print(rating.online_class)
    print(rating.credit)
    print(rating.attendance_mandatory)