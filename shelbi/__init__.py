from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the db object ONCE (not bound to app yet)
db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object("config")

# Bind db to this app
db.init_app(app)

# Register blueprints
from shelbi.calendar import bp as calendar_bp
app.register_blueprint(calendar_bp, url_prefix="/calendar")

# Import after app/db exist
from shelbi import routes, models
