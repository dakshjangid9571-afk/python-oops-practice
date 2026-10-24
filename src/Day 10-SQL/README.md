
# Task 2: Robust Student Database with Constraints

## Overview
This project upgrades the Python–SQL Student Management System with database constraints, duplicate ID handling, student search, and validation testing.

## Technologies Used
- Python
- SQLite
- sqlite3
- unittest

## Project Structure
- `student.py` - Student class and input validation
- `database.py` - Database connection, table creation, insertion, and retrieval
- `main.py` - Main application
- `test_student.py` - Automated tests for student validation and database operations
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
- Validates student details using the Student class.
- Prevents duplicate student IDs.
- Displays a friendly message when a duplicate ID is entered.
- Retrieves all student records using SELECT.
- Searches for a student using their ID and WHERE.
- Handles searches for students who do not exist.
- Closes the database connection.

## How to Run
Run these commands from the repository root:

```powershell
python "src/Day 10-SQL/main.py"
```

Run the automated tests:

```powershell
python "src/Day 10-SQL/test_student.py"
```

## Testing
The automated test suite checks these eight cases:

1. Valid student insertion
2. Duplicate student ID
3. Invalid age
4. Invalid marks
5. Empty student name
6. Empty course
7. Search for an existing student
8. Search for a non-existing student

All 8 automated tests passed during verification.

## Sample Student Records
- Rahul - 20 - BCA - 82
- Priya - 21 - BCA - 88
- Amit - 20 - BBA - 76
- Neha - 22 - BCA - 91
- Rohit - 21 - BBA - 69

## Learning Outcomes
- Applying SQL constraints in SQLite.
- Handling duplicate primary keys.
- Using SELECT and WHERE queries.
- Testing validation and database functionality with unittest.
