
import sqlite3
import os
from student import Student

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

        
    def update_student(self, student_id, name, age, course, marks):
        try:
            student = Student(student_id, name, age, course, marks)

            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE students
                SET name = ?, age = ?, course = ?, marks = ?
                WHERE student_id = ?
            """, (
                student.name,
                student.age,
                student.course,
                student.marks,
                student_id
            ))

            self.connection.commit()

            if cursor.rowcount == 1:
                print("Student updated successfully.")
            else:
                print("Student not found.")

            return cursor.rowcount

        except sqlite3.IntegrityError as e:
            self.connection.rollback()
            print(f"Student update failed: {e}")
            return 0

        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Student update error: {e}")
            raise

    def delete_student(self, student_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM students WHERE student_id = ?",
                (student_id,)
            )

            self.connection.commit()

            if cursor.rowcount == 1:
                print("Student deleted successfully.")
            else:
                print("Student not found.")

            return cursor.rowcount

        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Student deletion error: {e}")
            raise
    def get_students_by_course(self, course):
        if not isinstance(course, str) or not course.strip():
            raise ValueError("Course cannot be empty.")

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM students WHERE course = ?",
                (course.strip(),)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Course filtering error: {e}")
            raise


    def get_total_students(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        return cursor.fetchone()[0]

    def get_average_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT AVG(marks) FROM students")
        return cursor.fetchone()[0]

    def get_total_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(marks) FROM students")
        return cursor.fetchone()[0]

    def get_highest_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT MAX(marks) FROM students")
        return cursor.fetchone()[0]

    def get_lowest_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT MIN(marks) FROM students")
        return cursor.fetchone()[0]

    def get_course_statistics(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT course, COUNT(*) AS total_students,
                   AVG(marks) AS average_marks,
                   MAX(marks) AS highest_marks,
                   MIN(marks) AS lowest_marks
            FROM students
            GROUP BY course
        """)
        return cursor.fetchall()

    def get_course_average_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT course, AVG(marks) AS average_marks
            FROM students
            GROUP BY course
        """)
        return cursor.fetchall()

    def get_course_highest_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT course, MAX(marks) AS highest_marks
            FROM students
            GROUP BY course
        """)
        return cursor.fetchall()

    def get_course_lowest_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT course, MIN(marks) AS lowest_marks
            FROM students
            GROUP BY course
        """)
        return cursor.fetchall()

    def get_courses_above_average(self, min_average):
        if (
            not isinstance(min_average, (int, float))
            or isinstance(min_average, bool)
            or not 0 <= min_average <= 100
        ):
            raise ValueError("Invalid average marks.")

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT course, AVG(marks) AS average_marks
            FROM students
            GROUP BY course
            HAVING AVG(marks) >= ?
        """, (min_average,))
        return cursor.fetchall()

    def get_students_by_marks(self, min_marks):
        if (
            not isinstance(min_marks, (int, float))
            or isinstance(min_marks, bool)
            or not 0 <= min_marks <= 100
        ):
            raise ValueError("Invalid marks.")

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM students WHERE marks >= ?",
                (min_marks,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Marks filtering error: {e}")
            raise

    def search_students_by_name(self, keyword):
        if not isinstance(keyword, str) or not keyword.strip():
            raise ValueError("Search keyword cannot be empty.")

        try:
            keyword = f"%{keyword.strip()}%"
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM students WHERE name LIKE ?",
                (keyword,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Name search error: {e}")
            raise

    def get_students_sorted_by_marks(self, desc=True):
        if not isinstance(desc, bool):
            raise ValueError("Sort order must be True or False.")

        order = "DESC" if desc else "ASC"

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"SELECT * FROM students ORDER BY marks {order}"
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Student sorting error: {e}")
            raise

    def get_top_students(self, limit):
        if (
            not isinstance(limit, int)
            or isinstance(limit, bool)
            or limit <= 0
        ):
            raise ValueError("Number of students must be greater than 0.")

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM students ORDER BY marks DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Top students retrieval error: {e}")
            raise


        
    def get_students_by_course_and_marks(self, course, min_marks):
        if not isinstance(course, str) or not course.strip():
            raise ValueError("Course cannot be empty.")

        if (
            not isinstance(min_marks, (int, float))
            or isinstance(min_marks, bool)
            or not 0 <= min_marks <= 100
        ):
            raise ValueError("Invalid marks.")

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT * FROM students
                WHERE course = ? AND marks >= ?
                """,
                (course.strip(), min_marks)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Course and marks filtering error: {e}")
            raise

    def get_students_by_courses(self, course1, course2):
        if (
            not isinstance(course1, str) or not course1.strip()
            or not isinstance(course2, str) or not course2.strip()
        ):
            raise ValueError("Course cannot be empty.")

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT * FROM students
                WHERE course = ? OR course = ?
                """,
                (course1.strip(), course2.strip())
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Multiple-course filtering error: {e}")
            raise
