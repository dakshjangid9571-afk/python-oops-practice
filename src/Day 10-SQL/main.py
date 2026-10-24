
from database import Database
from student import Student


def display_student(student):
    if student is None:
        print("Student not found.")
        return

    print(
        f"ID: {student[0]}, Name: {student[1]}, "
        f"Age: {student[2]}, Course: {student[3]}, "
        f"Marks: {student[4]}"
    )


def delete_student_with_confirmation(db, student_id):
    student = db.get_student_by_id(student_id)

    if student is None:
        print("Student not found.")
        return

    display_student(student)
    confirmation = input("Are you sure you want to delete this student? (yes/no): ")

    if confirmation.strip().lower() in ("yes", "y"):
        db.delete_student(student_id)
    else:
        print("Deletion cancelled.")


def main():
    db = Database()

    try:
        db.connect()
        db.create_table()

        while True:
            print("\n===== Student Management System =====")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                try:
                    student_id = int(input("Enter Student ID: "))
                    name = input("Enter Name: ")
                    age = int(input("Enter Age: "))
                    course = input("Enter Course: ")
                    marks = float(input("Enter Marks: "))

                    student = Student(student_id, name, age, course, marks)
                    db.add_student(student)

                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "2":
                students = db.get_all_students()

                if not students:
                    print("No students found.")
                else:
                    print("\nAll Students:")
                    for student in students:
                        display_student(student)

            elif choice == "3":
                try:
                    student_id = int(input("Enter Student ID to search: "))
                    display_student(db.get_student_by_id(student_id))
                except ValueError:
                    print("Student ID must be an integer.")

            elif choice == "4":
                try:
                    student_id = int(input("Enter Student ID to update: "))
                    existing_student = db.get_student_by_id(student_id)

                    if existing_student is None:
                        print("Student not found.")
                        continue

                    print("Current student details:")
                    display_student(existing_student)

                    name = input("Enter new Name: ")
                    age = int(input("Enter new Age: "))
                    course = input("Enter new Course: ")
                    marks = float(input("Enter new Marks: "))

                    db.update_student(student_id, name, age, course, marks)

                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "5":
                try:
                    student_id = int(input("Enter Student ID to delete: "))
                    delete_student_with_confirmation(db, student_id)
                except ValueError:
                    print("Student ID must be an integer.")

            elif choice == "6":
                print("Exiting Student Management System.")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 6.")

    except Exception as e:
        print(f"Application error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
