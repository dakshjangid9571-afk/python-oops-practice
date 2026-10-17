
from database import Database
from student import Student


def main():
    db = Database()

    sample_students = [
        Student(1, "Rahul", 20, "BCA", 82),
        Student(2, "Priya", 21, "BCA", 88),
        Student(3, "Amit", 20, "BBA", 76),
        Student(4, "Neha", 22, "BCA", 91),
        Student(5, "Rohit", 21, "BBA", 69)
    ]

    try:
        db.connect()
        db.create_table()

        for student in sample_students:
            existing_student = db.get_student_by_id(student.student_id)

            if existing_student is None:
                db.add_student(student)
            else:
                print(f"Student ID {student.student_id} already exists.")

        print("\nAll Students:")
        for student in db.get_all_students():
            print(student)

    except Exception as e:
        print(f"Application error: {e}")

    finally:
        db.close()


if __name__ == '__main__':
    main()
