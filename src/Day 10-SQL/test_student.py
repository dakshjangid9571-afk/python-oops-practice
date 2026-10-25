
import os
import tempfile
import unittest
from unittest.mock import patch

from database import Database
from student import Student
from course import Course
from main import delete_student_with_confirmation


class TestStudentDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = os.path.join(self.temp_dir.name, "test.db")

        self.db = Database(db_name=db_path)
        self.db.connect()
        self.db.create_table()

        self.sample_courses = [
            Course(1, "BCA"),
            Course(2, "BBA"),
            Course(3, "MCA"),
            Course(4, "MBA"),
        ]

        for course in self.sample_courses:
            self.db.add_course(course)

        self.sample_students = [
            Student(1, "Rahul", 20, 1, 82),
            Student(2, "Priya", 21, 1, 88),
            Student(3, "Amit", 20, 2, 76),
            Student(4, "Neha", 22, 1, 91),
            Student(5, "Rohit", 21, 2, 69),
        ]

        for student in self.sample_students:
            self.db.add_student(student)

    def tearDown(self):
        self.db.close()
        self.temp_dir.cleanup()

    # Student validation

    def test_valid_student(self):
        student = Student(6, "Karan", 20, 1, 85)
        self.assertEqual(student.name, "Karan")
        self.assertEqual(student.course_id, 1)

    def test_invalid_student_id(self):
        with self.assertRaisesRegex(ValueError, "Student ID must be an integer"):
            Student("6", "Karan", 20, 1, 85)

    def test_invalid_age(self):
        with self.assertRaisesRegex(ValueError, "Age must be greater than 0"):
            Student(6, "Karan", -5, 1, 85)

    def test_invalid_marks(self):
        with self.assertRaisesRegex(ValueError, "Marks must be between 0 and 100"):
            Student(6, "Karan", 20, 1, 150)

    def test_empty_name(self):
        with self.assertRaisesRegex(ValueError, "Student name cannot be empty"):
            Student(6, "", 20, 1, 85)

    def test_invalid_course_id_type(self):
        with self.assertRaisesRegex(ValueError, "Course ID must be an integer"):
            Student(6, "Karan", 20, "BCA", 85)

    # Course validation and operations

    def test_course_validation(self):
        self.assertTrue(Course(5, "MTech").validate())

    def test_invalid_course_id(self):
        with self.assertRaisesRegex(ValueError, "Course ID must be an integer"):
            Course("5", "MTech")

    def test_empty_course_name(self):
        with self.assertRaisesRegex(ValueError, "Course name cannot be empty"):
            Course(5, "   ")

    def test_all_courses(self):
        courses = self.db.get_all_courses()
        self.assertEqual(
            courses,
            [(1, "BCA"), (2, "BBA"), (3, "MCA"), (4, "MBA")]
        )

    def test_get_course_by_id(self):
        self.assertEqual(self.db.get_course_by_id(1), (1, "BCA"))
        self.assertIsNone(self.db.get_course_by_id(99))

    def test_duplicate_course_id(self):
        result = self.db.add_course(Course(1, "Another Course"))
        self.assertFalse(result)
        self.assertEqual(len(self.db.get_all_courses()), 4)

    def test_delete_course_without_students(self):
        self.assertTrue(self.db.delete_course(3))
        self.assertIsNone(self.db.get_course_by_id(3))

    def test_cannot_delete_course_with_students(self):
        self.assertFalse(self.db.delete_course(1))
        self.assertIsNotNone(self.db.get_course_by_id(1))

    # Student CRUD

    def test_add_student(self):
        self.db.add_student(Student(6, "Karan", 20, 1, 85))
        result = self.db.get_student_by_id(6)
        self.assertEqual(result, (6, "Karan", 20, 1, 85.0))

    def test_duplicate_student_id(self):
        self.db.add_student(Student(1, "Rahul", 20, 1, 82))
        self.assertEqual(len(self.db.get_all_students()), 5)

    def test_invalid_course_does_not_insert_student(self):
        with patch("builtins.print") as mock_print:
            self.db.add_student(Student(99, "Test Student", 20, 99, 80))
        self.assertIsNone(self.db.get_student_by_id(99))
        self.assertTrue(
            any("Invalid course ID." in str(call) for call in mock_print.call_args_list)
        )

    def test_search_existing_student(self):
        self.assertEqual(
            self.db.get_student_by_id(3),
            (3, "Amit", 20, 2, 76.0)
        )

    def test_search_missing_student(self):
        self.assertIsNone(self.db.get_student_by_id(999))

    def test_update_student_marks(self):
        result = self.db.update_student(3, "Amit", 20, 2, 90)
        self.assertEqual(result, 1)
        self.assertEqual(self.db.get_student_by_id(3)[4], 90.0)

    def test_invalid_update_does_not_change_database(self):
        original = self.db.get_student_by_id(3)
        with self.assertRaisesRegex(ValueError, "Marks must be between 0 and 100"):
            self.db.update_student(3, "Amit", 20, 2, 150)
        self.assertEqual(self.db.get_student_by_id(3), original)

    def test_delete_existing_student(self):
        self.db.add_student(Student(6, "Karan", 20, 1, 85))
        self.assertEqual(self.db.delete_student(6), 1)
        self.assertIsNone(self.db.get_student_by_id(6))

    def test_delete_missing_student(self):
        self.assertEqual(self.db.delete_student(100), 0)

    def test_cancel_deletion_preserves_student(self):
        with patch("builtins.input", return_value="no"):
            delete_student_with_confirmation(self.db, 3)
        self.assertIsNotNone(self.db.get_student_by_id(3))

    # Student search and sorting

    def test_filter_students_by_course(self):
        students = self.db.get_students_by_course(1)
        self.assertEqual(len(students), 3)
        self.assertTrue(all(student[3] == 1 for student in students))

    def test_filter_students_by_minimum_marks(self):
        students = self.db.get_students_by_marks(80)
        self.assertEqual(len(students), 3)
        self.assertTrue(all(student[4] >= 80 for student in students))

    def test_search_students_by_partial_name(self):
        students = self.db.search_students_by_name("ri")
        self.assertEqual([student[1] for student in students], ["Priya"])

    def test_sort_students_by_marks_descending(self):
        marks = [s[4] for s in self.db.get_students_sorted_by_marks(True)]
        self.assertEqual(marks, sorted(marks, reverse=True))

    def test_sort_students_by_marks_ascending(self):
        marks = [s[4] for s in self.db.get_students_sorted_by_marks(False)]
        self.assertEqual(marks, sorted(marks))

    def test_get_top_three_students(self):
        students = self.db.get_top_students(3)
        self.assertEqual(len(students), 3)
        marks = [student[4] for student in students]
        self.assertEqual(marks, sorted(marks, reverse=True))

    def test_invalid_minimum_marks(self):
        with self.assertRaisesRegex(ValueError, "Invalid marks"):
            self.db.get_students_by_marks(150)

    def test_invalid_top_n(self):
        with self.assertRaisesRegex(ValueError, "Number of students must be greater than 0"):
            self.db.get_top_students(-5)

    # Overall statistics

    def test_total_students(self):
        self.assertEqual(self.db.get_total_students(), 5)

    def test_average_marks(self):
        self.assertAlmostEqual(self.db.get_average_marks(), 81.2)

    def test_total_marks(self):
        self.assertEqual(self.db.get_total_marks(), 406)

    def test_highest_marks(self):
        self.assertEqual(self.db.get_highest_marks(), 91)

    def test_lowest_marks(self):
        self.assertEqual(self.db.get_lowest_marks(), 69)

    # JOIN and course statistics

    def test_inner_join_students_with_courses(self):
        rows = self.db.get_students_with_courses()
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0], (1, "Rahul", 20, 1, "BCA", 82.0))
        self.assertEqual(rows[2][4], "BBA")

    def test_course_statistics(self):
        statistics = {
            row[1]: row[2:] for row in self.db.get_course_statistics()
        }

        self.assertEqual(statistics["BCA"][0], 3)
        self.assertAlmostEqual(statistics["BCA"][1], 87.0)
        self.assertEqual(statistics["BCA"][2:], (91.0, 82.0))

        self.assertEqual(statistics["BBA"][0], 2)
        self.assertAlmostEqual(statistics["BBA"][1], 72.5)
        self.assertEqual(statistics["BBA"][2:], (76.0, 69.0))

        self.assertEqual(statistics["MCA"][0], 0)
        self.assertIsNone(statistics["MCA"][1])
        self.assertEqual(statistics["MBA"][0], 0)

    def test_courses_without_students(self):
        self.assertEqual(
            self.db.get_courses_without_students(),
            [(3, "MCA"), (4, "MBA")]
        )

    def test_course_average_marks(self):
        averages = dict(self.db.get_course_average_marks())
        self.assertAlmostEqual(averages["BCA"], 87.0)
        self.assertAlmostEqual(averages["BBA"], 72.5)
        self.assertIsNone(averages["MCA"])
        self.assertIsNone(averages["MBA"])

    def test_course_highest_marks(self):
        highest = dict(self.db.get_course_highest_marks())
        self.assertEqual(highest["BCA"], 91.0)
        self.assertEqual(highest["BBA"], 76.0)
        self.assertIsNone(highest["MCA"])

    def test_course_lowest_marks(self):
        lowest = dict(self.db.get_course_lowest_marks())
        self.assertEqual(lowest["BCA"], 82.0)
        self.assertEqual(lowest["BBA"], 69.0)
        self.assertIsNone(lowest["MBA"])

    def test_courses_above_average(self):
        courses = self.db.get_courses_above_average(80)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0][0], "BCA")
        self.assertAlmostEqual(courses[0][1], 87.0)

    def test_invalid_minimum_average(self):
        with self.assertRaisesRegex(ValueError, "Invalid average marks"):
            self.db.get_courses_above_average(150)

    def test_empty_database_analytics(self):
        self.db.connection.execute("DELETE FROM students")
        self.db.connection.commit()

        self.assertEqual(self.db.get_total_students(), 0)
        self.assertIsNone(self.db.get_average_marks())
        self.assertIsNone(self.db.get_total_marks())
        self.assertIsNone(self.db.get_highest_marks())
        self.assertIsNone(self.db.get_lowest_marks())

        stats = self.db.get_course_statistics()
        self.assertEqual(len(stats), 4)
        self.assertTrue(all(row[2] == 0 for row in stats))
        self.assertEqual(
            self.db.get_courses_without_students(),
            [(1, "BCA"), (2, "BBA"), (3, "MCA"), (4, "MBA")]
        )

