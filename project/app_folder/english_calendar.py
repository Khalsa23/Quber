import calendar
from datetime import datetime


current_month = datetime.now().month
current_year = datetime.now().year
my_cal = calendar.HTMLCalendar(firstweekday=6)
cal = my_cal.formatmonth(current_year, current_month)

