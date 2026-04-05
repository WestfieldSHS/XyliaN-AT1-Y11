import datetime
from main import check_streak
from main import check_achievement, achievement, user, star_bar, show_achievements

#testing achievement feature
user["reviews"] = [{"word": "digital", "definition": "relating to computers and electronic technology"}]  # 1 review
user["streak"]["current"] = 3
user["streak"]["freeze_remaining"] = 0
print("Before adding review:")
show_achievements()
check_achievement(user, achievement)
print("After adding review:")
show_achievements()
#testing streak feature

last_date = "2024-10-01"
current = 5
longest = 9
name = "Xylia"

fake_date = datetime.date(2024, 10, 2)

print(check_streak(last_date, current, longest, name, fake_date))