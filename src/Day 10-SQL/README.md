# Task 5: Student Performance Analytics

## Overview

This project extends the Python-SQL Student Management System with student performance analytics and course-wise statistics. It retains the existing CRUD operations, filtering, searching, sorting, and Top N student retrieval features.

SQL aggregate functions are used to calculate total students, total marks, average marks, highest marks, and lowest marks. Course-wise analytics use `GROUP BY`, and `HAVING` filters courses based on their average marks.

## Technologies Used

- Python
- SQLite
- sqlite3
- unittest

## Project Structure

- `student.py` - Student class and input validation
- `database.py` - Database connection, CRUD operations, filtering, sorting, and analytics
- `main.py` - Menu-driven Student Management System
- `test_student.py` - Automated tests for validation, CRUD, filtering, sorting, and analytics
- `student_management.db` - SQLite database file

## Database Design

The `students` table contains these columns:

| Column | Data Type | Constraint |
|---|---|---|
| student_id | INTEGER | PRIMARY KEY |
| name | TEXT | NOT NULL |
| age | INTEGER | NOT NULL, CHECK(age > 0) |
| course | TEXT | NOT NULL |
| marks | REAL | NOT NULL, CHECK(marks >= 0 AND marks <= 100) |

## Features

- Adds, displays, searches, updates, and deletes students.
- Searches students by course and partial name.
- Filters students by minimum marks.
- Combines course and marks conditions using `AND`.
- Searches multiple courses using `OR`.
- Sorts students by marks in ascending or descending order.
- Retrieves the Top N students.
- Calculates total students using `COUNT()`.
- Calculates total marks using `SUM()`.
- Calculates average marks using `AVG()`.
- Finds highest and lowest marks using `MAX()` and `MIN()`.
- Displays course-wise student counts and marks statistics using `GROUP BY`.
- Filters courses by minimum average marks using `HAVING`.
- Uses parameterized SQL queries.
- Handles empty database analytics without crashing.
- Preserves deletion confirmation and database connection handling.

## Menu Options

1. Add Student
2. View All Students
3. Search Student by ID
4. Search Student by Course
5. Search Student by Name
6. Filter Students by Marks
7. Sort Students by Marks
8. Top N Students
9. Update Student
10. Delete Student
11. Student Statistics
12. Course-wise Statistics
13. Exit

## Required Analytics Methods

- `get_total_students()` - Returns the total number of students.
- `get_average_marks()` - Returns the average marks.
- `get_total_marks()` - Returns the sum of all marks.
- `get_highest_marks()` - Returns the highest marks.
- `get_lowest_marks()` - Returns the lowest marks.
- `get_course_statistics()` - Returns student count, average, highest, and lowest marks for each course.
- `get_course_average_marks()` - Returns average marks for each course.
- `get_course_highest_marks()` - Returns highest marks for each course.
- `get_course_lowest_marks()` - Returns lowest marks for each course.
- `get_courses_above_average(min_average)` - Returns courses whose average marks are greater than or equal to the specified threshold.

## How to Run

Run these commands from the repository root.

Start the application:

```powershell
python "src/Day 10-SQL/main.py"
```

Run automated tests:

```powershell
python -m unittest discover -s "src/Day 10-SQL" -p "test_student.py" -v
```

Check Python syntax:

```powershell
python -m py_compile "src/Day 10-SQL/main.py" "src/Day 10-SQL/database.py" "src/Day 10-SQL/test_student.py"
```

## Testing

The automated test suite contains 35 tests covering:

- Student validation and duplicate IDs
- Student search, update, and deletion
- Deletion cancellation
- Course and marks filtering
- Partial name search
- Ascending and descending marks sorting
- Top N students
- Invalid input handling
- Combined filtering with `AND` and `OR`
- Total student count and total marks
- Average, highest, and lowest marks
- Course-wise counts and marks statistics
- Courses filtered by minimum average marks
- Invalid minimum average input
- Empty database analytics

**Latest verification:** All 35 tests passed. Python syntax compilation completed without errors.

## Sample Student Records

The automated tests use these records in a temporary database:

- Rahul - 20 - BCA - 82
- Priya - 21 - BCA - 88
- Amit - 20 - BBA - 76
- Neha - 22 - BCA - 91
- Rohit - 21 - BBA - 69

## SQL Concepts Used

- `WHERE` - Filters records based on a condition.
- `AND` - Requires both conditions to be true.
- `OR` - Requires at least one condition to be true.
- `LIKE` - Searches for a matching name pattern.
- `ORDER BY` - Sorts query results.
- `ASC` - Sorts in ascending order.
- `DESC` - Sorts in descending order.
- `LIMIT` - Restricts the number of returned records.
- `COUNT()` - Counts records.
- `SUM()` - Calculates the sum of values.
- `AVG()` - Calculates the average of values.
- `MAX()` - Returns the maximum value.
- `MIN()` - Returns the minimum value.
- `GROUP BY` - Groups records for aggregate calculations.
- `HAVING` - Filters groups based on aggregate conditions.

## Learning Outcomes

- Performing CRUD operations with Python and SQLite.
- Filtering, searching, and sorting student records.
- Combining SQL conditions using `AND` and `OR`.
- Using SQL aggregate functions for performance analytics.
- Grouping records using `GROUP BY`.
- Filtering grouped results using `HAVING`.
- Writing parameterized SQL queries.
- Testing database operations using `unittest`.