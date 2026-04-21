import json, os
from student_management import load_user_data, save_user_data

#ranking system feature
def update_user_rank(user):
    user["rank"] = calculate_rank(user)
    return user

def calculate_rank(user):
    folder = 'users'
    all_users = []
    #Load all user json files 
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
                all_users.append(json.load(f))
    #Calculate points
    for u in all_users:
        words_learned = len(u['reviews'])
        u['points'] = points = words_learned * 10  # Example point calculation
        if u['streak']['current'] >= 7:
            points += 50 # Bonus points for a streak of 7 or more
    #sort users by points to determine rank
    all_users.sort(key=lambda x: x['points'], reverse=True)
    #Assign ranks
    for i, u in enumerate(all_users):
        u['rank'] = i + 1
#save updated user data back to their respective json files
    for u in all_users:
        save_user_data(u)

def display_rank(user):
    calculate_rank() #Call the calculate_rank function to update user's rank and points before displaying
    print(f"Rank: {user['rank']}")
    print(f"Points: {user['points']}")
    save_user_data(user) #Save user data after updating rank and points

def view_global_rankings():
    print("\nGlobal Rankings🏆-------------------:")
    #Load all user data to display global rankings
    folder = 'users'
    all_users = []
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
                all_users.append(json.load(f))
    #Sort users by points to display global rankings
    all_users.sort(key=lambda x: x['points'], reverse=True)
    for u in all_users:
        print(f"{u['rank']}. {u['name']} - {u['points']} points")

