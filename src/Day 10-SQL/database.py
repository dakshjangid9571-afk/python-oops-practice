

import sqlite3
import os
from student import Student
from course import Course


class Database:
    def __init__(self, db_name="student_management.db"):
        self.db_name = os.path.join(os.path.dirname(__file__), db_name)
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.execute("PRAGMA foreign_keys = ON")
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
    def create_course_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL UNIQUE
            )
        """)
        self.connection.commit()

    def create_table(self):
        try:
            cursor = self.connection.cursor()

            self.create_course_table()

            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type = 'table' AND name = 'students'
            """)
            exists = cursor.fetchone() is not None

            if not exists:
                cursor.execute("""
                    CREATE TABLE students (
                        student_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL CHECK(age > 0),
                        course_id INTEGER NOT NULL,
                        marks REAL NOT NULL
                            CHECK(marks >= 0 AND marks <= 100),
                        FOREIGN KEY(course_id)
                            REFERENCES courses(course_id)
                    )
                """)
            else:
                cursor.execute("PRAGMA table_info(students)")
                columns = [row[1] for row in cursor.fetchall()]

                if "course" in columns and "course_id" not in columns:
                    cursor.execute("""
                        SELECT DISTINCT UPPER(TRIM(course))
                        FROM students
                        WHERE course IS NOT NULL
                          AND TRIM(course) != ''
                    """)
                    old_courses = [
                        row[0] for row in cursor.fetchall()
                    ]

                    # Reuse existing course IDs where possible.
                    cursor.execute("SELECT course_id, course_name FROM courses")
                    existing = cursor.fetchall()
                    course_ids = {}

                    for course_id, course_name in existing:
                        key = course_name.strip().upper()
                        if key not in course_ids:
                            course_ids[key] = course_id

                    next_id = max(
                        [row[0] for row in existing] or [0]
                    ) + 1

                    for course_name in old_courses:
                        if course_name not in course_ids:
                            while next_id in [
                                row[0] for row in existing
                            ]:
                                next_id += 1

                            cursor.execute("""
                                INSERT INTO courses (course_id, course_name)
                                VALUES (?, ?)
                            """, (next_id, course_name))
                            course_ids[course_name] = next_id
                            existing.append((next_id, course_name))
                            next_id += 1

                    cursor.execute("""
                        CREATE TABLE students_new (
                            student_id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL CHECK(age > 0),
                            course_id INTEGER NOT NULL,
                            marks REAL NOT NULL
                                CHECK(marks >= 0 AND marks <= 100),
                            FOREIGN KEY(course_id)
                                REFERENCES courses(course_id)
                        )
                    """)

                    cursor.execute("SELECT * FROM students")
                    old_students = cursor.fetchall()

                    for student_id, name, age, course, marks in old_students:
                        if course is None or not course.strip():
                            raise ValueError(
                                f"Student {student_id} has no course."
                            )

                        course_key = course.strip().upper()
                        course_id = course_ids[course_key]

                        cursor.execute("""
                            INSERT INTO students_new
                                (student_id, name, age, course_id, marks)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            student_id, name, age, course_id, marks
                        ))

                    cursor.execute("DROP TABLE students")
                    cursor.execute(
                        "ALTER TABLE students_new RENAME TO students"
                    )

            self.connection.commit()
            print("Courses and students tables created successfully.")

        except (sqlite3.Error, ValueError) as e:
            self.connection.rollback()
            print(f"Table creation error: {e}")
            raise

    # Course operations

    def add_course(self, course):
        if not isinstance(course, Course):
            raise TypeError("Expected a Course object.")

        try:
            self.connection.execute("""
                INSERT INTO courses (course_id, course_name)
                VALUES (?, ?)
            """, (
                course.course_id,
                course.course_name.strip().upper()
            ))
            self.connection.commit()
            print("Course added successfully.")
            return True
        except sqlite3.IntegrityError as e:
            self.connection.rollback()
            print(f"Course insertion failed: {e}")
            return False

    def get_all_courses(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT course_id, course_name
            FROM courses ORDER BY course_id
        """)
        return cursor.fetchall()

    def get_course_by_id(self, course_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT course_id, course_name
            FROM courses WHERE course_id = ?
        """, (course_id,))
        return cursor.fetchone()

    def delete_course(self, course_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM courses WHERE course_id = ?",
                (course_id,)
            )
            self.connection.commit()

            if cursor.rowcount:
                print("Course deleted successfully.")
                return True

            print("Course not found.")
            return False
        except sqlite3.IntegrityError:
            self.connection.rollback()
            print("Cannot delete a course that has students enrolled.")
            return False

    # Student CRUD

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Expected a Student object.")

        if self.get_course_by_id(student.course_id) is None:
            print("Invalid course ID.")
            return False

        try:
            self.connection.execute("""
                INSERT INTO students
                    (student_id, name, age, course_id, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (
                student.student_id,
                student.name.strip(),
                student.age,
                student.course_id,
                student.marks
            ))
            self.connection.commit()
            print("Student added successfully.")
            return True
        except sqlite3.IntegrityError as e:
            self.connection.rollback()
            print(f"Student insertion failed: {e}")
            return False

    def get_all_students(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT student_id, name, age, course_id, marks
            FROM students ORDER BY student_id
        """)
        return cursor.fetchall()

    def get_student_by_id(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT student_id, name, age, course_id, marks
            FROM students WHERE student_id = ?
        """, (student_id,))
        return cursor.fetchone()

    def update_student(self, student_id, name, age, course_id, marks):
        student = Student(student_id, name, age, course_id, marks)

        if self.get_course_by_id(course_id) is None:
            print("Invalid course ID.")
            return 0

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE students
                SET name = ?, age = ?, course_id = ?, marks = ?
                WHERE student_id = ?
            """, (
                student.name.strip(), student.age,
                student.course_id, student.marks, student_id
            ))
            self.connection.commit()

            if cursor.rowcount:
                print("Student updated successfully.")
            else:
                print("Student not found.")

            return cursor.rowcount
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Student update error: {e}")
            raise

    def delete_student(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )
        self.connection.commit()

        if cursor.rowcount:
            print("Student deleted successfully.")
        else:
            print("Student not found.")

        return cursor.rowcount

    # JOIN operations

    def get_students_with_courses(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT s.student_id, s.name, s.age,
                   c.course_id, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c
                ON s.course_id = c.course_id
            ORDER BY s.student_id
        """)
        return cursor.fetchall()

    def get_course_statistics(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT c.course_id, c.course_name,
                   COUNT(s.student_id),
                   AVG(s.marks), MAX(s.marks), MIN(s.marks)
            FROM courses AS c
            LEFT JOIN students AS s
                ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            ORDER BY c.course_id
        """)
        return cursor.fetchall()

    def get_courses_without_students(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT c.course_id, c.course_name
            FROM courses AS c
            LEFT JOIN students AS s
                ON c.course_id = s.course_id
            WHERE s.student_id IS NULL
            ORDER BY c.course_id
        """)
        return cursor.fetchall()

    # Student and marks searches

    def get_students_by_course(self, course_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT student_id, name, age, course_id, marks
            FROM students WHERE course_id = ?
            ORDER BY student_id
        """, (course_id,))
        return cursor.fetchall()

    def get_students_by_marks(self, min_marks):
        if (
            not isinstance(min_marks, (int, float))
            or isinstance(min_marks, bool)
            or not 0 <= min_marks <= 100
        ):
            raise ValueError("Invalid marks.")

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT student_id, name, age, course_id, marks
            FROM students WHERE marks >= ?
            ORDER BY marks DESC
        """, (min_marks,))
        return cursor.fetchall()

    def search_students_by_name(self, keyword):
        if not isinstance(keyword, str) or not keyword.strip():
            raise ValueError("Search keyword cannot be empty.")

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT student_id, name, age, course_id, marks
            FROM students WHERE name LIKE ?
            ORDER BY student_id
        """, (f"%{keyword.strip()}%",))
        return cursor.fetchall()

    def get_students_sorted_by_marks(self, desc=True):
        if not isinstance(desc, bool):
            raise ValueError("Sort order must be True or False.")

        order = "DESC" if desc else "ASC"
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT student_id, name, age, course_id, marks
            FROM students ORDER BY marks {order}
        """)
        return cursor.fetchall()

    def get_top_students(self, limit):
        if (
            not isinstance(limit, int)
            or isinstance(limit, bool)
            or limit <= 0
        ):
            raise ValueError("Number of students must be greater than 0.")

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT student_id, name, age, course_id, marks
            FROM students ORDER BY marks DESC LIMIT ?
        """, (limit,))
        return cursor.fetchall()

    # Overall statistics

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

    def get_course_average_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT c.course_name, AVG(s.marks)
            FROM courses AS c
            LEFT JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            ORDER BY c.course_id
        """)
        return cursor.fetchall()

    def get_course_highest_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT c.course_name, MAX(s.marks)
            FROM courses AS c
            LEFT JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            ORDER BY c.course_id
        """)
        return cursor.fetchall()

    def get_course_lowest_marks(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT c.course_name, MIN(s.marks)
            FROM courses AS c
            LEFT JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            ORDER BY c.course_id
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
            SELECT c.course_name, AVG(s.marks)
            FROM courses AS c
            INNER JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            HAVING AVG(s.marks) >= ?
        """, (min_average,))
        return cursor.fetchall()

