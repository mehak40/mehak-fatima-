CREATE DATABASE uni_db0;
USE uni_db0;

CREATE TABLE student(
stu_rollno INT PRIMARY KEY,
stu_name VARCHAR(50),
program VARCHAR(20),
semester VARCHAR(20)
);
INSERT INTO student(stu_rollno,stu_name,program,semester)
VALUES(100,'MAHRUKH','BSIT','second'),
      (150,'Tehreem','BSCs', 'THIRD');
SELECT * FROM student

CREATE TABLE courses(
course_id INT PRIMARY KEY, 
course_name VARCHAR(50),
credithours VARCHAR(50)
);
INSERT INTO courses(course_id,course_name,credithours)
VALUES(303,'Database Systems',25),
      (101,'Operating Systems',25)
SELECT * FROM courses

CREATE TABLE enrollments(
grade VARCHAR,
stu_rollno INT,
course_id INT,

 FOREIGN KEY (stu_rollno) REFERENCES Student(stu_rollno),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
 );
 INSERT INTO enrollments(stu_rollno,course_id,grade)
 VALUES (150,303,'A'),
        (100,101,'B');
SELECT * FROM enrollments

SELECT Student.stu_rollno, stu_name, courses.course_name
FROM Student
JOIN enrollments ON Student.stu_rollno = enrollments.stu_rollno
JOIN courses ON enrollments.course_id = courses.course_id

SELECT Student.stu_rollno, Student.stu_name
FROM Student
JOIN enrollments ON Student.stu_rollno = enrollments.stu_rollno
JOIN Courses ON enrollments.course_id = courses.course_id
WHERE Courses.Course_Name = 'Database Systems';

INSERT INTO Student (stu_rollno,stu_name,program, Semester)
VALUES (10, 'Ali', 'BSCS', 'second');

SELECT *FROM Student

CREATE VIEW StudentView AS
SELECT stu_rollno,stu_name, Program
FROM Student;
SELECT* FROM StudentView;

