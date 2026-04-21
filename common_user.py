import os, json, datetime, time, random, shutil

# IMPORTANT: Only import modules, not specific functions (prevents circular imports)
import rank
import student_management

user = None


# ---------------------- USER DATA HANDLING ----------------------

def load_common_user_data(name):
    global user
    filename = f"users/{name.lower()}.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            user = json.load(f)
            return user

    # Create new user file
    new_user = {
        "name": name,
        "country": "",
        "selected_topics": [],
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
        "user_id": "",
        "user_password": ""
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_user, f)

    user = new_user
    return new_user


def save_common_user_data(user):
    filename = f"users/{user['name'].lower()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(user, f)


# ---------------------- AUTHENTICATION ----------------------

def authenticate_common_user(name, password):
    existed = input("Do you already have an account? (yes/no): ").strip().lower()

    if existed == "yes":
        return common_user_signin()
    elif existed == "no":
        return common_user_signup()
    else:
        print("Invalid input.")
        return authenticate_common_user(name, password)


def common_user_signup():
    print("Let's get you signed up!😊")
    name = input("Enter your full name: ").strip()
    password = input("Create a password: ").strip()
    confirm = input("Re-enter password: ").strip()

    if password != confirm:
        print("Passwords do not match.")
        return common_user_signup()

    user = load_common_user_data(name)
    user["user_password"] = password
    save_common_user_data(user)

    print(f"Welcome, {name}!🚀")

    country = input("Which country are you from? (optional): ").strip()
    if country:
        user["country"] = country
        try:
            with open("country.json", "r", encoding="utf-8") as f:
                country_data = json.load(f)
            if country in country_data:
                user["country_flag"] = country_data[country]
        except:
            pass
        save_common_user_data(user)

    personalised_question()
    time_choice()
    topic_generator()

    return user


def common_user_signin():
    name = input("Enter your full name: ").strip()
    password = input("Enter your password: ").strip()

    user = load_common_user_data(name)

    if user and user["user_password"] == password:
        print(f"Welcome back, {name}!😊")
        student_management.check_streak(name)
        streak_message()
        return user

    print("Invalid name or password.")
    return common_user_signin()


# ---------------------- STREAK MESSAGE ----------------------

def streak_message():
    global user
    current = user["streak"]["current"]
    longest = user["streak"]["longest"]

    if user["streak"]["last_date"] is None:
        print("First time here!🔥")
    print(f"Current streak: {current} days🔥")
    print(f"Longest streak: {longest} days🔥")


# ---------------------- PERSONALISATION QUESTIONS ----------------------

def personalised_question():
    print("Why do you want to improve your vocabulary?")
    print("1. Education and career")
    print("2. Enjoy books more")
    print("3. Communicate effectively")
    print("4. Fun and personal growth")
    print("5. Skip")

    choice = input("Enter 1–5: ").strip()
    responses = {
        "1": "Great choice!🚀",
        "2": "Books become more enjoyable with strong vocabulary!📚",
        "3": "Communication is power!🗣️",
        "4": "Learning is fun!🎉",
        "5": "Skipping!"
    }

    print(responses.get(choice, "Invalid choice"))
    if choice not in responses:
        return personalised_question()


def time_choice():
    print("How much time per day?")
    print("1. 5–10 minutes")
    print("2. 10–20 minutes")
    print("3. 20–30 minutes")
    print("4. 30+ minutes")
    print("5. Skip")

    choice = input("Enter 1–5: ").strip()
    if choice not in ["1", "2", "3", "4", "5"]:
        print("Invalid choice.")
        return time_choice()

    print("Great! Let's continue!⏰")


# ---------------------- TOPIC SELECTION ----------------------

def topic_generator():
    global user
    print("Choose your topics:")
    print("1. Science and Technology")
    print("2. Arts and Literature")
    print("3. Business and Finance")
    print("4. Sports and Entertainment")
    print("5. Humanities and Social Science")
    print("6. Skip")

    choice = input("Enter 1–6: ").strip()

    topics = {
        "1": "Science and Technology",
        "2": "Arts and Literature",
        "3": "Business and Finance",
        "4": "Sports and Entertainment",
        "5": "Humanities and Social Science"
    }

    if choice in topics:
        user["selected_topics"].append(topics[choice])
        save_common_user_data(user)
        print(f"Added topic: {topics[choice]}🎉")
    elif choice == "6":
        print("Skipping.")
    else:
        print("Invalid choice.")
        return topic_generator()


# ---------------------- MENU ----------------------

def common_user_menu():
    print("\nMenu:")
    print("1. View Vocabulary")
    print("2. Add to Favorites")
    print("3. Review Words")
    print("4. View User Information")
    print("5. View Achievements")
    print("6. View Rankings")
    print("7. View Topics")
    print("8. Exit")

    choice = input("Choose 1–8: ").strip()

    if choice == "1":
        vocab_generator()
    elif choice == "2":
        word = input("Enter word to favorite: ").lower().strip()
        student_management.add_to_favorites(user, word)
    elif choice == "3":
        word = input("Enter word to review: ").lower().strip()
        student_management.user_review(user, word)
    elif choice == "4":
        view_user_information()
    elif choice == "5":
        view_achievements()
    elif choice == "6":
        rank.display_rank(user)
        if input("View global rankings? (yes/no): ").lower() == "yes":
            rank.view_global_rankings()
    elif choice == "7":
        print("Your topics:", ", ".join(user["selected_topics"]))
    elif choice == "8":
        print("Goodbye!🔥")
        return
    else:
        print("Invalid choice.")

    return common_user_menu()


# ---------------------- VOCABULARY ----------------------

def vocab_generator():
    global user
    with open("vocab.json", "r", encoding="utf-8") as f:
        vocab_data = json.load(f)

    selected_vocab = [
        word for word, info in vocab_data.items()
        if info["topic"] in user["selected_topics"]
    ]

    random.shuffle(selected_vocab)

    print("Here are your words:")
    for word in selected_vocab[:5]:
        info = vocab_data[word]
        print(f"{word} ({info['type']}): {info['definition']}")
        print()


def review_words(word):
    student_management.user_review(word)
    student_management.check_achievement(user, user)
    save_common_user_data(user)


# ---------------------- USER INFO ----------------------

def view_user_information():
    global user
    print(f"Name: {user['name']}")
    print(f"Country: {user.get('country', 'Not specified')}")
    print(f"Favourites: {', '.join(user['favourites'])}")
    print(f"Reviews: {len(user['reviews'])}")
    print(f"Current Streak: {user['streak']['current']}🔥")
    print(f"Longest Streak: {user['streak']['longest']}🔥")
    student_management.show_achievements()


def view_achievements():
    student_management.check_achievement(user, user)
    student_management.show_achievements()


# ---------------------- MAIN ENTRY ----------------------

def common_user_main():
    global user
    authenticate_common_user("", "")
    common_user_menu()
