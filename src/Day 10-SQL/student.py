
class Student:
    def __init__(self, student_id, name, age, course, marks):
        if not isinstance(student_id, int):
            raise ValueError("Student ID must be an integer.")

        if not name.strip():
            raise ValueError("Student name cannot be empty.")

        if age <= 0:
            raise ValueError("Age must be greater than 0.")

        if not course.strip():
            raise ValueError("Course cannot be empty.")

        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")

        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks
