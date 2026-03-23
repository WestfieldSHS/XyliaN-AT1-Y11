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

def user_info():
    name = input("Enter your name: ")
    user['name'] = name
    print(f"Hello, {name}! It's great to have you here. Let's explore some new words together!")

def display_menu():
    print("\nMenu:")
    print("1. View Vocabulary")
    print("2. Add to Favorites")
    print("3. Leave a Review")
    print("4. View User Information")
    print("5. Exit")
    menu = input(int("Please select an option (1-5): "))
    if menu == 1:
        for word in random.sample(list(vocab.keys()), min(5, len(vocab))):  # Print only 5 random words/Refresh daily features
            info = vocab[word]
            print(f'{word} ({info["type"]}): {info["definition"]}')
            print() #blank line for better readability
    elif menu == 2:
        word = input("Enter the word you want to add to favorites: ")
        add_to_favorites(word)
    elif menu == 3:
        word = input("Enter the word you want to review: ")
        user_review(word)
    elif menu == 4:
        print(f"Name: {user['name']}")
        print(f"Favorites: {', '.join(user['favorites'])}")
        print(f"Reviews: {len(user['reviews'])}")
    elif menu == 5:
        print("Goodbye! Don't forget to come back tomorrow for new words!🔥✨")    


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

#calling functions
user_info()
display_menu()