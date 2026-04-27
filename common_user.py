import os, json, random, time, sys, termios, tty
import student_management
import rank   # safe now — rank.py no longer imports common_user

# Ensure folder exists
os.makedirs("common_user", exist_ok=True)

user = None

with open("achievement.json", "r", encoding="utf-8") as f:
    achievement_data = json.load(f)

# ---------------------- USER DATA HANDLING ----------------------

def load_common_user_data(name):
    global user
    filename = f"common_user/{name.lower()}.json"

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            user = json.load(f)
            user["is_common_user"] = True
            return user

    # Create new common user file
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
        "user_password": "",
        "is_common_user": True
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_user, f, indent=4)

    user = new_user
    return new_user


def save_common_user_data(user_obj):
    filename = f"common_user/{user_obj['name'].lower()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(user_obj, f, indent=4)


# ---------------------- AUTHENTICATION ----------------------

def authenticate_common_user():
    existed = input("Do you already have an account? (yes/no): ").strip().lower()

    if existed == "yes":
        return common_user_signin()
    elif existed == "no":
        return common_user_signup()
    else:
        print("Invalid input.")
        return authenticate_common_user()


def common_user_signup():
    global user
    print("Let's get you signed up!😊")
    name = input("Enter your full name: ").strip()

    password = input_password("Create a password: ")
    confirm = input_password("Re-enter password: ")

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
        save_common_user_data(user)

    personalised_question()
    time_choice()
    topic_generator()

    return user


def common_user_signin():
    global user
    name = input("Enter your full name: ").strip()
    password = input_password("Enter your password: ")

    user = load_common_user_data(name)

    if user and user["user_password"] == password:
        print(f"Welcome back, {name}!😊")
        # Optional: if you want streaks for common users, handle them here separately
        streak_message()
        return user

    print("Invalid name or password.")
    return common_user_signin()


# ---------------------- PASSWORD INPUT ----------------------

def input_password(prompt="Enter password: "):
    print(prompt, end="", flush=True)
    password = ""

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)

            if ch in ("\n", "\r"):
                print()
                break

            if ch == "\x7f":  # backspace
                if password:
                    password = password[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue

            password += ch
            sys.stdout.write("*")
            sys.stdout.flush()

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return password


# ---------------------- STREAK MESSAGE ----------------------

def streak_message():
    print(f"Current streak: {user['streak']['current']} days🔥")
    print(f"Longest streak: {user['streak']['longest']} days🔥")


# ---------------------- PERSONALISATION QUESTIONS ----------------------

def personalised_question():
    print("Why do you want to improve your vocabulary?")
    print("1. Education and career")
    print("2. Enjoy books more")
    print("3. Communicate effectively")
    print("4. Fun and personal growth")
    print("5. Skip")

    choice = input("Enter 1–5: ").strip()
    if choice not in ["1", "2", "3", "4", "5"]:
        print("Invalid choice.")
        return personalised_question()

    print("Great choice!🚀")


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
        if topics[choice] not in user["selected_topics"]:
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
    while True:
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
            # Make sure student_management uses THIS user for review
            student_management.user = user
            if not user["reviews"]:
                print("You haven't reviewed any words yet. Let's start with today's words!")
                student_management.review_menu(list(student_management.vocab.keys())[:5])
            else:
                student_management.review_menu(user["reviews"])
        elif choice == "4":
            view_user_information()
        elif choice == "5":
            view_achievements()
        elif choice == "6":
            rank.display_rank(user)
            if input("View global rankings? (yes/no): ").lower().strip() == "yes":
                rank.view_global_rankings()
        elif choice == "7":
            print("Your topics:", ", ".join(user["selected_topics"]) or "None")
            if input("Change topics? (yes/no): ").lower().strip() == "yes":
                topic_generator()
        elif choice == "8":
            print("Goodbye!🔥")
            return
        else:
            print("Invalid choice.")


# ---------------------- VOCABULARY ----------------------

def vocab_generator():
    global user

    with open("vocab.json", "r", encoding="utf-8") as f:
        vocab_data = json.load(f)

    # If user skipped topic selection → show random words
    if not user["selected_topics"]:
        print("You didn't select any topics, so here are some random words:")
        print("--------------------")

        random_words = random.sample(list(vocab_data.keys()), min(5, len(vocab_data)))

        for word in random_words:
            info = vocab_data[word]
            print(f"{word} ({info['type']}): {info['definition']}")
            print()

            # Add to review list (Option C)
            if word not in user["reviews"]:
                user["reviews"].append(word)

        save_common_user_data(user)
        return

    # Otherwise → filter by selected topics
    selected_vocab = [
        word for word, info in vocab_data.items()
        if info["topic"] in user["selected_topics"]
    ]

    if not selected_vocab:
        print("No words found for your selected topics.")
        return

    random.shuffle(selected_vocab)

    print("Here are your words:")
    print("--------------------")

    # Show 5 topic words
    for word in selected_vocab[:5]:
        info = vocab_data[word]
        print(f"{word} ({info['type']}): {info['definition']}")
        print(f"Example: {info['example']}")
        print()

        # Add to review list (Option C)
        if word not in user["reviews"]:
            user["reviews"].append(word)

    save_common_user_data(user)


def view_user_information():
    print(f"Name: {user['name']}")
    print(f"Country: {user.get('country', 'N/A')}")
    print(f"Favourites: {', '.join(user['favourites']) or 'None'}")
    print(f"Reviews: {len(user['reviews'])}")
    print(f"Current Streak: {user['streak']['current']} days🔥")
    print(f"Longest Streak: {user['streak']['longest']} days🔥")
    print(f"Selected Topics: {', '.join(user['selected_topics']) or 'None'}")


def view_achievements():
    # Use shared achievement logic, but display for THIS user
    student_management.check_achievement(user, achievement_data)

    print("\nAchievements--------------------:")
    for a in achievement_data["achievements"]:
        a_id = str(a["id"])
        unlocked = user["achievement_progress"].get(a_id, [])
        print(f"{a['name']}: {student_management.star_bar(unlocked)}")


# ---------------------- MAIN ENTRY ----------------------

def common_user_main():
    global user
    user = authenticate_common_user()
    # Keep student_management in sync when reusing its functions
    student_management.user = user
    common_user_menu()
