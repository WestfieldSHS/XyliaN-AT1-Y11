import os, json, datetime, time, random, shutil, difflib, sys, select #shutill for copying student files into class folders, difflib for lenient grading in quiz review, select for non-blocking input in match mode timer
import rank
from teacher_management import load_class_topic
import teacher_management

os.makedirs("students", exist_ok=True) #It creates a folder named students if it doesn’t already exist. exist_ok true prevent crashing if the student already exist

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
    # Prevent saving common users into students/
    if user.get("is_common_user"):
        return

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

    attempts = 0

    # -------- CLASS CODE VALIDATION LOOP --------
    while True:
        join = input("Enter class code to join (6 characters): ").strip()

        # Validate format
        if not join or not join.isalnum() or len(join) != 6:
            attempts += 1
            print("❌ Invalid class code format. It must be 6 letters/numbers.")

        # Check if class folder exists
        elif not os.path.exists(f"classes/{join}"):
            attempts += 1
            print("❌ Class does not exist. Please ask your teacher for the correct class code.")

        else:
            # Class exists → now check topic
            class_info_path = f"classes/{join}/class_info.json"
            if not os.path.exists(class_info_path):
                print("❌ This class has not been set up by the teacher yet.")
                print("Please ask your teacher to set a topic.")
                attempts += 1
            else:
                # Load topic
                with open(class_info_path, "r", encoding="utf-8") as f:
                    class_info = json.load(f)

                topic = class_info.get("topic")
                if not topic:
                    print("❌ Your teacher has not set a topic for this class yet.")
                    print("Please ask your teacher to set a topic.")
                    attempts += 1
                else:
                    # VALID CLASS → break loop
                    break

        # Too many failed attempts → offer switch to common user
        if attempts >= 3:
            print("\nYou've entered an invalid class code too many times.")
            choice = input("Would you like to continue as a common user instead? (yes/no): ").strip().lower()

            if choice == "yes":
                print("\nSwitching to common user mode...")
                import common_user
                common_user.load_common_user_data(name)      # <-- IMPORTANT: create common user profile
                common_user.common_user_main()
                sys.exit()

            else:
                print("\nPlease ask your teacher for the correct class code and try again later.")
                exit()

    # -------- VALID CLASS CODE FROM HERE ON --------

    # Create student file ONLY NOW
    user = load_student_data(name)

    user["class_code"] = join
    user["selected_topics"] = [topic]

    # Generate student ID ONLY NOW
    if not user.get("student_id"):
        student_id = (
            f"S{int(time.time())}"
            f"{first_name[0].upper()}{last_name[0].upper()}"
            f"{random.randint(1000, 9999)}"
        )
        user["student_id"] = student_id
        print(f"Your student ID is: {student_id}")

    save_student_data(user)
    teacher_management.update_class_student_list(join, user["name"], action="add") #add student to class list in teacher management


    # Copy student file into class folder
    if not user.get("is_common_user"):
        shutil.copy(f"students/{user['name'].lower()}.json", f"classes/{join}")

    print(f"\nWelcome to class {join}, {name}! Topic: {topic} 🎉")

    # -------- STREAK LOGIC --------
    current = user["streak"]["current"]
    longest = user["streak"]["longest"]

    if user["streak"]["last_date"] is None:
        print("This is your first day!🔥📚")
        user["streak"]["last_date"] = datetime.date.today().strftime("%Y-%m-%d")
        save_student_data(user)
    else:
        current, longest = check_streak(name)
        user["streak"]["current"] = current
        user["streak"]["longest"] = longest
        user["streak"]["last_date"] = datetime.date.today().strftime("%Y-%m-%d")
        save_student_data(user)

    print()


    # ---------- VALID CLASS CODE -----------

    user["class_code"] = join
    user["selected_topics"] = [topic]

    # Generate student ID ONLY NOW
    if not user.get("student_id"):
        student_id = (
            f"S{int(time.time())}"
            f"{first_name[0].upper()}{last_name[0].upper()}"
            f"{random.randint(1000, 9999)}"
        )
        user["student_id"] = student_id
        print(f"Your student ID is: {student_id}")

    save_student_data(user)

    # Copy student file into class folder
    shutil.copy(f"students/{user['name'].lower()}.json", f"classes/{join}")

    print(f"\nWelcome to class {join}, {name}! Topic: {topic} 🎉")

    # Streak logic
    current = user["streak"]["current"]
    longest = user["streak"]["longest"]

    if user["streak"]["last_date"] is None:
        print("This is your first day!🔥📚")
        user["streak"]["last_date"] = datetime.date.today().strftime("%Y-%m-%d")
        save_student_data(user)
    else:
        current, longest = check_streak(name)
        user["streak"]["current"] = current
        user["streak"]["longest"] = longest
        user["streak"]["last_date"] = datetime.date.today().strftime("%Y-%m-%d")
        save_student_data(user)

    print(f"Current streak: {current} days🔥")
    print(f"Longest streak: {longest} days🔥")
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

    # If teacher hasn't set a topic yet
    if not user["selected_topics"]:
        print("No topic set for your class yet. Showing random words:")
        random_words = random.sample(list(vocab.keys()), min(5, len(vocab)))

        for word in random_words:
            info = vocab[word]
            print(f"{word} ({info['type']}): {info['definition']}")
            print(f"Example: {info['example']}")
            print()

            # Add to review list
            if word not in user["reviews"]:
                user["reviews"].append(word)

        save_student_data(user)
        return

    # Teacher-assigned topic
    topic = user["selected_topics"][0]

    # Filter vocab by topic
    filtered = [w for w, info in vocab.items() if info.get("topic") == topic] #items() gives us both the word (w) and its info (info), so we can check the topic in the info dictionary

    if not filtered:
        print(f"No words found for topic: {topic}.")
        return

    print(f"Words for topic: {topic}")

    # Pick 5 topic words
    selected_words = random.sample(filtered, min(5, len(filtered)))

    for word in selected_words:
        info = vocab[word]
        print(f"{word} ({info['type']}): {info['definition']}")
        print(f"Example: {info['example']}")
        print()

        # Add to review list (Option C)
        if word not in user["reviews"]:
            user["reviews"].append(word)

    save_student_data(user)

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

        similarity = difflib.SequenceMatcher(None, answer, correct_answer).ratio() #divide into ratio of 0 to 1, for less strict grading (e.g. if student misses a word or has minor wording differences, they can still get partial credit)

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
    rank.calculate_rank()  # Update global rankings after quiz review
    save_student_data(user)

