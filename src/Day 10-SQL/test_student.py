
from student import Student

try:
    student = Student(6, "Karan", 20, "   ", 80)
    print("Student created successfully.")

except ValueError as e:
    print(f"Validation Error: {e}")
