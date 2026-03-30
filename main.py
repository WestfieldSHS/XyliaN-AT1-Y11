# Vocabulary daily refresh feature
import json
import datetime

with open('vocab.json', 'r', encoding='utf-8') as f:
    vocab = json.load(f)
#user data handling
with open('user.json', 'r', encoding='utf-8') as f:
    user = json.load(f)
import random #random module for selecting random words for daily refresh feature
#Welcome message
print("Welcome to Vocabulary!")
#user information input
def user_info():
    name = input("Enter your name: ")
    print() #blank line for better readability
    user['name'] = name
    print(f"Hello, {name}! It's great to have you here. Let's explore some new words together!😊")
    print(f"Current streak: {user['streak']['current']}🔥")
    print(f"Longest streak: {user['streak']['longest']}🔥")
#menu display function
def display_menu():
    print("\nMenu--------------------:")
    print("1. View Vocabulary")
    print("2. Add to Favorites")
    print("3. Review Words")
    print("4. View User Information")
    print("5. Exit")

def menu_selection():
    menu = input("Please select an option (1-5): ")
    if menu == '1':
        for word in random.sample(list(vocab.keys()), min(10, len(vocab))):  # Print only 10 random words/Refresh daily features
            info = vocab[word]
            print(f'{word} ({info["type"]}): {info["definition"]}')
            print() #blank line for better readability
    elif menu == '2':
        word = input("Enter the word you want to add to favorites: ")
        add_to_favorites(word)  
        print() #blank line for better readability
    elif menu == '3':
        word = input("Enter the word you want to review: ")
        user_review(word)
        print() #blank line for better readability
    elif menu == '4':
        print(f"Name: {user['name']}")
        print(f"Favorites: {', '.join(user['favorites'])}")
        print(f"Reviews: {len(user['reviews'])}")
        print() #blank line for better readability
    elif menu == '5':
        print("Goodbye! Don't forget to come back tomorrow for new words!🔥✨")  
    else: 
        print("Invalid option. Please select a number between 1-5 only.🫩")


print() #blank line for better readability

#favorite words feature
def add_to_favorites(word):
    if word in vocab:
        if word not in user['favourites']:
            user['favourites'].append(word)
            print(f' "{word}" added to your favourites!')
        elif word in user['favourites']:
            print(f' "{word}" is already in your favourites.')
    else:
        None
        
#user review feature
def user_review(word):
    if word in vocab:
        review = input(f'Enter your review for word "{word}": ')
        user['reviews'][word] = review
        print(f'Review added for word "{word}".')
    else:
        None

#streak feature
def check_streak():
    if 'last_Date' in user:
        last_date = user['last_Date']
        current = user['streak']['current']
        longest = user['streak']['longest']
        # check if user have revisit the app within 24 hours
        if last_date:
            last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d') #convert string from user.joson file to date time
            now = datetime.datetime.now()
            if (now - last_date).days == 1: #if user revisit the app within 24 hours, increase currennt streak by 1
                user['streak']['current'] += 1
                print(f"Great job, {user['name']}! Your current streak is now {user['streak']['current']}🔥!") 
                if user['streak']['current'] > longest: #if current streak is longer than longest streak, update longest streak
                    user['streak']['longest'] = user['streak']['current']
                elif (now - last_date).days > 1: #if user revisit the app after 24 hours, reset current streak to 0
                    user['streak']['current'] = 0
                    print(f"Don't worry, {user['name']}! Your current streak has been reset to 0. Let's start building it up again!💪")
                elif (now - last_date).days == 2 or (now - last_date).days == 3: #If user revisit the app after 3 or 4 days, freeze the curren streak for 1 day and give user a warning message
                    print(f"Welcome back, {user['name']}! Your current streak is {user['streak']['current']}🔥. However, since you haven't visited the app for a while, your streak will be frozen for 1 day. Please make sure to visit the app daily to keep your streak alive!💪")
            else:
                print(f"Welcome back, {user['name']}! Your current streak is {user['streak']['current']}🔥. Keep it up!💪")


#calling functions
user_info()
display_menu()
menu_selection()
check_streak()