import os, json
#user data management
def load_user_data(name):
    filename = f"users/{name.lower()}.json"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    # If user data file doesn't exist, create a new user data structure
    new_user = {
        "name": name,
        "favorites": [],
        "reviews": [],
        "streak": {
            "current": 0,
            "longest": 0,
            "last_date": None,
            "freeze_remaining": 0
        },
        "achievement_progress": {
            "1": [],
            "2": [],
            "3": []
        },
        "points": 0,
        "rank": 0
    }
    with open('user.json', 'w', encoding='utf-8') as f:
        json.dump(new_user, f, indent=4)
    return new_user
#save user data to file
def save_user_data(user):
    filename = f"users/{user['name'].lower()}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(user, f, indent=4)