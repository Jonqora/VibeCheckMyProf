import ratemyprofessor

school = ratemyprofessor.get_school_by_name("University of British Columbia")
professor = ratemyprofessor.get_professor_by_school_and_name(school, "Gregor Kiczales") 

print("%s works in the %s Department of %s." % (professor.name, professor.department, professor.school.name))
print("Rating: %s / 5.0" % professor.rating)
print("Difficulty: %s / 5.0" % professor.difficulty)
print("Total Ratings: %s" % professor.num_ratings)
# print(professor.comments[0])