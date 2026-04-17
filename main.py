
import os, shutil #os and shutil modules for handling file operations related to class joining feature
import json, datetime, time
user = None #Initialize user variable to None, it will be assigned after loading user data based on name input
from user_management import load_user_data, save_user_data #Importing functions to handle user data
from teacher_management import teacher_main
from student_management import student_main
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
       teacher_main()
    elif role == 'student':
        student_main()
    else:
        input("Invalid role. Please enter 'student' or 'teacher' only.🫩  Please enter to try again")
        return role_selection() #Loop role selection until user selects a valid role

#Start the program by calling the welcome_message function
welcome_message()
  
  
    