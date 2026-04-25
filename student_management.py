import os, json, datetime, time, random, shutil
import rank
import common_user

import os, json, datetime

os.makedirs("students", exist_ok=True)

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
        "class_code": ""
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_user, f, indent=4)

    return new_user


def save_student_data(user):
    filename = f"students/{user['name'].lower()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(user, f, indent=4)

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
    user = load_student_data(name)
    user["name"] = name

    # 3. Ask for class code
    join = input("Enter class code to join (6 digits): ").strip()

    if join and not join.isdigit(): #If the user entered incorrect class code, ask user to re-enter
        print("Invalid class code. It should be 6 digits.")
        join = ""
    # If user re-entered over 3 times, ask user if they want to switch to common user instead and ask their teacher for the class code later
    attempts = 0

    while join and not join.isdigit():
        attempts += 1
        if attempts >= 3:
            choice = input("Do you want to continue as a common user instead? (Yes/No): ").strip().lower()
            if choice == "yes":
                print("Switching to common user. You can join a class later with the class code provided by your teacher.")
                common_user.common_user_main()
            elif choice == "no":
                print("Class not found. Please ask your teacher for the correct class code and try again.")
                print("Exiting program.")
                exit()
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")
        else:
            print("Invalid class code. It should be 6 digits.")
            join = input("Enter class code to join (6 digits): ").strip()



    # 4. Generate student ID #Only generate student ID if user is new and doesn't have one yet and able to join class successfully, otherwise user can still use the program as a common user without student ID and class features until they can join a class successfully
    if "student_id" not in user and join:
        student_id = (
            f"S{int(time.time())}"
            f"{first_name[0].upper()}{last_name[0].upper()}"
            f"{random.randint(1000, 9999)}"
        )
        user["student_id"] = student_id
        print(f"Your generated student ID is: {student_id}")

    # 5. Save class code
    user["class_code"] = join
    save_student_data(user)

    # 6. Join class AFTER loading user
    if join:
        class_folder = f"classes/{join}"
        if os.path.exists(class_folder):
            src = f"students/{user['name'].lower()}.json"
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
        save_student_data(user)
        print(f"current streak: {current} days🔥")
        print(f"longest streak: {longest} days🔥")
        print()
    else:
        # ✅ FIX: call check_streak with ONLY the name
        current, longest = check_streak(name)
        user["streak"]["current"] = current
        user["streak"]["longest"] = longest
        user["streak"]["last_date"] = datetime.date.today().strftime("%Y-%m-%d")
        save_student_data(user)

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
            if not user["reviews"]:
                print("You haven't reviewed any words yet. Let's start with today's words!")
                review_menu(list(vocab.keys())[:5])  # Start with first 5 words for new users
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


# MENU OPTION FUNCTIONS

def show_random_words():
    for word in random.sample(list(vocab.keys()), min(5, len(vocab))):
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
    print()


def add_to_favorites(user, word):
    if word in vocab:
        if word not in user["favourites"]:
            user["favourites"].append(word)
            print(f'"{word}" added to your favourites!')
        else:
            print(f'"{word}" is already in your favourites.')
        save_student_data(user)
    else:
        print(f'"{word}" is not in the vocabulary list.')


def review_menu(word):
    while True:
        print("\nReview Menu--------------------:")
        print("1. Flashcard Review")
        print("2. Quiz Review")
        print("3. Match Mode")
        print("4. Return to Main Menu")

        choice = input("Please select an option (1-5): ").strip()

        if choice == "1":
            flashcard_review(word)

        elif choice == "2":
            quiz_review(word)

        elif choice == "3":
            match_mode(word)
        
        elif choice == "4":
            print("Exiting review. Keep up the great work!🔥✨")
            return student_menu()

        else:
            print("Invalid option. Please select 1–4.")

#------------DIFFERENT REVIEW MODES (FLASHCARD, QUIZ, MATCH)------------

import difflib #For fuzzy matching in quiz review, less strict than exact match but still gives credit for close answers
def quiz_review(word):
    print("\nQuiz Review--------------------:")
    score = 0

    for w in word:
        print(f"\nWord: {w}")
        answer = input("Enter the definition: ").strip().lower()
        correct_answer = vocab[w]["definition"].lower()

        # Use difflib to calculate similarity ratio
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

    print(f"\nYour quiz review score: {score}/{len(word)}")
    check_achievement(user, achievement)
    load_student_data(user["name"])  # Reload student data to update achievements and points
    save_student_data(user)

def match_mode(word):
    print("\nMatch Mode--------------------:")
    print("Match the words with their definitions. Enter the number corresponding to the correct definition.")
    print("You have 10 seconds to answer each word.⏰")
    time.sleep(3) #Give user time to read instructions

    words_list = [w['word'] for w in word]
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

        #Visible timer logic
        for remaining in range(10, 0, -1):
            print(f"Time remaining: {remaining} seconds", end="\r")
            time.sleep(1)
            #Check if user has still have time left to answer
            if answer is None:
                answer = input("Your answer (1-4): ").strip()
                if answer != "":
                    break
        if answer is None or answer == "":
            print("\nTime's up!⏰")
            correct_answer = vocab[w]['definition']
            print(f"The correct definition is: {correct_answer}")
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
            print("Invalid input. Please enter a number corresponding to the options.")
    clear()
    print(f"\nYour match mode score: {correct}/{len(words_list)}")
    time.sleep(3)
    choice = (input("Try again? (Yes/No): ").lower().strip())

    if choice == "yes":
        match_mode(word)
    else:
        print("Exiting match mode. Keep up the great work!🔥✨")
        return review_menu(word)
    rank.calculate_rank(user, correct) #Calculate rank based on match mode score
    rank.update_user_rank(user, correct) #Update rank based on match mode score
    check_achievement(user, achievement)
    load_student_data(user["name"])  # Reload student data to update achievements and points  
    save_student_data(user)

def clear(): #Cross-platform clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

def flashcard_review(word):
    print("\nFlashcard Review--------------------:")
    print("Press Enter to see the definition, then press Enter again to see the example.")

    random.shuffle(word)
    score = 0

    for w in word:
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
    print(f"\nYour flashcard review score: {score}/{len(word)}")
    rank.calculate_rank(user, score) #Calculate rank based on flashcard review score
    rank.update_user_rank(user, score) #Update rank based on flashcard review score
    check_achievement(user, achievement)
    load_student_data(user["name"])  # Reload student data to update achievements and points
    save_student_data(user)

# STREAK + ACHIEVEMENTS

def check_streak(name):
    user = load_student_data(name)
    today = datetime.date.today()

    last_date = user["streak"]["last_date"]

    # If last_date is None, this is the user's first day
    if last_date is None:
        user["streak"]["current"] = 1
        user["streak"]["longest"] = max(user["streak"]["longest"], 1)
        user["streak"]["last_date"] = today.strftime("%Y-%m-%d")
        save_student_data(user)
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
    save_student_data(user)

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

    save_student_data(user)


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
