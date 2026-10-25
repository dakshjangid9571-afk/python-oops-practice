class Student:
    def __init__(self, student_id, name, age, course_id, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course_id = course_id
        self.marks = marks

        self.validate()

    def validate(self):
        if not isinstance(self.student_id, int) or isinstance(self.student_id, bool):
            raise ValueError("Student ID must be an integer.")

        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Student name cannot be empty.")

        if not isinstance(self.age, int) or isinstance(self.age, bool) or self.age <= 0:
            raise ValueError("Age must be greater than 0.")

        if not isinstance(self.course_id, int) or isinstance(self.course_id, bool):
            raise ValueError("Course ID must be an integer.")

        if (
            not isinstance(self.marks, (int, float))
            or isinstance(self.marks, bool)
            or not 0 <= self.marks <= 100
        ):
            raise ValueError("Marks must be between 0 and 100.")