#---------- MATCH MODE WITH TIMER & SELECTABLE OPTIONS ----------
def timed_input(prompt, timeout=10):
    print(prompt)
    sys.stdout.flush()

    start = time.time()
    user_input = ""
    typing_started = False  # NEW FLAG

    while True:
        remaining = timeout - (time.time() - start)

        # Only show timer if user hasn't started typing
        if not typing_started: #sys.stdout.write() allows us to overwrite the same line with the timer countdown, and sys.stdout.flush() ensures it updates immediately without waiting for a newline
            sys.stdout.write(f"\r⏳ {remaining:0.1f}s left ") #write() instead of print() to stay on same line, flush to ensure it shows immediately
            sys.stdout.flush()

        # Check input
        rlist, _, _ = select.select([sys.stdin], [], [], 0) # Non-blocking check for input #select() checks if there's input available on sys.stdin without blocking the program. If the user has started typing, we set typing_started to True, which stops the timer from displaying and allows the user to finish their input without time pressure.
        if rlist:
            ch = sys.stdin.read(1)
            typing_started = True  # STOP TIMER IMMEDIATELY

            if ch in ("\n", "\r"):
                # Clear timer line
                sys.stdout.write("\r" + " " * 50 + "\r")
                sys.stdout.flush()
                return user_input.strip()

            user_input += ch
            continue

        # Timeout
        if remaining <= 0:
            sys.stdout.write("\r" + " " * 50 + "\r")
            sys.stdout.flush()
            return None

        time.sleep(0.05)
        
