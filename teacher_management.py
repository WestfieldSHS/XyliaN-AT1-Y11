import os, json, shutil
import time, random
from student_management import load_user_data, save_user_data
def load_teacher_data(name):
    filename = f"teachers/{name.lower()}.json"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    # If teacher data file doesn't exist, create a new teacher data structure
    new_teacher = {
        "name": name,
        "pronouns": "",
        "teacher_id":"",
        "educational_institution": "",
        "class_codes": [],
        "students": []
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(new_teacher, f, indent=4)
    return new_teacher
#save teacher data to file
def save_teacher_data(teacher):
    filename = f"teachers/{teacher['name'].lower()}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(teacher, f, indent=4)

#Teacher login
def teacher_info(signup=False):
    name = input("Enter your full name: ").strip()
    first_name, last_name = name.split(" ", 1) #Split name input into first and last name
    educational_institution = input("Enter your educational institution: ").strip()
    pronouns = input("What would you like us to call you? (Mr./Ms./Mrs./Dr.): ").strip()
    edu_initials = ''.join([word[0].upper() for word in educational_institution.split()]) #Get initials of educational institution
    teacher_id = f"T{int(time.time())}{first_name[0].upper()}{last_name[0].upper()}{random.randint(1000, 9999)}" #Teacher ID format: T + current timestamp in seconds + Teacher's initials + random 2 digit number and school's initials to ensure uniqueness
    teacher_data = {
        "name": name,
        "teacher_id": teacher_id,
        "pronouns": pronouns,
        "educational_institution": educational_institution,
        "class_codes": [],
        "students": []
    }
    save_teacher_data(teacher_data)
    teacher = load_teacher_data(name)
    print(f"Welcome, {teacher['pronouns']} {teacher['name']}!")
    return teacher

def teacher_login(teacher):
    #Check if teacher is new or returning by checking if they have their id and matching name in the teacher data file
    if not teacher['teacher_id'] or teacher['name'].lower() != os.name.lower():
        print("It looks like you're new here. We've created a profile for you.")
        print("Would you like to sign up as a teacher? (y/n): ")
        choice = input().strip().lower()
        if choice == 'y':
            return teacher_info(signup=True)    
        elif choice == 'n':
            print("No worries! You can sign up as a teacher anytime from the main menu.")
            return None
    else:
        print(f"Welcome back, {teacher['pronouns']} {teacher['name']}!")
        teacher_menu(teacher)
    load_teacher_data(teacher['name']) #Reload teacher data to ensure any updates are reflected
    return teacher

def teacher_menu(teacher):
    while True:
        print("\nTeacher Menu-------------------:")
        print("1. Create Class")
        print("2. View Class")
        print("3. View Class List")
        print("4. Logout")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == '1':
            create_class(teacher)
        elif choice == '2':
            #If teacher has no classes, prompt to create one first
            if not teacher['class_codes']:
                print("You have no classes yet. Please create a class first.")
                continue
            elif teacher['class_codes']: #If teacher has classes, show class menu
                class_menu(teacher)
        elif choice == '3':
            view_class_list(teacher)
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def create_class(teacher):
    import random
    class_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    teacher['class_codes'].append(class_code)
    save_teacher_data(teacher)
    print(f"Class created successfully! Class code: {class_code}")
    return class_code

def view_class_list(teacher):
    if not teacher['class_codes']:
        print("You have no classes yet.")
        return
    print("Your Classes:")
    for idx, code in enumerate(teacher['class_codes'], start=1):
        print(f"{idx}. Class Code: {code} - Students: {len(teacher['students'])}") #Show number of students in each class
        #Print student names in each class
        if teacher['students']:
            print("   Students:")
            for student in teacher['students']:
                print(f"   - {student}")
            
def class_menu(teacher):
    print("Class Menu-------------------:")
    print("1. View Students")
    print("2. Add Students")
    print("3. Remove Students")
    print("4. View Teacher's Information")
    print("5. Back to Teacher Menu" )
    choice = input("Enter your choice (1-5): ").strip()
    if choice == '1':
        view_students(teacher)
    elif choice == '2':
        add_students(teacher)
    elif choice == '3':
        remove_students(teacher)
    elif choice == '4':
        view_teacher_info(teacher)
    else:
        print("Invalid choice. Please try again.")

def view_students(teacher):
    #IF teacher has no students, prompt to add students first
    if not teacher['students']:
        print("You have no students yet. Please add students first.")
        return add_students(teacher)
    print("Your Students:")
    for idx, student in enumerate(teacher['students'], start=1):
        print(f"{idx}. {student}")
    
    #Ask teacher if they want to view student details
    view_details = input("Do you want to view student details? (y/n): ").strip().lower()
    if view_details == 'y':
        student_id = input("Enter the student's ID: ").strip().lower()
        if student_id in teacher['students']:
            student_data = load_user_data(student_id)
            print(f"Student Name: {student_data['name']}")
            print(f"Student ID: {student_data['student_id']}")
            print(f"Favourites: {', '.join(student_data['favourites'])}")
            print(f"Reviews: {', '.join(student_data['reviews'])}")
            print(f"Streak: {student_data['streak']['current']} (Longest: {student_data['streak']['longest']})")
        else:
            print("Student not found.")

def add_students(teacher):
    student_id = input("Enter the student's ID to add: ").strip().lower()
    if student_id in teacher['students']:
        print("Student is already in your class.")
        return
    teacher['students'].append(student_id)
    save_teacher_data(teacher)
    print(f"Student {student_id} added successfully!")

def remove_students(teacher):
    student_id = input("Enter the student's ID to remove: ").strip().lower()
    if student_id not in teacher['students']:
        print("Student not found in your class.")
        return
    teacher['students'].remove(student_id)
    save_teacher_data(teacher)
    print(f"Student {student_id} removed successfully!")

def view_teacher_info(teacher):
    print(f"Teacher Name: {teacher['name']}")
    print(f"Teacher ID: {teacher['teacher_id']}")
    print(f"Educational Institution: {teacher['educational_institution']}")
    print(f"Class Codes: {', '.join(teacher['class_codes'])}")
