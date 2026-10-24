
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
