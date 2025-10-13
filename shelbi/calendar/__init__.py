from flask import Blueprint

# define the blueprint object named "bp"
bp = Blueprint(
    "calendar",
    __name__,
    template_folder="../templates/calendar",
    static_folder="../static"
)

# import routes so they attach to bp
from shelbi.calendar import routes
