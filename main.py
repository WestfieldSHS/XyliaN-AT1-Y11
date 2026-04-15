
import os, shutil #os and shutil modules for handling file operations related to class joining feature
import json, datetime, time
user = None #Initialize user variable to None, it will be assigned after loading user data based on name input
from user_management import load_user_data, save_user_data #Importing functions to handle user data
from teacher_management import teacher_info, teacher_menu, create_class, view_class_list, view_teacher_info, teacher_login, teacher_aunthentication, teacher_signup, load_teacher_data, save_teacher_data #handling teacher data
from student_management import check_streak, check_achievement, star_bar, show_achievements, add_to_favorites, user_review, user_info #handling student data
#Welcome message
def welcome_message():
    print("Welcome to Vocabulary!")
    for char in "Let's start building your vocabulary together!🔥📚":
        print(char, end='', flush=True) #Print welcome message with a typing effect
        time.sleep(0.05) #Delay between each character for typing effect
    print() #blank line for better readability
    role_selection() #Call role selection function to determine if user is a student or teacher and direct them to the appropriate menu

def role_selection():
    role = input("Are you a student or a teacher? (Enter 'student' or 'teacher'): ").strip().lower()
    if role == 'teacher':
        teacher = teacher_info() #Call teacher_info function if user is a teacher
        teacher_menu(teacher) #Call teacher_menu function to display teacher menu after logging in
    elif role == 'student':
        user_info() #Call user_info function if user is a student
    else:
        input("Invalid role. Please enter 'student' or 'teacher' only.🫩  Please enter to try again")
        return role_selection() #Loop role selection until user selects a valid role

#Start the program by calling the welcome_message function
welcome_message()
  
  
    