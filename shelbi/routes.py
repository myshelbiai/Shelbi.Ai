from shelbi import app
from flask import render_template, jsonify
from shelbi.models import User, Task  # we'll add Task in a moment

@app.route("/")
def home():
    return render_template("home.html", title="Shelbi Home")

@app.route("/users")
def users():
    names = [u.name for u in User.query.all()]
    return jsonify(users=names)

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/tasks")
def tasks():
    items = [{"id": t.id, "title": t.title, "done": t.done} for t in Task.query.order_by(Task.id)]
    return jsonify(tasks=items)

@app.route("/about")
def about():
    return render_template("about.html", title="About")
