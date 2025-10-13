import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLite file will live at: Shelbi.Ai\shelbi\shelbi.db
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'shelbi', 'shelbi.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "change-me"
