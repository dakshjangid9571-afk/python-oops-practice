
import os
import tempfile
import unittest

from database import Database
from student import Student


class TestStudentDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = os.path.join(self.temp_dir.name, "test.db")

        self.db = Database(db_name=db_path)
        self.db.connect()
        self.db.create_table()
        self.db.add_student(Student(1, "Rahul", 20, "BCA", 82))

    def tearDown(self):
        self.db.close()
        self.temp_dir.cleanup()

    def test_valid_student(self):
        self.db.add_student(Student(6, "Karan", 20, "BCA", 85))
        result = self.db.get_student_by_id(6)
        self.assertEqual(result[1], "Karan")

    def test_duplicate_student_id(self):
        self.db.add_student(Student(1, "Rahul", 20, "BCA", 82))
        self.assertEqual(len(self.db.get_all_students()), 1)

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
        result = self.db.get_student_by_id(1)
        self.assertEqual(result, (1, "Rahul", 20, "BCA", 82.0))

    def test_search_missing_student(self):
        result = self.db.get_student_by_id(999)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
