import os
import json


#  LOAD ALL USERS (students + common users)

def load_all_users():
    users = []

    folders = ["students", "common_user"]

    for folder in folders:
        if not os.path.exists(folder):
            continue

        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                path = os.path.join(folder, filename)
                with open(path, "r", encoding="utf-8") as f:
                    user = json.load(f)

                # Mark user type
                user["is_common_user"] = (folder == "common_user")
                users.append(user)

    return users


#  SAVE USER BACK TO CORRECT FOLDER
def save_user(user):
    folder = "common_user" if user.get("is_common_user") else "students"
    path = f"{folder}/{user['name'].lower()}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(user, f, indent=4)



#  CALCULATE POINTS + RANK FOR ALL USERS
def calculate_rank():
    all_users = load_all_users()

    # Calculate points
    for u in all_users:
        words_learned = len(u.get("reviews", []))
        points = words_learned * 10

        # Bonus for streak
        if u.get("streak", {}).get("current", 0) >= 7: #if the user has a current streak of 7 or more days, they receive a bonus of 50 points.
            points += 50

        u["points"] = points

    # Sort by points (descending)
    all_users.sort(key=lambda x: x["points"], reverse=True) #key=lambda to sort fuction, x is each user, sort by points, reverse for descending order

    # Assign ranks
    for i, u in enumerate(all_users): #enumerate gives us the index (i) and the user (u) for each user in the sorted list
        u["rank"] = i + 1
        save_user(u)  # Save updated rank + points

    return all_users


#  DISPLAY RANK FOR CURRENT USER
def display_rank(user):
    calculate_rank()  # Update global rankings first

    print("\n🏆 Your Ranking -------------------")
    print(f"Name: {user['name']}")
    print(f"Rank: {user.get('rank', 'N/A')}")
    print(f"Points: {user.get('points', 0)}")

#  VIEW GLOBAL RANKINGS

def view_global_rankings():
    all_users = calculate_rank()

    print("\n🌍 Global Rankings -------------------")
    for u in all_users:
        print(f"{u['rank']}. {u['name']} - {u['points']} points")