def flush_input():
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]: #flush input is for clearing the input buffer before timed input, so that accidental key presses don't affect the timer
        sys.stdin.read(1) # Read and discard any input that's currently in the buffer, ensuring that the timed input starts with a clean slate and isn't affected by any previous key presses or inputs that the user may have entered before the timer started. This is especially important in match mode, where we want to ensure that the timer accurately reflects the time remaining for each question without being prematurely triggered by leftover input.

def match_mode(word_list):
    print("\nMatch Mode--------------------:")
    print("Match the words with their definitions. You have 10 seconds per word.⏰")
    time.sleep(2) # Brief pause before starting match mode

    words_list = word_list[:]
    definitions_list = [vocab[w]['definition'] for w in words_list]

    correct = 0

    for w in words_list:
        clear() #Clear answer from previous question for better UX in match mode
        print(f"\nWord: {w}")
        options = random.sample(definitions_list, min(4, len(definitions_list)))
        if vocab[w]['definition'] not in options:
            options[random.randint(0, len(options)-1)] = vocab[w]['definition']

        for i, option in enumerate(options): #enumerate options for user to select #enumerate() gives us both the index (i) and the option itself, so we can display numbered options for the user to choose from
            print(f"{i+1}. {option}")

        flush_input() # Clear input buffer before timed input to prevent accidental key presses from affecting the timer
        answer = timed_input("Your answer (1-4): ", timeout=10)

        if answer is None:
            print("\nTime's up!⏰")
            print(f"The correct definition is: {vocab[w]['definition']}")
            time.sleep(2)
            continue


        if not answer:
            print("\nTime's up!⏰")
            print(f"The correct definition is: {vocab[w]['definition']}")
            time.sleep(2)
            continue

        if answer.isdigit() and 1 <= int(answer) <= len(options): #isdigit() checks if the input is a number, and we also check if it's within the range of available options
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
    rank.calculate_rank()  # Update global rankings after match mode
    save_student_data(user)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear') # Clear console for better UX in match mode


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

        while True: #while loop to validate user input for whether they got the flashcard right or not, ensuring they enter either "yes" or "no"
            correct = input("Did you get it right? (Yes/No): ").lower().strip()
            if correct in ["yes", "no"]:
                if correct == "yes":
                    score += 1
                break #break out of the loop if valid input, otherwise keep asking until they enter "yes" or "no"
            else:
                print("Please enter 'Yes' or 'No'.")

    print(f"\nYour flashcard review score: {score}/{len(word_list)}")
    check_achievement(user, achievement)
    rank.calculate_rank()  # Update global rankings after flashcard review
    save_student_data(user)


# ---------- STREAK + ACHIEVEMENTS ----------

def check_streak(name):
    u = load_student_data(name)
    today = datetime.date.today()

    last_date = u["streak"]["last_date"]

    if last_date is None: #none means user is logging in for the first time, so we start their streak at 1 and set last_date to today. We also update longest streak to 1 if it was previously 0, but if they already had a longest streak from before (e.g. they had a streak of 5 but took a break and are now back), we don't want to reset their longest streak to 1, so we use max() to keep the higher value between the existing longest streak and 1.
        u["streak"]["current"] = 1
        u["streak"]["longest"] = max(u["streak"]["longest"], 1) # If it's the user's first day, set current streak to 1 and update longest streak if necessary #max() ensures that if the user already has a longest streak of 5 from before, it won't reset to 1 on their first day back
        u["streak"]["last_date"] = today.strftime("%Y-%m-%d")
        save_student_data(u)
        return u["streak"]["current"], u["streak"]["longest"]

    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d").date()

    if today == last_date:
        pass # User log in on the same day, doesn't affect streak
    elif today == last_date + datetime.timedelta(days=1): #delta(days=1) checks if today is exactly one day after the last date, which means the user has maintained their streak
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


def star_bar(unlocked_stars): #unlocked star is from achievement_progress in student data, which is a list of the stars they've unlocked for that achievement
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