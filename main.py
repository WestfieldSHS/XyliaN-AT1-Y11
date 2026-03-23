# Vocabulary daily refresh feature
import json

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
        if word not in user['favorites']:
            user['favorites'].append(word)
            print(f' "{word}" added to your favorites!')
        else:
            print(f' "{word}" is already in your favorites.')
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
        # check if user have revisit the site

#calling functions
user_info()
display_menu()
menu_selection()