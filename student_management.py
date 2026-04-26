import os, json, datetime, time, random, shutil, difflib
import rank
from teacher_management import load_class_topic

os.makedirs("students", exist_ok=True)

# ---------- LOAD & SAVE STUDENT DATA ----------

def load_student_data(name):
    filename = f"students/{name.lower()}.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    new_user = {
        "name": name,
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
        "student_id": "",
        "class_code": "",
        "selected_topics": []
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_user, f, indent=4)

    return new_user


def save_student_data(user):
    filename = f"students/{user['name'].lower()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(user, f, indent=4)


# ---------- GLOBALS ----------

user = None

with open("achievement.json", "r", encoding="utf-8") as f:
    achievement = json.load(f)

with open("vocab.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)


# ---------- USER LOGIN + CLASS JOIN ----------

def user_info():
    global user

    name = input("Enter your full name: ").strip()
    first_name, last_name = name.split(" ", 1)

    user = load_student_data(name)
    user["name"] = name

    join = input("Enter class code to join (6 digits): ").strip()

    attempts = 0
    while join and not join.isalnum():
        attempts += 1
        if attempts >= 3:
            print("Class code invalid too many times. Exiting.")
            exit()
        print("Invalid class code. It should be 6 characters (letters/numbers).")
        join = input("Enter class code to join (6 digits): ").strip()

    # generate student ID if new and joined class
    if not user.get("student_id") and join:
        student_id = (
            f"S{int(time.time())}"
            f"{first_name[0].upper()}{last_name[0].upper()}"
            f"{random.randint(1000, 9999)}"
        )
        user["student_id"] = student_id
        print(f"Your generated student ID is: {student_id}")

    user["class_code"] = join

    # inherit topic from class
    if join:
        topic = load_class_topic(join)
        if topic:
            user["selected_topics"] = [topic]
        else:
            user["selected_topics"] = []
    else:
        user["selected_topics"] = []

    save_student_data(user)

    if join:
        class_folder = f"classes/{join}"
        if os.path.exists(class_folder):
            src = f"students/{user['name'].lower()}.json"
            shutil.copy(src, class_folder)
            print("Joined class successfully!")
        else:
            print("Invalid class code.")

    print()
    print(f"Hello, {name}! Let's explore some new words together!😊")

    current = user["streak"]["current"]
    longest = user["streak"]["longest"]

    if user["streak"]["last_date"] is None:
        print("It looks like this is your first time here!🔥📚")
        user["streak"]["last_date"] = datetime.date.today().strftime("%Y-%m-%d")
        save_student_data(user)
        print(f"current streak: {current} days🔥")
        print(f"longest streak: {longest} days🔥")
        print()
    else:
        current, longest = check_streak(name)
        user["streak"]["current"] = current
        user["streak"]["longest"] = longest
        user["streak"]["last_date"] = datetime.date.today().strftime("%Y-%m-%d")
        save_student_data(user)

        print(f"current streak: {current} days🔥")
        print(f"longest streak: {longest} days🔥")

        check_achievement(user, achievement)
        print()


# ---------- MENU SYSTEM ----------

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
            show_topic_words()
        elif choice == "2":
            word = input("Enter the word you want to add to favorites: ").lower().strip()
            add_to_favorites(user, word)
        elif choice == "3":
            if not user["reviews"]:
                print("You haven't reviewed any words yet. Let's start with today's words!")
                review_menu(list(vocab.keys())[:5])
            else:
                review_menu(user["reviews"])
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


# ---------- MENU OPTION FUNCTIONS ----------

def show_topic_words():
    global user
    if not user["selected_topics"]:
        print("No topic set for your class yet. Showing random words:")
        for word in random.sample(list(vocab.keys()), min(5, len(vocab))):
            info = vocab[word]
            print(f"{word} ({info['type']}): {info['definition']}")
            print(f"Example: {info['example']}")
            print()
        return

    topic = user["selected_topics"][0]
    filtered = [w for w, info in vocab.items() if info.get("topic") == topic]

    if not filtered:
        print(f"No words found for topic: {topic}.")
        return

    print(f"Words for topic: {topic}")
    for word in random.sample(filtered, min(5, len(filtered))):
        info = vocab[word]
        print(f"{word} ({info['type']}): {info['definition']}")
        print(f"Example: {info['example']}")
        print()


def show_user_info():
    print(f"Name: {user['name']}")
    print(f"Class: {user.get('class_code', 'None')}")
    print(f"Favourites: {', '.join(user['favourites'])}")
    print(f"Reviews: {len(user['reviews'])}")
    print(f"Current Streak: {user['streak']['current']} days🔥")
    print(f"Longest Streak: {user['streak']['longest']} days🔥")
    print(f"Selected Topic: {user['selected_topics'][0] if user['selected_topics'] else 'None'}")
    print()


def add_to_favorites(user_obj, word):
    if word in vocab:
        if word not in user_obj["favourites"]:
            user_obj["favourites"].append(word)
            print(f'"{word}" added to your favourites!')
        else:
            print(f'"{word}" is already in your favourites.')
        save_student_data(user_obj)
    else:
        print(f'"{word}" is not in the vocabulary list.')


def review_menu(word_list):
    while True:
        print("\nReview Menu--------------------:")
        print("1. Flashcard Review")
        print("2. Quiz Review")
        print("3. Match Mode")
        print("4. Return to Main Menu")

        choice = input("Please select an option (1-4): ").strip()

        if choice == "1":
            flashcard_review(word_list)
        elif choice == "2":
            quiz_review(word_list)
        elif choice == "3":
            match_mode(word_list)
        elif choice == "4":
            print("Exiting review. Keep up the great work!🔥✨")
            return
        else:
            print("Invalid option. Please select 1–4.")


# ---------- REVIEW MODES ----------

def quiz_review(word_list):
    print("\nQuiz Review--------------------:")
    score = 0

    for w in word_list:
        print(f"\nWord: {w}")
        answer = input("Enter the definition: ").strip().lower()
        correct_answer = vocab[w]["definition"].lower()

        similarity = difflib.SequenceMatcher(None, answer, correct_answer).ratio()

        if similarity >= 0.8:
            print("Correct!🔥")
            score += 1
        elif similarity >= 0.6:
            print("Almost there! Partial credit awarded.🔥")
            print(f"The correct definition is: {vocab[w]['definition']}")
            score += 0.5
        else:
            print("Incorrect.🔥")
            print(f"The correct definition is: {vocab[w]['definition']}")

    print(f"\nYour quiz review score: {score}/{len(word_list)}")
    check_achievement(user, achievement)
    save_student_data(user)


def match_mode(word_list):
    print("\nMatch Mode--------------------:")
    print("Match the words with their definitions. You have 10 seconds per word.⏰")
    time.sleep(2)

    words_list = word_list[:]
    definitions_list = [vocab[w]['definition'] for w in words_list]

    correct = 0

    for w in words_list:
        clear()
        print(f"\nWord: {w}")
        options = random.sample(definitions_list, min(4, len(definitions_list)))
        if vocab[w]['definition'] not in options:
            options[random.randint(0, len(options)-1)] = vocab[w]['definition']

        for i, option in enumerate(options):
            print(f"{i+1}. {option}")

        start_time = time.time()
        answer = input("Your answer (1-4): ").strip()
        end_time = time.time()

        if not answer:
            print("\nTime's up!⏰")
            print(f"The correct definition is: {vocab[w]['definition']}")
            time.sleep(2)
            continue

        if answer.isdigit() and 1 <= int(answer) <= len(options):
            if options[int(answer)-1] == vocab[w]['definition']:
                print("Correct!🔥")
                correct += 1
            else:
                print("Incorrect.🔥")
                print(f"The correct definition is: {vocab[w]['definition']}")
            time.sleep(2)
        else:
            print("Invalid input.")
            time.sleep(1)

    clear()
    print(f"\nYour match mode score: {correct}/{len(words_list)}")
    time.sleep(2)
    check_achievement(user, achievement)
    save_student_data(user)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def flashcard_review(word_list):
    print("\nFlashcard Review--------------------:")
    print("Press Enter to see the definition, then the example.")

    random.shuffle(word_list)
    score = 0

    for w in word_list:
        print(f"\nWord: {w}")
        input("Press Enter to see the definition...")
        print(f"Definition: {vocab[w]['definition']}")
        print()
        input("Press Enter to see the example...")
        print(f"Example: {vocab[w]['example']}")
        print()

        while True:
            correct = input("Did you get it right? (Yes/No): ").lower().strip()
            if correct in ["yes", "no"]:
                if correct == "yes":
                    score += 1
                break
            else:
                print("Please enter 'Yes' or 'No'.")

    print(f"\nYour flashcard review score: {score}/{len(word_list)}")
    check_achievement(user, achievement)
    save_student_data(user)


# ---------- STREAK + ACHIEVEMENTS ----------

def check_streak(name):
    u = load_student_data(name)
    today = datetime.date.today()

    last_date = u["streak"]["last_date"]

    if last_date is None:
        u["streak"]["current"] = 1
        u["streak"]["longest"] = max(u["streak"]["longest"], 1)
        u["streak"]["last_date"] = today.strftime("%Y-%m-%d")
        save_student_data(u)
        return u["streak"]["current"], u["streak"]["longest"]

    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d").date()

    if today == last_date:
        pass
    elif today == last_date + datetime.timedelta(days=1):
        u["streak"]["current"] += 1
    else:
        u["streak"]["current"] = 1

    u["streak"]["longest"] = max(u["streak"]["longest"], u["streak"]["current"])
    u["streak"]["last_date"] = today.strftime("%Y-%m-%d")
    save_student_data(u)

    return u["streak"]["current"], u["streak"]["longest"]


def check_achievement(u, achievement_data):
    for a in achievement_data["achievements"]:
        a_id = str(a["id"])
        unlocked = u["achievement_progress"].get(a_id, [])

        for star_info in a["stars"]:
            star = star_info["star"]
            req = star_info["requirement"]

            if star in unlocked:
                continue

            if a["type"] == "reviews" and len(u["reviews"]) >= req:
                unlocked.append(star)
            elif a["type"] == "streak" and u["streak"]["current"] >= req:
                unlocked.append(star)
            elif a["type"] == "freeze" and u["streak"]["freeze_remaining"] <= req:
                unlocked.append(star)

        u["achievement_progress"][a_id] = unlocked

    save_student_data(u)


def star_bar(unlocked_stars):
    return "★" * len(unlocked_stars) + "☆" * (5 - len(unlocked_stars))


def show_achievements():
    print("\nAchievements--------------------:")
    for a in achievement["achievements"]:
        a_id = str(a["id"])
        unlocked = user["achievement_progress"].get(a_id, [])
        print(f"{a['name']}: {star_bar(unlocked)}")


# ---------- MAIN ENTRY ----------

def student_main():
    user_info()
    student_menu()