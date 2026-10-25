# Task 8: PostgreSQL Database Integration

## Overview
This project upgrades the Python Student Management System from SQLite to PostgreSQL using Python and psycopg.

## Features
- Student and course CRUD operations
- JOIN queries and student performance analytics
- Course transfers with transaction history
- Transaction commit and rollback
- Environment-based database configuration

## Database Schema
- `courses`: course ID and course name
- `students`: student details, course reference, and marks
- `student_course_history`: course transfer history

## Setup
1. Install PostgreSQL and create a database named `student_management`.
2. Install dependencies:
   `python -m pip install -r "src\Day 10-SQL\requirements.txt"`
3. Copy `.env.example` to `.env` in `src\Day 10-SQL`.
4. Update `.env` with your local PostgreSQL credentials. Never commit `.env`.
5. Run from the project root:
   `python "src\Day 10-SQL\main.py"`

## Tests
Run:
`python -m unittest discover -s "src\Day 10-SQL" -p "test_postgresql.py" -v`

## Security
Commit `.env.example` only. Never commit passwords or local database files.
