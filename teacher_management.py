import os, json, shutil, time, random

# ---------- TEACHER ENTRY ----------

def teacher_info():
    print("\nTeacher Login-------------------:")
    teacher = teacher_authentication()
    return teacher


# ---------- LOAD & SAVE TEACHER DATA ----------

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
        "classes": {}   # class_code -> [student names]
    }

    os.makedirs("teachers", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_teacher, f, indent=4)

    return new_teacher


def save_teacher_data(teacher):
    os.makedirs("teachers", exist_ok=True)
    filename = f"teachers/{teacher['name'].lower()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(teacher, f, indent=4)


# ---------- AUTH ----------

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


def teacher_signup():
    name = input("Enter your full name: ").strip()
    first, last = name.split(" ", 1)

    educational_institution = input("Enter your educational institution: ").strip()
    pronouns = input("What would you like us to call you? (Mr./Ms./Mrs./Dr.): ").strip()

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
    print(f"Your Teacher ID is: {teacher_id}")
    return teacher


def teacher_login():
    name = input("Enter your full name: ").strip()
    password = input("Enter your teacher ID: ").strip()
    teacher = load_teacher_data(name)

    if teacher["teacher_id"] == "":
        print("Teacher not found. Please sign up first.")
        return None

    if teacher["teacher_id"] != password:
        print("Incorrect teacher ID.")
        return None

    print(f"Welcome back, {teacher['pronouns']} {teacher['name']}!")
    return teacher


# ---------- TEACHER MENU ----------

def teacher_menu(teacher):
    while True:
        print("\nTeacher Menu-------------------:")
        print("1. Create Class")
        print("2. View Class")
        print("3. View All Classes")
        print("4. View Teacher Info")
        print("5. Logout")

        choice = input("Enter your choice (1-5): ").strip()

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


# ---------- CLASS CREATION & LIST ----------

def create_class(teacher):
    class_code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))

    teacher["class_codes"].append(class_code)
    teacher["classes"][class_code] = []

    os.makedirs(f"classes/{class_code}", exist_ok=True)

    # create class_info.json with no topic yet
    class_info_path = f"classes/{class_code}/class_info.json"
    if not os.path.exists(class_info_path):
        class_info = {
            "class_code": class_code,
            "topic": None,
            "students": [] #Number of students
        }
        with open(class_info_path, "w", encoding="utf-8") as f:
            json.dump(class_info, f, indent=4)

    save_teacher_data(teacher)
    print(f"Class created successfully! Class code: {class_code}")


def view_class_list(teacher):
    if not teacher["class_codes"]:
        print("You have no classes yet.")
        return

    print("\nYour Classes:")
    for code in teacher["class_codes"]:
        count = len(teacher["classes"].get(code, []))
        topic = load_class_topic(code)
        topic_display = topic if topic else "No topic set"
        print(f"- {code} ({count} students) | Topic: {topic_display}")
        

def update_class_student_list(class_code, student_name, action="add"):
    class_info_path = f"classes/{class_code}/class_info.json"

    # Load class info
    with open(class_info_path, "r", encoding="utf-8") as f:
        class_info = json.load(f)

    # Ensure "students" list exists
    if "students" not in class_info:
        class_info["students"] = []

    # Add or remove student
    if action == "add":
        if student_name not in class_info["students"]:
            class_info["students"].append(student_name)

    elif action == "remove":
        if student_name in class_info["students"]:
            class_info["students"].remove(student_name)

    # Save updated file
    with open(class_info_path, "w", encoding="utf-8") as f:
        json.dump(class_info, f, indent=4)



# ---------- CLASS MENU ----------

def class_menu(teacher):
    while True:
        print("\nClass Menu-------------------:")
        print("1. View Students")
        print("2. Add Student")
        print("3. Remove Student")
        print("4. Set Class Topic")
        print("5. Back")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            view_students(teacher)
        elif choice == "2":
            add_student(teacher)
        elif choice == "3":
            remove_student(teacher)
        elif choice == "4":
            set_class_topic(teacher)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")


# ---------- CLASS TOPIC HANDLING ----------

TOPIC_OPTIONS = {
    "1": "Science and Technology",
    "2": "Arts and Literature",
    "3": "Business and Finance",
    "4": "Sports and Entertainment",
    "5": "Humanities and Social Science"
}

def load_class_topic(class_code):
    class_info_path = f"classes/{class_code}/class_info.json"
    if not os.path.exists(class_info_path):
        return None

    with open(class_info_path, "r", encoding="utf-8") as f:
        info = json.load(f)
    return info.get("topic")


def save_class_topic(class_code, topic):
    os.makedirs(f"classes/{class_code}", exist_ok=True)
    class_info_path = f"classes/{class_code}/class_info.json"

    info = {
        "class_code": class_code,
        "topic": topic
    }

    with open(class_info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4)


def set_class_topic(teacher):
    class_code = input("Enter class code: ").strip()

    if class_code not in teacher["classes"]:
        print("Class not found.")
        return

    print("\nChoose a topic for this class:")
    for key, value in TOPIC_OPTIONS.items():
        print(f"{key}. {value}")

    choice = input("Enter 1–5: ").strip()
    if choice not in TOPIC_OPTIONS:
        print("Invalid choice.")
        return

    topic = TOPIC_OPTIONS[choice]
    save_class_topic(class_code, topic)
    print(f"Topic for class {class_code} set to: {topic}")


# ---------- STUDENT LIST MANAGEMENT ----------

def view_students(teacher):
    class_code = input("Enter class code: ").strip()

    if class_code not in teacher["classes"]:
        print("Class not found.")
        return

    students = teacher["classes"][class_code]

    if not students:
        print("No students in this class.")
        return

    print("\nStudents:")
    for s in students:
        print("-", s)


def add_student(teacher):
    class_code = input("Enter class code: ").strip()
    if class_code not in teacher["classes"]:
        print("Class not found.")
        return

    quantity = int(input("Enter number of students to add: ").strip())

    for _ in range(quantity):
        student_name = input("Enter student name: ").strip()
        teacher["classes"][class_code].append(student_name)

        # ensure student file exists in students/
        os.makedirs("students", exist_ok=True)
        student_file = f"students/{student_name.lower()}.json"
        if not os.path.exists(student_file):
            new_user = {
                "name": student_name,
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
                "rank": 0,
                "student_id": "",
                "class_code": class_code,
                "selected_topics": []
            }
            with open(student_file, "w", encoding="utf-8") as f:
                json.dump(new_user, f, indent=4)

    save_teacher_data(teacher)
    print(f"Added {quantity} students to class {class_code}.")


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


# ---------- MAIN ENTRY ----------

def teacher_main():
    teacher = teacher_authentication()
    if teacher:
        teacher_menu(teacher)
