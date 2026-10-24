
import os
import tempfile
import unittest
from unittest.mock import patch

from database import Database
from student import Student
from main import delete_student_with_confirmation


class TestStudentDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = os.path.join(self.temp_dir.name, "test.db")

        self.db = Database(db_name=db_path)
        self.db.connect()
        self.db.create_table()

        self.sample_students = [
            Student(1, "Rahul", 20, "BCA", 82),
            Student(2, "Priya", 21, "BCA", 88),
            Student(3, "Amit", 20, "BBA", 76),
            Student(4, "Neha", 22, "BCA", 91),
            Student(5, "Rohit", 21, "BBA", 69),
        ]

        for student in self.sample_students:
            self.db.add_student(student)

    def tearDown(self):
        self.db.close()
        self.temp_dir.cleanup()

    def test_valid_student(self):
        self.db.add_student(Student(6, "Karan", 20, "BCA", 85))
        result = self.db.get_student_by_id(6)
        self.assertEqual(result[1], "Karan")
        self.assertEqual(result[4], 85.0)

    def test_duplicate_student_id(self):
        self.db.add_student(Student(1, "Rahul", 20, "BCA", 82))
        self.assertEqual(len(self.db.get_all_students()), 5)

    def test_invalid_age(self):
        with self.assertRaisesRegex(ValueError, "Age must be greater than 0"):
            Student(6, "Karan", -5, "BCA", 85)

    def test_invalid_marks(self):
        with self.assertRaisesRegex(ValueError, "Marks must be between 0 and 100"):
            Student(6, "Karan", 20, "BCA", 150)

    def test_empty_name(self):
        with self.assertRaisesRegex(ValueError, "Student name cannot be empty"):
            Student(6, "", 20, "BCA", 85)

    def test_empty_course(self):
        with self.assertRaisesRegex(ValueError, "Course cannot be empty"):
            Student(6, "Karan", 20, "   ", 85)

    def test_search_existing_student(self):
        result = self.db.get_student_by_id(3)
        self.assertEqual(result, (3, "Amit", 20, "BBA", 76.0))

    def test_search_missing_student(self):
        result = self.db.get_student_by_id(999)
        self.assertIsNone(result)

    def test_update_student_marks(self):
        result = self.db.update_student(3, "Amit", 20, "BBA", 90)
        updated_student = self.db.get_student_by_id(3)

        self.assertEqual(result, 1)
        self.assertEqual(updated_student[4], 90.0)

    def test_invalid_update_does_not_change_database(self):
        original_student = self.db.get_student_by_id(3)

        with self.assertRaisesRegex(ValueError, "Marks must be between 0 and 100"):
            self.db.update_student(3, "Amit", 20, "BBA", 150)

        unchanged_student = self.db.get_student_by_id(3)
        self.assertEqual(unchanged_student, original_student)

    def test_delete_existing_student(self):
        self.db.add_student(Student(6, "Karan", 20, "BCA", 85))

        result = self.db.delete_student(6)

        self.assertEqual(result, 1)
        self.assertIsNone(self.db.get_student_by_id(6))

    def test_delete_missing_student(self):
        result = self.db.delete_student(100)
        self.assertEqual(result, 0)

    def test_cancel_deletion_preserves_student(self):
        with patch("builtins.input", return_value="no"):
            delete_student_with_confirmation(self.db, 3)

        self.assertIsNotNone(self.db.get_student_by_id(3))

    def test_filter_students_by_course(self):
        students = self.db.get_students_by_course("BCA")
        self.assertEqual(len(students), 3)
        self.assertTrue(all(student[3] == "BCA" for student in students))

    def test_filter_students_by_minimum_marks(self):
        students = self.db.get_students_by_marks(80)
        self.assertTrue(all(student[4] >= 80 for student in students))
        self.assertEqual(len(students), 3)

    def test_search_students_by_partial_name(self):
        students = self.db.search_students_by_name("ri")
        names = [student[1] for student in students]
        self.assertIn("Priya", names)
        self.assertEqual(names, ["Priya"])

    def test_sort_students_by_marks_descending(self):
        students = self.db.get_students_sorted_by_marks(desc=True)
        marks = [student[4] for student in students]
        self.assertEqual(marks, sorted(marks, reverse=True))

    def test_sort_students_by_marks_ascending(self):
        students = self.db.get_students_sorted_by_marks(desc=False)
        marks = [student[4] for student in students]
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
        with self.assertRaisesRegex(
            ValueError, "Number of students must be greater than 0"
        ):
            self.db.get_top_students(-5)


    def test_filter_students_by_course_and_marks(self):
        students = self.db.get_students_by_course_and_marks("BCA", 80)

        self.assertEqual(len(students), 3)
        self.assertTrue(
            all(student[3] == "BCA" and student[4] >= 80
                for student in students)
        )

    def test_filter_students_by_either_course(self):
        students = self.db.get_students_by_courses("BCA", "BBA")

        self.assertEqual(len(students), 5)
        self.assertTrue(
            all(student[3] in ("BCA", "BBA") for student in students)
        )


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

    def test_course_statistics(self):
        statistics = {
            row[0]: row[1:]
            for row in self.db.get_course_statistics()
        }

        self.assertEqual(statistics["BCA"][0], 3)
        self.assertAlmostEqual(statistics["BCA"][1], 87.0)
        self.assertEqual(statistics["BCA"][2:], (91.0, 82.0))

        self.assertEqual(statistics["BBA"][0], 2)
        self.assertAlmostEqual(statistics["BBA"][1], 72.5)
        self.assertEqual(statistics["BBA"][2:], (76.0, 69.0))

    def test_course_average_marks(self):
        averages = dict(self.db.get_course_average_marks())

        self.assertAlmostEqual(averages["BCA"], 87.0)
        self.assertAlmostEqual(averages["BBA"], 72.5)

    def test_course_highest_marks(self):
        highest = dict(self.db.get_course_highest_marks())

        self.assertEqual(highest["BCA"], 91.0)
        self.assertEqual(highest["BBA"], 76.0)

    def test_course_lowest_marks(self):
        lowest = dict(self.db.get_course_lowest_marks())

        self.assertEqual(lowest["BCA"], 82.0)
        self.assertEqual(lowest["BBA"], 69.0)

    def test_courses_above_average(self):
        courses = self.db.get_courses_above_average(80)

        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0][0], "BCA")
        self.assertAlmostEqual(courses[0][1], 87.0)

    def test_invalid_minimum_average(self):
        with self.assertRaisesRegex(ValueError, "Invalid average marks"):
            self.db.get_courses_above_average(150)


    def test_empty_database_analytics(self):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM students")
        self.db.connection.commit()

        self.assertEqual(self.db.get_total_students(), 0)
        self.assertIsNone(self.db.get_average_marks())
        self.assertIsNone(self.db.get_total_marks())
        self.assertIsNone(self.db.get_highest_marks())
        self.assertIsNone(self.db.get_lowest_marks())
        self.assertEqual(self.db.get_course_statistics(), [])
        self.assertEqual(self.db.get_course_average_marks(), [])
        self.assertEqual(self.db.get_course_highest_marks(), [])
        self.assertEqual(self.db.get_course_lowest_marks(), [])
        self.assertEqual(self.db.get_courses_above_average(80), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
