"""
Populate database with fake data using the SQLAlchemy ORM.
"""

import random
from faker import Faker
from src.models import Course,Instructor,Department,CourseRegistration,Student, db
from src import create_app
from datetime import time, timedelta 

STUDENT_COUNT = 50
COURSE_COUNT = 10 
DEPARTMENT_COUNT = 20 
INSTRUCTOR_COUNT = 20 
COURSE_REGISTRATION_COUNT = 500

assert COURSE_REGISTRATION_COUNT <= COURSE_COUNT*STUDENT_COUNT

department_names = ["American History",
                    "Electrical Engineering",
                    "Chemistry",
                    "Physics",
                    "Foreign Languages",
                    "American Literature"]

course_dict = {
    "American History": [
        "Early Colonial History",
        "The Civil War",
        "The Gilded Age",
        "The Great Depression"],
    "Electrical Engineering": [
        "Electromagnetics",
        "Cyberphysical Systems",
        "Foundations and Theory"],
    "Chemistry": [
        "General Chemistry",
        "Organic Chemistry",
        "Physical Chemistry",
        "Inorganic Chemistry"
        ],
    "Physics": [
        "General Physics",
        "Advanced Newtonian Mechanics",
        "Quantum Mechanics",
        "Light and Optics"
        ],
    "Foreign Languages": [
        "Chinese",
        "French",
        "German",
        "Spanish",
        "Japanese"
        ],
    "American Literature": [
        "Colonial Literature",
        "The Transcendentalists",
        "The Lost Generation",
        "Complete Works of Mark Twain",
        "Pulp Novels of the 1920s and 1930s",
        "Contemporary Literature"
    ]
}

instructor_dict = {
    "American History": ["Sam Smith","Terry Watkins"],
    "Electrical Engineering": ["Wang Wen Li","Sally Jones"],
    "Chemistry": ["David Crumrine","Anne Levinsons"],
    "Physics": ["Tom Kowalski","Deeprak Siva"],
    "Foreign Languages": ["Harold Wilson"],
    "English Literature": ["Bill Tomson"]
}



def truncate_tables():
    """Delete all rows from database tables"""
    Course.query.delete()
    Instructor.query.delete()
    Department.query.delete()
    Student.query.delete()
    CourseRegistration.query.delete()
    db.session.commit()
    
def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()
    
    last_student = None 
    for _ in range(STUDENT_COUNT):
        last_student = Student(
            name=fake.unique.first_name() + " " + fake.unique.last_name(),
            year=random.randint(1,4)
        )
        db.session.add(last_student)
    
    db.session.commit()
    
    last_department = None 
    
    for dname in department_names:
        last_department = Department(
            name=dname
        )
        print(last_department)
        db.session.add(last_department)
    
    db.session.commit()
    
    last_instructor = None 
    
    for i in range(50):
        dept_pks = [obj.id for obj in Department.query.all()];
        last_instructor = Instructor(
            name=fake.unique.first_name() + " " + fake.unique.last_name(),
            department_id=random.choice(dept_pks)
            )
            
        db.session.add(last_instructor)
    
    db.session.commit()
    
    last_course = None 
    
    for dept_name,course_list in course_dict.items():
        for course_name in course_list:
            dept = Department.query.filter_by(name=dept_name)[0]
            dept_instructor = random.choice(dept.instructors)
            last_course = Course(
                name=course_name,
                instructor_id=dept_instructor.id,
                description=fake.sentence()
            )
            last_course.total_credits = random.randint(2,4)
            db.session.add(last_course)
    
    db.session.commit()
    
    course_student_pairs = set()
    students = Student.query.all()
    student_ids = [obj.id for obj in students]
    courses = Course.query.all()
    course_ids = [obj.id for obj in courses]
    
    while len(course_student_pairs) < COURSE_REGISTRATION_COUNT:
        registration = (
            random.choice(student_ids),
            random.choice(course_ids)
            )
        
        if registration in course_student_pairs:
            continue 
        
        course_student_pairs.add(registration)
    
    for pair in list(course_student_pairs):
        random_start_time = time(hour=random.randint(8,17))
        random_end_time = time(hour=random_start_time.hour+2)
        new_registration = CourseRegistration(
            student_id=pair[0],
            course_id=pair[1],
            semester=random.choice(["Fall","Spring","Summer"]),
            year=random.randint(2022,2023)
            )
        
        new_registration.start_time =random_start_time
        new_registration.end_time =random_end_time
        
        db.session.add(new_registration)
    
    db.session.commit()

#run script 
main()
        
        