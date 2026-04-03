# Vocabulary daily refresh feature
import json, datetime

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
        word = input("Enter the word you want to add to favorites: ").strip()
        add_to_favorites(word)  
        print() #blank line for better readability
    elif menu == '3':
        word = input("Enter the word you want to review: ").strip()
        user_review(word)
        print() #blank line for better readability
   
    elif menu == '4':
        print(f"Name: {user['name']}")
        print(f"Favorites: {', '.join(user['favourites'])}")
        print(f"Reviews: {len(user['reviews'])}")
        print() #blank line for better readability
    elif menu == '5':
        exit_program()
    else: 
        input("Invalid option. Please select a number between 1-5 only.🫩 Please enter to try again")
        print() #blank line for better readability
    return menu_selection() #loop the menu until user select exit option


print() #blank line for better readability

def exit_program():
    print("Goodbye! Don't forget to come back tomorrow for new words!🔥✨")  
    exit() #Exit the program

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
   #Check if the word exits in vocab.json
   if word not in vocab:
       print(f'"{word}" is not in the vocabulary list. Please try another word.')
       return
   
   #Check if user has already reviewed the word
   if word in reviewed_words:
       reviewed_words = [review['word'] for review in user['reviews']]
       print(f'You have already reviewed the word "{word}".')
       return #Exit the function if the word has already been reviewed
   
   #User input for reviewing the word
   definition = input(f'Enter your definition for word "{word}": ')
   user['reviews'].append({"word": word, "definition": definition})
   print(f'Review added for word "{word}".') 

#streak feature
def check_streak(last_date, current, longest_streak, name, now=None):
    #Simulate current date for testing purposes
    if now is None:
        now = datetime.date.now()
        #Convert last_date to date
        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d").date()
        delta = (now - last_date).days
        if delta == 1: #User revisits the app the next day, increase current streak by one
            current += 1
            print(f"Great job, {name}! Your current streak is now {current} days!🔥")
            if current > longest_streak: #Update longest streak if current streak exceeds it
                longest_streak = current
    elif delta in (2, 3): #User breaks the streak after 2 or 3 days, freeze current streak
        print(f"Welcome back, {name}! Your current streak is frozen at {current} days. Keep up the good work!🔥")
    elif delta > 4: #User breaks the streak after 4 days, reset streak to 0
        current = 0
        print(f"Welcome back, {name}! Your streak has been reset to 0. Don't worry, you can start building it up again!🔥")
    else: #User revisits the app on the same day, no change to streak
        None
    return current, longest_streak

    

#calling functions
user_info()
display_menu()
menu_selection()

#testing streak feature
if __name__ == "__main__":
    check_streak("2026-04-01", 5, 10, "Alice") #simulate user revisit the app after 5 days
  