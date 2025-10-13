from . import bp
from flask import render_template

@bp.route("/")
def index():
    return render_template("calendar/index.html", title="Calendar")
