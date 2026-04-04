import datetime
from main import check_streak

#testing streak feature

last_date = "2024-10-01"
current = 5
longest = 9
name = "Xylia"

fake_date = datetime.date(2024, 10, 2)

print(check_streak(last_date, current, longest, name, fake_date))