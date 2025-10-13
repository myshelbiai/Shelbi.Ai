from . import bp
from flask import render_template, request, url_for
import calendar
from datetime import date

@bp.route("/")
def index():
    # read ?y=YYYY&m=MM or default to today
    today = date.today()
    year = int(request.args.get("y", today.year))
    month = int(request.args.get("m", today.month))

    # build a 6x7 grid (weeks) of days; 0 means 'pad' day
    cal = calendar.Calendar(firstweekday=0)  # 0 = Monday
    weeks = []
    week = []
    for d in cal.itermonthdays(year, month):
        week.append(d)
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        while len(week) < 7:
            week.append(0)
        weeks.append(week)

    # prev/next month links
    prev_y, prev_m = (year - 1, 12) if month == 1 else (year, month - 1)
    next_y, next_m = (year + 1, 1)  if month == 12 else (year, month + 1)

    return render_template(
        "calendar/index.html",
        title="Calendar",
        year=year,
        month=month,
        month_name=calendar.month_name[month],
        weeks=weeks,
        prev_link=url_for("calendar.index", y=prev_y, m=prev_m),
        next_link=url_for("calendar.index", y=next_y, m=next_m),
        today=today,
    )
