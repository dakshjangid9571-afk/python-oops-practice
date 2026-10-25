# Task 7: Database Transactions & ACID

## Overview

This project extends the Python-SQL Student Management System with database transactions and transaction history tracking. It retains the previous student CRUD operations, course management, searching, filtering, sorting, JOIN operations, and performance analytics.

The system supports transferring a student from one course to another using database transactions. Each successful transfer updates the student's course and records the transfer in the `student_course_history` table.

Transactions help maintain data consistency. If any part of a transfer fails, the transaction is rolled back so that incomplete changes are not saved.

## Technologies Used

- Python
- SQLite
- sqlite3
- unittest
- SQL Transactions

## Project Structure

- `student.py` - Student class and validation
- `course.py` - Course class and validation
- `database.py` - Database connection, student/course operations, JOINs, analytics, transactions, and transfer history
- `main.py` - Menu-driven Student Management System
- `test_student.py` - Automated tests for validation, CRUD, JOINs, analytics, and transactions
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

### Student Course History

The `student_course_history` table records successful student course transfers. It maintains a history of course changes for tracking and verification.

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
- Transfers a student from one course to another.
- Records successful course transfers in `student_course_history`.
- Uses database transactions to maintain consistent data.
- Commits a transfer only after the required operations succeed.
- Rolls back changes if a transfer operation fails.
- Retrieves course transfer history.
- Supports viewing transfer history for a particular student.
- Uses parameterized SQL queries and handles database errors.

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
15. Transfer Student Course
16. View Course Transfer History
17. Exit

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

### Transaction and History Methods

- `create_history_table()` - Creates the student course history table.
- `begin_transaction()` - Begins a database transaction.
- `commit()` - Commits a successful transaction.
- `rollback()` - Rolls back a failed transaction.
- `transfer_student_course()` - Transfers a student to another course within a transaction.
- `get_course_history()` - Retrieves course transfer history.
- `get_student_course_history()` - Retrieves transfer history for a particular student.

## Database Transactions and ACID

### Atomicity

A course transfer is treated as a single unit of work. If an operation fails, the transaction is rolled back instead of saving only part of the transfer.

### Consistency

Student and course relationships must remain valid. A transfer must use a valid student and destination course.

### Isolation

Database transactions provide a mechanism for controlling how changes are handled while a transaction is in progress.

### Durability

Once a transaction is successfully committed, its changes are saved to the database.

## How to Run

Run these commands from the repository root.

### Start the Application

```powershell
python "src/Day 10-SQL/main.py"
```

### Run Automated Tests

```powershell
$env:PYTHONPATH = "src\Day 10-SQL"
python -m unittest discover -s "src/Day 10-SQL" -p "test_student.py" -v
```

### Check Python Syntax

```powershell
python -m py_compile "src/Day 10-SQL/main.py" "src/Day 10-SQL/database.py" "src/Day 10-SQL/student.py" "src/Day 10-SQL/course.py" "src/Day 10-SQL/test_student.py"
```

## Testing

The automated test suite contains **51 tests** covering:

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
- Successful student course transfers
- Handling invalid student IDs during transfers
- Handling invalid destination courses
- Rejecting transfers to the same course
- Transaction rollback when recording transfer history fails

**Latest verification:** All 51 tests passed.

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
- `BEGIN` - Starts a transaction.
- `COMMIT` - Saves transaction changes.
- `ROLLBACK` - Reverts uncommitted transaction changes.
- ACID properties - Describe the reliability principles of database transactions.

## Learning Outcomes

- Designing relational database tables.
- Using primary keys and foreign keys.
- Managing students and courses with Python and SQLite.
- Retrieving related records using INNER JOIN and LEFT JOIN.
- Calculating course-wise statistics.
- Identifying courses without students.
- Implementing database transactions.
- Maintaining data consistency through commit and rollback.
- Recording and retrieving student course transfer history.
- Testing database functionality using `unittest`.
