import unittest

from database import Database
from course import Course
from student import Student


class TestPostgreSQLIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Database()
        cls.db.connect()
        cls.db.create_tables()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_connection_and_tables(self):
        self.assertIsNotNone(self.db.fetch_one("SELECT 1"))

    def test_required_courses_exist(self):
        courses = self.db.get_all_courses()
        names = {row[1] for row in courses}
        self.assertTrue({"BCA", "BBA", "MCA", "MBA"}.issubset(names))

    def test_parameterized_fetch_helpers(self):
        row = self.db.fetch_one("SELECT %s::INTEGER", (123,))
        self.assertEqual(row[0], 123)

    def test_history_method_returns_list(self):
        self.assertIsInstance(self.db.get_course_history(), list)


if __name__ == "__main__":
    unittest.main(verbosity=2)
