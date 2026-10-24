
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


def display_students(students):
    if not students:
        print("No students found.")
        return

    for student in students:
        display_student(student)


def delete_student_with_confirmation(db, student_id):
    student = db.get_student_by_id(student_id)

    if student is None:
        print("Student not found.")
        return

    display_student(student)
    confirmation = input(
        "Are you sure you want to delete this student? (yes/no): "
    )

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
            print("3. Search Student by ID")
            print("4. Search Student by Course")
            print("5. Search Student by Name")
            print("6. Filter Students by Marks")
            print("7. Sort Students by Marks")
            print("8. Top N Students")
            print("9. Update Student")
            print("10. Delete Student")
            print("11. Exit")

            choice = input("Enter your choice (1-11): ").strip()

            if choice == "1":
                try:
                    student_id = int(input("Enter Student ID: "))
                    name = input("Enter Name: ")
                    age = int(input("Enter Age: "))
                    course = input("Enter Course: ")
                    marks = float(input("Enter Marks: "))

                    student = Student(
                        student_id, name, age, course, marks
                    )
                    db.add_student(student)

                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "2":
                display_students(db.get_all_students())

            elif choice == "3":
                try:
                    student_id = int(
                        input("Enter Student ID to search: ")
                    )
                    display_student(db.get_student_by_id(student_id))

                except ValueError:
                    print("Student ID must be an integer.")

            elif choice == "4":
                try:
                    course = input("Enter course to search: ")
                    students = db.get_students_by_course(course)
                    display_students(students)

                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "5":
                try:
                    keyword = input("Enter name or part of name: ")
                    students = db.search_students_by_name(keyword)
                    display_students(students)

                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "6":
                try:
                    min_marks = float(
                        input("Enter minimum marks (0-100): ")
                    )
                    students = db.get_students_by_marks(min_marks)
                    display_students(students)

                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "7":
                print("1. Sort by marks (Descending)")
                print("2. Sort by marks (Ascending)")
                sort_choice = input("Choose sorting order (1-2): ").strip()

                if sort_choice == "1":
                    students = db.get_students_sorted_by_marks(desc=True)
                    display_students(students)
                elif sort_choice == "2":
                    students = db.get_students_sorted_by_marks(desc=False)
                    display_students(students)
                else:
                    print("Invalid sorting choice.")

            elif choice == "8":
                try:
                    limit = int(input("Enter number of top students: "))
                    students = db.get_top_students(limit)
                    display_students(students)

                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "9":
                try:
                    student_id = int(
                        input("Enter Student ID to update: ")
                    )
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

                    db.update_student(
                        student_id, name, age, course, marks
                    )

                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "10":
                try:
                    student_id = int(
                        input("Enter Student ID to delete: ")
                    )
                    delete_student_with_confirmation(db, student_id)

                except ValueError:
                    print("Student ID must be an integer.")

            elif choice == "11":
                print("Exiting Student Management System.")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 11.")

    except Exception as e:
        print(f"Application error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
