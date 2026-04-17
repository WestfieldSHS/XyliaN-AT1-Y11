import os, json, shutil, time, random #shutil for handling file operations related to class joining feature, time for welcome message effect, random for generating unique teacher IDs and class codes
from user_management import load_user_data, save_user_data #Importing functions to handle user data



def teacher_info():
    print("\nTeacher Login-------------------:")
    teacher = teacher_authentication() #Call teacher authentication function to handle login/signup process
    return teacher
# Load & Save Teacher Data
def load_teacher_data(name):
        filename = f"teachers/{name.lower()}.json"

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)

        new_teacher = {
            "name": name,
            "teacher_id": "",
            "pronouns": "",
            "educational_institution": "",
            "class_codes": [],
            "classes": {}   # list of class's name
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(new_teacher, f, indent=4)

        return new_teacher


def save_teacher_data(teacher):
        filename = f"teachers/{teacher['name'].lower()}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(teacher, f, indent=4)

def teacher_authentication():
    while True:
            choice = input("Do you have an account? (yes/no): ").strip().lower()
            if choice == "yes":
                teacher = teacher_login()
                if teacher:
                    return teacher
            elif choice == "no":
                return teacher_signup()
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        # Teacher Signup
def teacher_signup():
            #If the teacher dosen't exist, create a new teacher profile with their name, educational institution, pronouns, and generate a unique teacher ID. Then save the teacher data and welcome them.
            name = input("Enter your full name: ").strip()
            first, last = name.split(" ", 1)

            educational_institution = input("Enter your educational institution: ").strip()
            pronouns = input("What would you like us to call you? (Mr./Ms./Mrs./Dr.): ").strip()

            # Generate unique teacher ID by combining timestamp, initials, and random number
            teacher_id = (
                f"T{int(time.time())}"
                f"{first[0].upper()}{last[0].upper()}"
                f"{random.randint(1000, 9999)}"
            )

            teacher = {
                "name": name,
                "teacher_id": teacher_id,
                "pronouns": pronouns,
                "educational_institution": educational_institution,
                "class_codes": [],
                "classes": {}
            }

            save_teacher_data(teacher)
            print(f"Welcome, {pronouns} {name}!")
            return teacher

def teacher_login():
            name = input("Enter your full name: ").strip()
            password = input("Enter your teacher ID: ").strip()
            teacher = load_teacher_data(name)

            if teacher["teacher_id"] == "": # Check if teacher ID is empty, which indicates that the teacher profile was just created but not properly set up with a teacher ID. Prompt them to sign up again to ensure they have a valid teacher ID.
                print("Teacher not found. Please sign up first.")
                return None

            if teacher["teacher_id"] != password: # Check if entered teacher ID matches the one stored in the teacher profile. If not, display error message and return None to indicate failed login.
                print("Incorrect teacher ID.")
                return None
            elif teacher["teacher_id"] == password: # If teacher ID matches, welcome the teacher back and return their profile data to be used in the teacher menu.
                print(f"Welcome back, {teacher['pronouns']} {teacher['name']}!")
                return teacher

    # Teacher Menu
def teacher_menu(teacher):
        while True:
            print("\nTeacher Menu-------------------:")
            print("1. Create Class")
            print("2. View Class")
            print("3. View All Classes")
            print("4. View Teacher Info")
            print("5. Logout")

            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                create_class(teacher)

            elif choice == "2":
                if not teacher["class_codes"]:
                    print("You have no classes yet.")
                else:
                    class_menu(teacher)

            elif choice == "3":
                view_class_list(teacher)
            
            elif choice == "4": 
                view_teacher_info(teacher)

            elif choice == "5":
                print("Logging out...")
                break

            else:
                print("Invalid choice. Try again.")

def view_teacher_info(teacher):
        print("\nTeacher Information-------------------:")
        print(f"Name: {teacher['name']}")
        print(f"Teacher ID: {teacher['teacher_id']}")
        print(f"Pronouns: {teacher['pronouns']}")
        print(f"Educational Institution: {teacher['educational_institution']}")
        print(f"Number of Classes: {len(teacher['class_codes'])}")


    # Create Class
def create_class(teacher):
        class_code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6)) # Generate random 6-character class code

        teacher["class_codes"].append(class_code)
        teacher["classes"][class_code] = []

        os.makedirs(f"classes/{class_code}", exist_ok=True) # Create directory for class if it doesn't exist

        save_teacher_data(teacher)
        print(f"Class created successfully! Class code: {class_code}")

    # View All Classes
