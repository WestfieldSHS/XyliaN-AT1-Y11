import os, json, datetime, time, random, shutil
from user_management import load_user_data, save_user_data
import rank

# Global user object
user = None

# Load shared data
with open("achievement.json", "r", encoding="utf-8") as f:
    achievement = json.load(f)

with open("vocab.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)


# USER LOGIN + CLASS JOIN
def user_info():
    global user

    # 1. Ask for name
    name = input("Enter your full name: ").strip()
    first_name, last_name = name.split(" ", 1)

    # 2. Load or create user file FIRST
    user = load_user_data(name)
    user["name"] = name

    # 3. Ask for class code
    join = input("Enter class code to join (6 digits): ").strip()

    # 4. Generate student ID
    student_id = (
        f"S{int(time.time())}"
        f"{first_name[0].upper()}{last_name[0].upper()}"
        f"{random.randint(1000, 9999)}"
    )
    user["student_id"] = student_id
    print(f"Your generated student ID is: {student_id}")

    # 5. Save class code
    user["class_code"] = join
    save_user_data(user)

    # 6. Join class AFTER loading user
    if join:
        class_folder = f"classes/{join}"
        if os.path.exists(class_folder):
            src = f"users/{user['name'].lower()}.json"
            shutil.copy(src, class_folder)
            print("Joined class successfully!")
        else:
            print("Invalid class code.")

    print()
    print(f"Hello, {name}! It's great to have you here. Let's explore some new words together!😊")

    # 7. Streak logic
    current = user["streak"]["current"]
    longest = user["streak"]["longest"]

    if user["streak"]["last_date"] is None:
        print("It looks like this is your first time here! Let's start building your vocabulary!🔥📚")
        user["streak"]["last_date"] = datetime.date.today().strftime("%Y-%m-%d")
        save_user_data(user)
        print(f"current streak: {current} days🔥")
        print(f"longest streak: {longest} days🔥")
        print()
    else:
        # ✅ FIX: call check_streak with ONLY the name
        current, longest = check_streak(name)
        user["streak"]["current"] = current
        user["streak"]["longest"] = longest
        user["streak"]["last_date"] = datetime.date.today().strftime("%Y-%m-%d")
        save_user_data(user)

        print(f"current streak: {current} days🔥")
        print(f"longest streak: {longest} days🔥")

        check_achievement(user, achievement)
        print()


# MENU SYSTEM
def student_menu():
    global user
    while True:
        print("\nMenu--------------------:")
        print("1. View Vocabulary")
        print("2. Add to Favorites")
        print("3. Review Words")
        print("4. View User Information")
        print("5. View Achievements")
        print("6. View Rankings")
        print("7. Exit")

        choice = input("Please select an option (1-7): ").strip()

        if choice == "1":
            show_random_words()

        elif choice == "2":
            word = input("Enter the word you want to add to favorites: ").lower().strip()
            # ✅ FIX: pass user into add_to_favorites
            add_to_favorites(user, word)

        elif choice == "3":
            word = input("Enter the word you want to review: ").lower().strip()
            # ✅ FIX: pass user into user_review
            user_review(user, word)

        elif choice == "4":
            show_user_info()

        elif choice == "5":
            check_achievement(user, achievement)
            show_achievements()

        elif choice == "6":
            rank.display_rank(user)
            choice2 = input("View global rankings? (Yes/No): ").lower().strip()
            if choice2 == "yes":
                rank.view_global_rankings()

        elif choice == "7":
            print("Goodbye! Don't forget to come back tomorrow for new words!🔥✨")
            return

        else:
            print("Invalid option. Please select 1–7.")


# MENU OPTION FUNCTIONS

def show_random_words():
    for word in random.sample(list(vocab.keys()), min(5, len(vocab))):
        info = vocab[word]
        print(f"{word} ({info['type']}): {info['definition']}")
        print()


def show_user_info():
    print(f"Name: {user['name']}")
    print(f"Class: {user.get('class_code', 'None')}")
    print(f"Favourites: {', '.join(user['favourites'])}")
    print(f"Reviews: {len(user['reviews'])}")
    print(f"Current Streak: {user['streak']['current']} days🔥")
    print(f"Longest Streak: {user['streak']['longest']} days🔥")
    print()


def add_to_favorites(user, word):
    if word in vocab:
        if word not in user["favourites"]:
            user["favourites"].append(word)
            print(f'"{word}" added to your favourites!')
        else:
            print(f'"{word}" is already in your favourites.')
        save_user_data(user)
    else:
        print(f'"{word}" is not in the vocabulary list.')


def user_review(user, word):
    if word not in vocab:
        print(f'"{word}" is not in the vocabulary list.')
        return

    reviewed_words = [review["word"] for review in user["reviews"]]
    if word in reviewed_words:
        print(f'You have already reviewed "{word}".')
        return

    definition = input(f'Enter your definition for "{word}": ')
    print()

    correct_definition = vocab[word]["definition"]
    print(f'The correct definition of "{word}" is: {correct_definition}')
    print(vocab[word]["example"])
    print()

    user["reviews"].append({"word": word, "definition": definition})
    save_user_data(user)

    check_achievement(user, achievement)
    print(f'Review added for "{word}".')
    print()


# STREAK + ACHIEVEMENTS

def check_streak(name):
    user = load_user_data(name)
    today = datetime.date.today()

    last_date = user["streak"]["last_date"]

    # If last_date is None, this is the user's first day
    if last_date is None:
        user["streak"]["current"] = 1
        user["streak"]["longest"] = max(user["streak"]["longest"], 1)
        user["streak"]["last_date"] = today.strftime("%Y-%m-%d")
        save_user_data(user)
        return user["streak"]["current"], user["streak"]["longest"]

    # Otherwise, parse the stored date
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d").date()

    # Calculate streak normally
    if today == last_date:
        pass  # same day, streak unchanged
    elif today == last_date + datetime.timedelta(days=1):
        user["streak"]["current"] += 1
    else:
        user["streak"]["current"] = 1  # streak reset

    # Update longest streak
    user["streak"]["longest"] = max(user["streak"]["longest"], user["streak"]["current"])

    # Save updated date
    user["streak"]["last_date"] = today.strftime("%Y-%m-%d")
    save_user_data(user)

    return user["streak"]["current"], user["streak"]["longest"]


def check_achievement(user, achievement):
    for a in achievement["achievements"]:
        a_id = str(a["id"])
        unlocked = user["achievement_progress"].get(a_id, [])

        for star_info in a["stars"]:
            star = star_info["star"]
            req = star_info["requirement"]

            if star in unlocked:
                continue

            if a["type"] == "reviews" and len(user["reviews"]) >= req:
                unlocked.append(star)

            elif a["type"] == "streak" and user["streak"]["current"] >= req:
                unlocked.append(star)

            elif a["type"] == "freeze" and user["streak"]["freeze_remaining"] <= req:
                unlocked.append(star)

        user["achievement_progress"][a_id] = unlocked

    save_user_data(user)


def star_bar(unlocked_stars):
    return "★" * len(unlocked_stars) + "☆" * (5 - len(unlocked_stars))


def show_achievements():
    print("\nAchievements--------------------:")
    for a in achievement["achievements"]:
        a_id = str(a["id"])
        unlocked = user["achievement_progress"].get(a_id, [])
        print(f"{a['name']}: {star_bar(unlocked)}")


# MAIN ENTRY POINT
def student_main():
    user_info()
    student_menu()
