# Python–SQL Database Foundation

## Project Overview
This project demonstrates how to connect Python with an SQLite database and perform basic database operations for student management.

## Technologies Used
- Python
- SQLite
- `sqlite3` Python module

## Project Structure
- `student.py` — Defines the Student class and validates student details.
- `database.py` — Connects to SQLite, creates the students table, inserts records, retrieves data, and closes the connection.
- `main.py` — Runs the application and manages sample student records.
- `test_student.py` — Tests Student class input validation.
- `student_management.db` — SQLite database file created automatically.

## Student Table
The `students` table contains:
- `student_id` — Student ID
- `name` — Student name
- `age` — Student age
- `course` — Course name
- `marks` — Student marks

## Features
- SQLite database connection
- Automatic table creation
- Insert student records
- Retrieve all student records
- Search for a student by ID
- Validate student details
- Handle database errors and close the connection safely

## How to Run
Open a terminal in the `src` folder and run:

```bash
python "Day 10-SQL/main.py"
```

To run the validation tests:

```bash
python "Day 10-SQL/test_student.py"
```

## Sample Students
The project uses sample records for Rahul, Priya, Amit, Neha, and Rohit.

## Learning Outcomes
- Understand Python–SQLite connectivity.
- Write basic SQL `INSERT` and `SELECT` queries.
- Use parameterized SQL queries.
- Handle exceptions and manage database connections.
