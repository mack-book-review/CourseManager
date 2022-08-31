from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import datetime 

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),unique=True,nullable=False)
    instructors = relationship('Instructor',backref='departments')

    def __init__(self,name: str):
        self.name = name 
    
    def serialize(self):
        return {
            'id':self.id, 
            'name':self.name
        }
        
class Instructor(db.Model):
    __tablename__ = "instructors"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    department_id = db.Column(
        db.Integer,
        db.ForeignKey('departments.id',ondelete='SET NULL'),
        nullable=True
        )
    courses = relationship('Course',backref="instructors")
    
    def __init__(self,name: str,department_id:int):
        self.name = name 
        self.department_id = department_id
        
    def serialize(self):
        return {
            'id':self.id, 
            'name':self.name,
            'department_id':self.department_id
        }
        
class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    
    instructor_id = db.Column(db.Integer,
            db.ForeignKey('instructors.id',ondelete="SET NULL"),
            nullable=False)
    name = db.Column(db.String(100),unique=True,nullable=True)
    description = db.Column(db.String(100),nullable=True)
    total_credits = db.Column(db.Integer,nullable=True)
    registrations = relationship('CourseRegistration',backref="courses")
    
    def __init__(self,name: str,instructor_id: int, description: str):
        self.name = name 
        self.instructor_id = instructor_id
        self.description = description
    
    def serialize(self):
        return {
            'id':self.id, 
            'name':self.name,
            'instructor_id':self.instructor_id,
            'description':self.description,
            'total_credits':self.total_credits
        }
        
class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    year = db.Column(db.Integer,nullable=False)
    registrations = relationship('CourseRegistration',backref="students")

    def __init__(self,name: str,year:int):
        self.name = name 
        self.year = year
    
    def serialize(self):
        return {
            'id':self.id, 
            'name':self.name,
            'year':self.year
        }
        
class CourseRegistration(db.Model):
    __tablename__ = "course_registrations"
    course_id = db.Column(db.Integer,
        db.ForeignKey('courses.id',ondelete="CASCADE"),
        primary_key=True)
    student_id = db.Column(db.Integer,
        db.ForeignKey('students.id',ondelete="CASCADE"),
        primary_key=True)
    semester = db.Column(db.String(100),nullable=False)
    year = db.Column(db.Integer,nullable=False)
    start_time = db.Column(db.Time,nullable=True)
    end_time = db.Column(db.Time,nullable=True)
     
    def __init__(self,
                 student_id: int,
                 course_id: int,
                 semester: str, 
                 year: int):
        self.student_id = student_id
        self.course_id = course_id
        self.semester = semester 
        self.year = year 
    
    def serialize(self):
        return {
            'student_id':self.student_id, 
            'course_id':self.course_id,
            'year':self.year,
            'semester':self.semester,
        }
# registration_table = db.Table(
#     'registrations',
#     db.Column('student_id',
#               db.Integer,
#               db.ForeignKey('students.id'),
#               primary_key=True
#             ),
    
#      db.Column('course_id',
#               db.Integer,
#               db.ForeignKey('courses.id'),
#               primary_key=True
#             ),
# )
