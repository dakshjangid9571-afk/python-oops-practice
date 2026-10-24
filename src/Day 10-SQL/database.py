
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
                SELECT name
                FROM sqlite_master
                WHERE type = 'table' AND name = 'students'
            """)
            table_exists = cursor.fetchone() is not None

            if not table_exists:
                cursor.execute("""
                    CREATE TABLE students (
                        student_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL CHECK(age > 0),
                        course TEXT NOT NULL,
                        marks REAL NOT NULL
                            CHECK(marks >= 0 AND marks <= 100)
                    )
                """)
            else:
                cursor.execute("PRAGMA table_info(students)")
                columns = cursor.fetchall()
                column_info = {column[1]: column for column in columns}

                constraints_exist = (
                    column_info.get("student_id", (None,) * 6)[5] == 1
                    and all(
                        column_info.get(name, (None,) * 4)[3] == 1
                        for name in ("name", "age", "course", "marks")
                    )
                )

                if not constraints_exist:
                    cursor.execute("PRAGMA foreign_keys = OFF")
                    cursor.execute("BEGIN")

                    cursor.execute("""
                        CREATE TABLE students_new (
                            student_id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL CHECK(age > 0),
                            course TEXT NOT NULL,
                            marks REAL NOT NULL
                                CHECK(marks >= 0 AND marks <= 100)
                        )
                    """)

                    cursor.execute("""
                        INSERT INTO students_new
                            (student_id, name, age, course, marks)
                        SELECT student_id, name, age, course, marks
                        FROM students
                    """)

                    cursor.execute("DROP TABLE students")
                    cursor.execute(
                        "ALTER TABLE students_new RENAME TO students"
                    )

            self.connection.commit()
            print("Students table created successfully.")

        except sqlite3.Error as e:
            self.connection.rollback()
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
            print("Student added successfully.")

        except sqlite3.IntegrityError as e:
            self.connection.rollback()

            if "UNIQUE constraint failed" in str(e) or \
                    "PRIMARY KEY" in str(e):
                print("Student ID already exists.")
            else:
                print(f"Student data violates database constraints: {e}")

        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Student insertion error: {e}")
            raise

    def get_all_students(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students")
            return cursor.fetchall()
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
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Student search error: {e}")
            raise
