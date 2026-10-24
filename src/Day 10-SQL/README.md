
# Task 4: Student Filtering and Sorting

## Overview

This project extends the Python-SQL Student Management System with student filtering, partial name searching, sorting, and Top N student retrieval. It retains all existing CRUD operations and uses parameterized SQL queries.

## Technologies Used

- Python
- SQLite
- sqlite3
- unittest

## Project Structure

- `student.py` - Student class and input validation
- `database.py` - Database connection, CRUD operations, filtering, and sorting
- `main.py` - Menu-driven Student Management System
- `test_student.py` - Automated tests for validation, CRUD, filtering, and sorting
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
- Searches students by course using `WHERE`.
- Filters students by minimum marks using `WHERE` and `>=`.
- Searches names partially using `LIKE`.
- Combines course and marks conditions using `AND`.
- Searches multiple courses using `OR`.
- Sorts students by marks in ascending or descending order using `ORDER BY`.
- Retrieves the Top N students using `ORDER BY marks DESC LIMIT`.
- Uses parameterized SQL queries.
- Validates course, marks, and Top N input.
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
11. Exit

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

## Testing

The automated test suite contains 23 tests covering:

- Student validation and duplicate IDs
- Student search, update, and deletion
- Deletion cancellation
- Course filtering
- Minimum marks filtering
- Partial name search
- Ascending and descending marks sorting
- Top N students
- Invalid marks and Top N input
- Combined course and marks filtering with `AND`
- Multiple-course filtering with `OR`

**Latest verification:** All 23 tests passed.

## Sample Student Records

The tests use these records in a temporary database:

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

## Learning Outcomes

- Performing CRUD operations with Python and SQLite.
- Filtering and searching student records.
- Combining conditions using `AND` and `OR`.
- Sorting query results using `ORDER BY`.
- Retrieving a limited number of records using `LIMIT`.
- Writing parameterized SQL queries.
- Testing database operations using `unittest`.
