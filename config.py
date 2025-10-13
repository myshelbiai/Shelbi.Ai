import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLite file will live at: Shelbi.Ai\shelbi\shelbi.db
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'shelbi', 'shelbi.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "change-me"

# add near the bottom of config.py
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'shelbi', 'static', 'uploads')
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