class TestStudentCourseTransactions(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = os.path.join(self.temp_dir.name, "transaction_test.db")

        self.db = Database(db_name=db_path)
        self.db.connect()
        self.db.create_table()
        self.db.create_history_table()

        self.db.add_course(Course(1, "BCA"))
        self.db.add_course(Course(2, "MCA"))
        self.db.add_student(Student(1, "Rahul", 20, 1, 82))

    def tearDown(self):
        self.db.close()
        self.temp_dir.cleanup()

    def test_successful_course_transfer(self):
        result = self.db.transfer_student_course(1, 2)

        student = self.db.get_student_by_id(1)
        history = self.db.get_student_course_history(1)

        self.assertTrue(result)
        self.assertEqual(student[3], 2)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][2], 1)
        self.assertEqual(history[0][4], 2)

    def test_invalid_student_rolls_back(self):
        with self.assertRaisesRegex(ValueError, "Student not found"):
            self.db.transfer_student_course(999, 2)

        self.assertEqual(self.db.get_student_by_id(1)[3], 1)
        self.assertEqual(self.db.get_student_course_history(1), [])

    def test_invalid_course_rolls_back(self):
        with self.assertRaisesRegex(ValueError, "New course not found"):
            self.db.transfer_student_course(1, 99)

        self.assertEqual(self.db.get_student_by_id(1)[3], 1)
        self.assertEqual(self.db.get_student_course_history(1), [])

    def test_same_course_is_rejected(self):
        with self.assertRaisesRegex(
            ValueError, "already enrolled in this course"
        ):
            self.db.transfer_student_course(1, 1)

        self.assertEqual(self.db.get_student_by_id(1)[3], 1)
        self.assertEqual(self.db.get_student_course_history(1), [])

    def test_history_insert_failure_rolls_back_transfer(self):
        self.db.connection.execute("""
            CREATE TRIGGER fail_history_insert
            BEFORE INSERT ON student_course_history
            BEGIN
                SELECT RAISE(ABORT, 'Simulated history insert failure');
            END
        """)
        self.db.connection.commit()

        with self.assertRaisesRegex(
            Exception, "Simulated history insert failure"
        ):
            self.db.transfer_student_course(1, 2)

        student = self.db.get_student_by_id(1)
        history = self.db.get_student_course_history(1)

        self.assertEqual(student[3], 1)
        self.assertEqual(history, [])


if __name__ == "__main__":
    unittest.main()
