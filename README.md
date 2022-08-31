# Courses Website 

## A Course Management System 

## API Reference Table

# Endpoints

***Courses***

> GET, POST /courses
>> Allows the user to view all courses or add a new course

> GET,POST,DELETE /courses/course_id 

> GET /courses/course_id/registrations

***Departments***

> GET,POST /departments

> GET,POST, DELETE /departments/department_id 

> GET /departments/department_id/instructors

***Instructors***

> GET,POST /instructors

> GET,POST, DELETE /instructors/instructor_id 

> GET /instructors/instructor_id/taught_courses

***Students***

> GET,POST /students

> GET,POST, DELETE /students/student_id 

> GET /students/student_id/registrations

### Notes

Originally, I started with a very complicated entity-relationship model diagram.  It made it difficult to generate large amounts of seed data.  I went back and revised by ER diagram to make it simpler so that it would be easier to generate seed data. 

I chose the ORM approach because it's easy to generate seed data using Python tools such as Faker as well as the random module.  For the future, I hope add more attributes to each of the models so that there are more columns in each data table.  This will allow the app to keep track of more data.