def view_class_list(teacher):
        if not teacher["class_codes"]: # Check if teacher has any classes
            print("You have no classes yet.") 
            return

        print("\nYour Classes:")
        for code in teacher["class_codes"]: # Loop through class codes and display them with student count
            count = len(teacher["classes"][code])
            print(f"- {code} ({count} students)")


    # Class Menu
def class_menu(teacher):
        print("\nClass Menu-------------------:")
        print("1. View Students")
        print("2. Add Student")
        print("3. Remove Student")
        print("4. Back")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            view_students(teacher)

        elif choice == "2":
            add_student(teacher)

        elif choice == "3":
            remove_student(teacher)

        elif choice == "4":
            return class_menu(teacher) # Return to class menu after viewing students, adding students, or removing students to allow teacher to perform multiple actions without having to navigate back to the class menu each time.
        
        else:
            print("Invalid choice. Try again.")
            class_menu(teacher)
    # View Students
def view_students(teacher):
        class_code = input("Enter class code: ").strip()

        if class_code not in teacher["classes"]: # Check if class code exists in teacher's classes
            print("Class not found.")
            return

        students = teacher["classes"][class_code]

        if not students:
            print("No students in this class.")
            return

        print("\nStudents:")
        for s in students:
            print("-", s) # Loop through students in class and display their names


    # Add Student
def add_student(teacher):
        class_code = input("Enter class code: ").strip()
        quantity = int(input("Enter number of students to add: ").strip()) # Allow teacher to add multiple students at once by entering the number of students they want to add, then looping through that many times to get each student's name and add them to the class.
        # Check if student name already exists in the class to prevent duplicates. If a duplicate is found, display a message and skip adding that student.
        if class_code not in teacher["classes"]:
            print("Class not found.")
            return
        for _ in range(quantity):
            student_name = input("Enter student name: ").strip()
            teacher["classes"][class_code].append(student_name) # Add each entered student name to the class list in the teacher's profile

        else: #Check if student's accounts exist across the platform by looking for their user data file. If a student's account does not exist, create a new user profile for them with default values and save it to the users directory. This ensures that all students added to classes have an account on the platform.
            for student in teacher["classes"][class_code]:
                student_file = f"users/{student.lower()}.json"
                if not os.path.exists(student_file):
                    new_user = {
                        "name": student,
                        "student_id": "",
                        "favourites": [],
                        "reviews": [],
                        "streak": {
                            "current": 0,
                            "longest": 0,
                            "last_date": None,
                            "freeze_remaining": 0
                        },
                        "achievement_progress": {"1": [], "2": [], "3": []},
                        "points": 0,
                        "rank": 0
                    }
                    with open(student_file, "w", encoding="utf-8") as f:
                        json.dump(new_user, f, indent=4)
            
        save_teacher_data(teacher)

        print(f"Added {quantity} students to class {class_code}.")


    # Remove Student
def remove_student(teacher):
        class_code = input("Enter class code: ").strip()

        if class_code not in teacher["classes"]:
            print("Class not found.")
            return

        student_name = input("Enter student name to remove: ").strip()

        if student_name in teacher["classes"][class_code]:
            teacher["classes"][class_code].remove(student_name)
            save_teacher_data(teacher)
            print(f"Removed {student_name} from class {class_code}.")
        else:
            print("Student not found.")

def teacher_main():
    teacher = teacher_authentication()
    if teacher:
     teacher_menu(teacher)
