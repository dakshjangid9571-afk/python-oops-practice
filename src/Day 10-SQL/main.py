
from database import Database
from student import Student
from course import Course


def display_courses(courses):
    if not courses:
        print("No courses found.")
        return

    print(f"{'Course ID':<12}{'Course Name':<15}")
    print("-" * 27)
    for course_id, course_name in courses:
        print(f"{course_id:<12}{course_name:<15}")


def display_student(student):
    if student is None:
        print("Student not found.")
        return

    print(
        f"ID: {student[0]}, Name: {student[1]}, "
        f"Age: {student[2]}, Course ID: {student[3]}, "
        f"Marks: {student[4]}"
    )


def display_students(students):
    if not students:
        print("No students found.")
        return

    for student in students:
        display_student(student)


def display_students_with_courses(students):
    if not students:
        print("No students found.")
        return

    print(
        f"{'ID':<8}{'Name':<15}{'Age':<8}"
        f"{'Course ID':<12}{'Course Name':<15}{'Marks':<8}"
    )
    print("-" * 66)

    for student_id, name, age, course_id, course_name, marks in students:
        print(
            f"{student_id:<8}{name:<15}{age:<8}"
            f"{course_id:<12}{course_name:<15}{marks:<8.2f}"
        )


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


def display_student_statistics(db):
    total = db.get_total_students()

    if total == 0:
        print("No student records available.")
        return

    print("\n===== Student Statistics =====")
    print(f"Total Students: {total}")
    print(f"Total Marks: {db.get_total_marks():.2f}")
    print(f"Average Marks: {db.get_average_marks():.2f}")
    print(f"Highest Marks: {db.get_highest_marks():.2f}")
    print(f"Lowest Marks: {db.get_lowest_marks():.2f}")


def display_course_statistics(db):
    statistics = db.get_course_statistics()

    if not statistics:
        print("No course records available.")
        return

    print(
        f"\n{'ID':<8}{'Course':<15}{'Students':<12}"
        f"{'Average':<12}{'Highest':<12}{'Lowest':<12}"
    )
    print("-" * 71)

    for course_id, name, total, average, highest, lowest in statistics:
        avg_text = f"{average:.2f}" if average is not None else "N/A"
        high_text = f"{highest:.2f}" if highest is not None else "N/A"
        low_text = f"{lowest:.2f}" if lowest is not None else "N/A"

        print(
            f"{course_id:<8}{name:<15}{total:<12}"
            f"{avg_text:<12}{high_text:<12}{low_text:<12}"
        )


def main():
    db = Database()

    try:
        db.connect()
        db.create_tables()

        while True:
            print("\n===== Student Management System =====")
            print("1. Add Course")
            print("2. View Courses")
            print("3. Add Student")
            print("4. View All Students")
            print("5. Search Student")
            print("6. Search Students by Course")
            print("7. Search Students by Marks")
            print("8. Sort Students")
            print("9. Top N Students")
            print("10. Update Student")
            print("11. Delete Student")
            print("12. Student Statistics")
            print("13. Course-wise Statistics")
            print("14. Courses Without Students")
            print("15. Transfer Student Course")
            print("16. View Course Transfer History")
            print("17. Exit")

            choice = input("Enter your choice (1-17): ").strip()

            if choice == "1":
                try:
                    course_id = int(input("Enter Course ID: "))
                    course_name = input("Enter Course Name: ")
                    course = Course(course_id, course_name)
                    db.add_course(course)
                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "2":
                display_courses(db.get_all_courses())

            elif choice == "3":
                try:
                    student_id = int(input("Enter Student ID: "))
                    name = input("Enter Name: ")
                    age = int(input("Enter Age: "))
                    course_id = int(input("Enter Course ID: "))
                    marks = float(input("Enter Marks: "))

                    if db.get_course_by_id(course_id) is None:
                        print("Invalid course ID.")
                        continue

                    student = Student(
                        student_id, name, age, course_id, marks
                    )
                    db.add_student(student)

                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "4":
                display_students_with_courses(db.get_students_with_courses())

            elif choice == "5":
                try:
                    student_id = int(input("Enter Student ID to search: "))
                    display_student(db.get_student_by_id(student_id))
                except ValueError:
                    print("Student ID must be an integer.")

            elif choice == "6":
                try:
                    course_id = int(input("Enter Course ID: "))
                    if db.get_course_by_id(course_id) is None:
                        print("Invalid course ID.")
                    else:
                        display_students(db.get_students_by_course(course_id))
                except ValueError:
                    print("Course ID must be an integer.")

            elif choice == "7":
                try:
                    min_marks = float(input("Enter minimum marks (0-100): "))
                    display_students(db.get_students_by_marks(min_marks))
                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "8":
                print("1. Sort by marks (Descending)")
                print("2. Sort by marks (Ascending)")
                sort_choice = input("Choose sorting order (1-2): ").strip()

                if sort_choice == "1":
                    display_students(db.get_students_sorted_by_marks(desc=True))
                elif sort_choice == "2":
                    display_students(db.get_students_sorted_by_marks(desc=False))
                else:
                    print("Invalid sorting choice.")

            elif choice == "9":
                try:
                    limit = int(input("Enter number of top students: "))
                    display_students(db.get_top_students(limit))
                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "10":
                try:
                    student_id = int(input("Enter Student ID to update: "))
                    existing = db.get_student_by_id(student_id)

                    if existing is None:
                        print("Student not found.")
                        continue

                    print("Current student details:")
                    display_student(existing)

                    name = input("Enter new Name: ")
                    age = int(input("Enter new Age: "))
                    course_id = int(input("Enter new Course ID: "))
                    marks = float(input("Enter new Marks: "))

                    db.update_student(
                        student_id, name, age, course_id, marks
                    )
                except ValueError as e:
                    print(f"Validation/Input error: {e}")

            elif choice == "11":
                try:
                    student_id = int(input("Enter Student ID to delete: "))
                    delete_student_with_confirmation(db, student_id)
                except ValueError:
                    print("Student ID must be an integer.")

            elif choice == "12":
                display_student_statistics(db)

            elif choice == "13":
                display_course_statistics(db)

            elif choice == "14":
                print("\n===== Courses Without Students =====")
                display_courses(db.get_courses_without_students())


            elif choice == "15":
                try:
                    student_id = int(input("Enter Student ID to transfer: "))
                    new_course_id = int(input("Enter new Course ID: "))
                    db.transfer_student_course(student_id, new_course_id)
                except ValueError as e:
                    print(f"Transfer failed: {e}")
                except Exception as e:
                    print(f"Database error: {e}")

            elif choice == "16":
                print("\n===== Student Course Transfer History =====")
                history = db.get_course_history()

                if not history:
                    print("No course transfer history found.")
                else:
                    for record in history:
                        print(
                            f"History ID: {record[0]}, "
                            f"Student ID: {record[1]}, "
                            f"Name: {record[2]}, "
                            f"Old Course: {record[4]}, "
                            f"New Course: {record[6]}, "
                            f"Changed At: {record[7]}"
                        )

            elif choice == "17":
                print("Exiting Student Management System.")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 17.")


    except Exception as e:
        print(f"Application error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()

