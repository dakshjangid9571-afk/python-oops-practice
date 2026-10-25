import psycopg

from config import DB_CONFIG
from student import Student

class Database:
    def __init__(self, db_name=None):
        self.db_config = DB_CONFIG.copy()
        if db_name is not None:
            self.db_config["dbname"] = db_name
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg.connect(**self.db_config)
            print("PostgreSQL connection successful.")
            return self.connection
        except psycopg.Error as error:
            self.connection = None
            raise ConnectionError(
                "Could not connect to PostgreSQL. "
                "Check the server and .env configuration."
            ) from error

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def create_tables(self):
        if self.connection is None or self.connection.closed:
            raise ConnectionError("Connect to PostgreSQL first.")

        statements = [
            """
            CREATE TABLE IF NOT EXISTS courses (
                course_id SERIAL PRIMARY KEY,
                course_name VARCHAR(100) NOT NULL UNIQUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INTEGER NOT NULL CHECK (age > 0),
                course_id INTEGER NOT NULL
                    REFERENCES courses(course_id),
                marks NUMERIC(5,2) NOT NULL
                    CHECK (marks >= 0 AND marks <= 100)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS student_course_history (
                history_id SERIAL PRIMARY KEY,
                student_id INTEGER NOT NULL
                    REFERENCES students(student_id),
                old_course_id INTEGER NOT NULL
                    REFERENCES courses(course_id),
                new_course_id INTEGER NOT NULL
                    REFERENCES courses(course_id),
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
        ]

        try:
            with self.connection.cursor() as cursor:
                for statement in statements:
                    cursor.execute(statement)
            self.connection.commit()
            print("PostgreSQL tables created successfully.")
        except psycopg.Error:
            self.connection.rollback()
            raise

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.rowcount

    def fetch_one(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def fetch_all(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def commit(self):
        if self.connection is not None:
            self.connection.commit()

    def rollback(self):
        if self.connection is not None:
            self.connection.rollback()

    def add_course(self, course):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO courses (course_id, course_name)
                    VALUES (%s, %s)
                    """,
                    (course.course_id, course.course_name),
                )
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            raise

    def get_all_courses(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT course_id, course_name
                FROM courses
                ORDER BY course_id
                """
            )
            return cursor.fetchall()

    def get_course_by_id(self, course_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT course_id, course_name
                FROM courses
                WHERE course_id = %s
                """,
                (course_id,),
            )
            return cursor.fetchone()

    def delete_course(self, course_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM courses WHERE course_id = %s",
                    (course_id,),
                )
                deleted = cursor.rowcount > 0
            self.connection.commit()
            return deleted
        except Exception:
            self.connection.rollback()
            raise
    def add_student(self, student):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO students
                        (student_id, name, age, course_id, marks)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        student.student_id,
                        student.name.strip(),
                        student.age,
                        student.course_id,
                        student.marks,
                    ),
                )
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            raise

    def get_all_students(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT student_id, name, age, course_id, marks
                FROM students
                ORDER BY student_id
                """
            )
            return cursor.fetchall()

    def get_student_by_id(self, student_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT student_id, name, age, course_id, marks
                FROM students
                WHERE student_id = %s
                """,
                (student_id,),
            )
            return cursor.fetchone()

    
    def update_student(
        self, student_id, name=None, age=None, course_id=None, marks=None
    ):
        try:
            if isinstance(student_id, Student):
                student = student_id
                student_id = student.student_id
                name = student.name
                age = student.age
                course_id = student.course_id
                marks = student.marks

            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE students
                    SET name = %s, age = %s, course_id = %s, marks = %s
                    WHERE student_id = %s
                    """,
                    (name.strip(), age, course_id, marks, student_id),
                )
                updated = cursor.rowcount > 0

            self.connection.commit()
            return updated
        except Exception:
            self.connection.rollback()
            raise


    def delete_student(self, student_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM students WHERE student_id = %s",
                    (student_id,),
                )
                deleted = cursor.rowcount > 0
            self.connection.commit()
            return deleted
        except Exception:
            self.connection.rollback()
            raise

    def get_students_with_courses(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT s.student_id, s.name, c.course_name, s.marks
                FROM students AS s
                JOIN courses AS c ON s.course_id = c.course_id
                ORDER BY s.student_id
                """
            )
            return cursor.fetchall()

    def transfer_student_course(self, student_id, new_course_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT course_id
                    FROM students
                    WHERE student_id = %s
                    FOR UPDATE
                    """,
                    (student_id,),
                )
                student = cursor.fetchone()

                if student is None:
                    raise ValueError(
                        f"Student ID {student_id} does not exist."
                    )

                old_course_id = student[0]

                if old_course_id == new_course_id:
                    raise ValueError(
                        "Student is already enrolled in this course."
                    )

                cursor.execute(
                    "SELECT course_id FROM courses WHERE course_id = %s",
                    (new_course_id,),
                )
                if cursor.fetchone() is None:
                    raise ValueError(
                        f"Course ID {new_course_id} does not exist."
                    )

                cursor.execute(
                    """
                    UPDATE students
                    SET course_id = %s
                    WHERE student_id = %s
                    """,
                    (new_course_id, student_id),
                )

                cursor.execute(
                    """
                    INSERT INTO student_course_history
                        (student_id, old_course_id, new_course_id)
                    VALUES (%s, %s, %s)
                    """,
                    (student_id, old_course_id, new_course_id),
                )

            self.connection.commit()
            return True

        except Exception:
            self.connection.rollback()
            raise



    def get_course_statistics(self):
        with self.connection.cursor() as cursor:
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
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.course_id, c.course_name
                FROM courses AS c
                LEFT JOIN students AS s
                    ON c.course_id = s.course_id
                WHERE s.student_id IS NULL
                ORDER BY c.course_id
            """)
            return cursor.fetchall()

    def get_students_by_course(self, course_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT student_id, name, age, course_id, marks
                FROM students
                WHERE course_id = %s
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

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT student_id, name, age, course_id, marks
                FROM students
                WHERE marks >= %s
                ORDER BY marks DESC
            """, (min_marks,))
            return cursor.fetchall()

    def search_students_by_name(self, keyword):
        if not isinstance(keyword, str) or not keyword.strip():
            raise ValueError("Search keyword cannot be empty.")

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT student_id, name, age, course_id, marks
                FROM students
                WHERE name ILIKE %s
                ORDER BY student_id
            """, (f"%{keyword.strip()}%",))
            return cursor.fetchall()

    def get_students_sorted_by_marks(self, desc=True):
        if not isinstance(desc, bool):
            raise ValueError("Sort order must be True or False.")

        order = "DESC" if desc else "ASC"

        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT student_id, name, age, course_id, marks
                FROM students
                ORDER BY marks {order}
            """)
            return cursor.fetchall()

    def get_top_students(self, limit):
        if (
            not isinstance(limit, int)
            or isinstance(limit, bool)
            or limit <= 0
        ):
            raise ValueError(
                "Number of students must be greater than 0."
            )

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT student_id, name, age, course_id, marks
                FROM students
                ORDER BY marks DESC
                LIMIT %s
            """, (limit,))
            return cursor.fetchall()

    def get_total_students(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM students")
            return cursor.fetchone()[0]

    def get_average_marks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT AVG(marks) FROM students")
            return cursor.fetchone()[0]

    def get_total_marks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT SUM(marks) FROM students")
            return cursor.fetchone()[0]

    def get_highest_marks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT MAX(marks) FROM students")
            return cursor.fetchone()[0]

    def get_lowest_marks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT MIN(marks) FROM students")
            return cursor.fetchone()[0]

    def get_course_average_marks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.course_name, AVG(s.marks)
                FROM courses AS c
                LEFT JOIN students AS s
                    ON c.course_id = s.course_id
                GROUP BY c.course_id, c.course_name
                ORDER BY c.course_id
            """)
            return cursor.fetchall()

    def get_course_highest_marks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.course_name, MAX(s.marks)
                FROM courses AS c
                LEFT JOIN students AS s
                    ON c.course_id = s.course_id
                GROUP BY c.course_id, c.course_name
                ORDER BY c.course_id
            """)
            return cursor.fetchall()

    def get_course_lowest_marks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.course_name, MIN(s.marks)
                FROM courses AS c
                LEFT JOIN students AS s
                    ON c.course_id = s.course_id
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

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.course_name, AVG(s.marks)
                FROM courses AS c
                INNER JOIN students AS s
                    ON c.course_id = s.course_id
                GROUP BY c.course_id, c.course_name
                HAVING AVG(s.marks) >= %s
                ORDER BY c.course_id
            """, (min_average,))
            return cursor.fetchall()

    def begin_transaction(self):
        if self.connection is None or self.connection.closed:
            raise ConnectionError("Connect to PostgreSQL first.")

        if not self.connection.autocommit and not self.connection.info.transaction_status == 0:
            raise RuntimeError("A transaction is already active.")

        self.connection.execute("BEGIN")

    def get_course_history(self, student_id=None):
        if student_id is not None:
            return self.get_student_course_history(student_id)

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    h.history_id,
                    h.student_id,
                    s.name,
                    h.old_course_id,
                    old_c.course_name,
                    h.new_course_id,
                    new_c.course_name,
                    h.changed_at
                FROM student_course_history AS h
                JOIN students AS s
                    ON h.student_id = s.student_id
                JOIN courses AS old_c
                    ON h.old_course_id = old_c.course_id
                JOIN courses AS new_c
                    ON h.new_course_id = new_c.course_id
                ORDER BY h.history_id
            """)
            return cursor.fetchall()
    def get_student_course_history(self, student_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    h.history_id,
                    h.student_id,
                    h.old_course_id,
                    old_c.course_name,
                    h.new_course_id,
                    new_c.course_name,
                    h.changed_at
                FROM student_course_history AS h
                JOIN courses AS old_c
                    ON h.old_course_id = old_c.course_id
                JOIN courses AS new_c
                    ON h.new_course_id = new_c.course_id
                WHERE h.student_id = %s
                ORDER BY h.history_id
            """, (student_id,))
            return cursor.fetchall()
