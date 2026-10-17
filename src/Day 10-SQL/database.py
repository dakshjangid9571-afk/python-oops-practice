
import sqlite3
import os


class Database:
    def __init__(self, db_name="student_management.db"):
        self.db_name = os.path.join(os.path.dirname(__file__), db_name)
        self.connection = None


    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            print("Database connected successfully.")
            return self.connection
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("Database connection closed.")

    def create_table(self):
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER,
                    name TEXT,
                    age INTEGER,
                    course TEXT,
                    marks REAL
                )
            """)

            self.connection.commit()
            print("Students table created successfully.")

        except sqlite3.Error as e:
            print(f"Table creation error: {e}")
            raise

    def add_student(self, student):
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                INSERT INTO students (student_id, name, age, course, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (
                student.student_id,
                student.name,
                student.age,
                student.course,
                student.marks
            ))

            self.connection.commit()
            print("Student stored successfully.")

        except sqlite3.Error as e:
            print(f"Student insertion error: {e}")
            raise

    def get_all_students(self):
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT * FROM students")

            students = cursor.fetchall()

            return students

        except sqlite3.Error as e:
            print(f"Data retrieval error: {e}")
            raise

    def get_student_by_id(self, student_id):
        try:
            cursor = self.connection.cursor()

            cursor.execute(
                "SELECT * FROM students WHERE student_id = ?",
                (student_id,)
            )

            student = cursor.fetchone()

            return student

        except sqlite3.Error as e:
            print(f"Student search error: {e}")
            raise
