with open('user.json', 'r', encoding='utf-8') as f:
    user = json.load(f)
with open('user_review.json', 'r', encoding='utf-8') as f:
    user_review = json.load(f)
#ranking system feature
rank = 0
points = 0

#different users split
if user['name'] != {user['name']}:
    rank = 0 #New users start at rank 0
    points = 0 #New users start with 0 points
def calculate_rank():
    user['points'] = points
    user['rank'] = rank
    words_learned = len(user['reviews'])
    points = words_learned * 10 #Each word learned gives 10 points
    if user['streak']['current'] >= 7: #Bonus points for maintaining a streak of 7 or more days
        points += 50
    elif user['points'] > user['points']: 
        rank += 1 #Increase rank if points exceed other users
        print(f"Congratulations! You've been promoted to Rank {rank}! Keep up the great work!🔥")
        print(f"Your points is now: {user['points']}")
    else:
        print(f"Your current rank is: {rank}. Keep learning to climb the ranks!🔥")
        print(f"Your points is now: {user['points']}")

#Calling function
calculate_rank()