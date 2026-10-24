
# Task 3: Student CRUD Operations

## Overview
This project upgrades the Python-SQL Student Management System with Create, Read, Update, and Delete (CRUD) operations, student validation, safe SQL queries, and deletion confirmation.

## Technologies Used
- Python
- SQLite
- sqlite3
- unittest

## Project Structure
- `student.py` - Student class and input validation using `Student.validate()`
- `database.py` - Database connection, table creation, and CRUD operations
- `main.py` - Menu-driven Student Management System
- `test_student.py` - Automated tests for validation and database operations
- `student_management.db` - SQLite database file

## Database Design
The `students` table contains the following columns:

| Column | Data Type | Constraint |
|---|---|---|
| student_id | INTEGER | PRIMARY KEY |
| name | TEXT | NOT NULL |
| age | INTEGER | NOT NULL, CHECK(age > 0) |
| course | TEXT | NOT NULL |
| marks | REAL | NOT NULL, CHECK(marks >= 0 AND marks <= 100) |

## Features
- Connects to an SQLite database.
- Creates the students table with required constraints.
- Validates student details using `Student.validate()`.
- Adds students using INSERT.
- Displays all students using SELECT.
- Searches for students using SELECT and WHERE.
- Updates student details using UPDATE and WHERE.
- Keeps the student ID unchanged during updates.
- Deletes students using DELETE and WHERE.
- Uses parameterized SQL queries.
- Uses `cursor.rowcount` to check affected records.
- Displays student details and asks for confirmation before deletion.
- Cancels deletion when the user does not confirm.
- Handles duplicate IDs, invalid input, and missing students.
- Closes the database connection when exiting.

## Menu Options
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit

## How to Run
Run these commands from the repository root.

Start the application:

```powershell
python "src/Day 10-SQL/main.py"
```

Run the automated tests:

```powershell
python "src/Day 10-SQL/test_student.py"
```

## Testing
The automated test suite checks these 13 cases:

1. Valid student insertion
2. Duplicate student ID
3. Invalid age
4. Invalid marks
5. Empty student name
6. Empty course
7. Search for an existing student
8. Search for a non-existing student
9. Update student marks successfully
10. Reject invalid marks during update without changing the database
11. Delete an existing student
12. Handle deletion of a missing student
13. Cancel deletion and preserve the record

All 13 automated tests passed during verification.

## Sample Student Records
The test suite uses these sample records in a temporary database:

- Rahul - 20 - BCA - 82
- Priya - 21 - BCA - 88
- Amit - 20 - BBA - 76
- Neha - 22 - BCA - 91
- Rohit - 21 - BBA - 69

## Learning Outcomes
- Performing CRUD operations using Python and SQLite.
- Applying SQL constraints and parameterized queries.
- Using SELECT, WHERE, UPDATE, and DELETE.
- Validating student details during insertion and updating.
- Using `cursor.rowcount` to identify affected records.
- Implementing deletion confirmation.
- Testing database operations with unittest.
