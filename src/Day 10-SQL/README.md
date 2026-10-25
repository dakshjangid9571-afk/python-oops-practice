# Task 6: Student Database Relationships & JOINs

## Overview

This project extends the Python-SQL Student Management System by introducing relational database design, course management, foreign keys, and SQL JOIN operations. It retains the previous student CRUD operations, searching, filtering, sorting, Top N retrieval, and performance analytics.

The system manages courses separately from students and connects them using `course_id`. SQL INNER JOIN displays students with their course names, while LEFT JOIN provides course-wise statistics, including courses without students.

## Technologies Used

- Python
- SQLite
- sqlite3
- unittest

## Project Structure

- `student.py` - Student class and validation
- `course.py` - Course class and validation
- `database.py` - Database connection, course/student CRUD, JOINs, and analytics
- `main.py` - Menu-driven Student Management System
- `test_student.py` - Automated tests for validation, CRUD, JOINs, and analytics
- `student_management.db` - SQLite database file

## Database Design

### Courses Table

| Column | Data Type | Constraint |
|---|---|---|
| course_id | INTEGER | PRIMARY KEY |
| course_name | TEXT | NOT NULL, UNIQUE |

### Students Table

| Column | Data Type | Constraint |
|---|---|---|
| student_id | INTEGER | PRIMARY KEY |
| name | TEXT | NOT NULL |
| age | INTEGER | NOT NULL, CHECK(age > 0) |
| course_id | INTEGER | NOT NULL, FOREIGN KEY references courses(course_id) |
| marks | REAL | NOT NULL, CHECK(marks >= 0 AND marks <= 100) |

## Sample Courses

| Course ID | Course Name |
|---|---|
| 1 | BCA |
| 2 | BBA |
| 3 | MCA |
| 4 | MBA |

## Features

- Adds, displays, searches, updates, and deletes students.
- Adds, displays, searches, and deletes courses.
- Validates student and course input.
- Checks that a course exists before inserting a student.
- Displays students with course names using INNER JOIN.
- Displays course-wise student counts and marks statistics using LEFT JOIN.
- Lists courses without enrolled students.
- Filters students by course and minimum marks.
- Searches students by ID and partial name.
- Sorts students by marks in ascending or descending order.
- Retrieves the Top N students.
- Calculates total students, total marks, average marks, highest marks, and lowest marks.
- Calculates course-wise student counts and marks statistics.
- Uses SQL aggregate functions, GROUP BY, HAVING, and parameterized queries.
- Handles invalid input and empty analytics results.
- Preserves deletion confirmation and database connection handling.

## Menu Options

1. Add Course
2. View Courses
3. Add Student
4. View All Students
5. Search Student
6. Search Students by Course
7. Search Students by Marks
8. Sort Students
9. Top N Students
10. Update Student
11. Delete Student
12. Student Statistics
13. Course-wise Statistics
14. Courses Without Students
15. Exit

## Required Database Methods

### Course Methods

- `create_course_table()` - Creates the courses table.
- `add_course()` - Adds a course.
- `get_all_courses()` - Returns all courses.
- `get_course_by_id()` - Retrieves a course by ID.
- `delete_course()` - Deletes a course when deletion is permitted.

### Student and JOIN Methods

- `get_students_with_courses()` - Returns student records with course names using INNER JOIN.
- `get_course_statistics()` - Returns course-wise student counts and marks statistics, including courses with no students.
- `get_courses_without_students()` - Returns courses without enrolled students.

## How to Run

Run these commands from the repository root.

Start the application:

```powershell
python "src/Day 10-SQL/main.py"
```

Run automated tests:

```powershell
$env:PYTHONPATH = "src\Day 10-SQL"
python -m unittest discover -s "src\Day 10-SQL" -p "test_student.py" -v
```

Check Python syntax:

```powershell
python -m py_compile "src/Day 10-SQL/main.py" "src/Day 10-SQL/database.py" "src/Day 10-SQL/student.py" "src/Day 10-SQL/course.py" "src/Day 10-SQL/test_student.py"
```

## Testing

The automated test suite contains 46 tests covering:

- Course validation and course CRUD operations
- Student validation and student CRUD operations
- Duplicate IDs and invalid course IDs
- Student searching, filtering, sorting, and Top N retrieval
- Deletion confirmation
- Overall student statistics
- INNER JOIN student-course results
- LEFT JOIN course statistics, including empty courses
- Courses without students
- Course-wise average, highest, and lowest marks
- Empty database analytics

**Latest verification:** All 46 tests passed.

## Sample Student Records

| Name | Age | Course ID | Marks |
|---|---:|---:|---:|
| Rahul | 20 | 1 | 82 |
| Priya | 21 | 1 | 88 |
| Amit | 20 | 2 | 76 |
| Neha | 22 | 1 | 91 |
| Rohit | 21 | 2 | 69 |

## SQL Concepts Used

- `PRIMARY KEY` - Uniquely identifies each record.
- `FOREIGN KEY` - Connects students with courses.
- `UNIQUE` - Prevents duplicate course names.
- `CHECK` - Enforces valid age and marks values.
- `WHERE` - Filters records.
- `INNER JOIN` - Returns matching student-course records.
- `LEFT JOIN` - Includes courses without students.
- `GROUP BY` - Groups records for aggregate calculations.
- `HAVING` - Filters groups based on aggregate conditions.
- `COUNT()`, `SUM()`, `AVG()`, `MAX()`, `MIN()` - Perform aggregate calculations.
- `ORDER BY` - Sorts results.
- `LIMIT` - Restricts the number of returned records.

## Learning Outcomes

- Designing relational database tables.
- Using primary keys and foreign keys.
- Managing students and courses with Python and SQLite.
- Retrieving related records using INNER JOIN and LEFT JOIN.
- Calculating course-wise statistics.
- Identifying courses without students.
- Testing database functionality using `unittest`.
