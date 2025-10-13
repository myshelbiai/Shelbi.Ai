from shelbi import app, db
from flask import render_template, jsonify, request, abort, redirect, url_for
from shelbi.models import User, Task
from sqlalchemy import text 
from werkzeug.utils import secure_filename
import os, time
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------- PAGES ----------
@app.route("/")
def home():
    return render_template("home.html", title="Shelbi Home")

@app.route("/tasks/ui")
def tasks_ui():
    # Simple UI page to interact without Postman/curl
    items = Task.query.order_by(Task.id).all()
    return render_template("tasks.html", title="Tasks", items=items)

# ---------- JSON API ----------
@app.route("/tasks")
def tasks_list():
    # Keep your original JSON list at /tasks
    items = [{"id": t.id, "title": t.title, "done": t.done} for t in Task.query.order_by(Task.id)]
    return jsonify(tasks=items)

@app.route("/api/tasks", methods=["POST"])
def task_create():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        abort(400, "title is required")
    t = Task(title=title, done=False)
    db.session.add(t)
    db.session.commit()
    return jsonify(id=t.id, title=t.title, done=t.done), 201

@app.route("/api/tasks/<int:task_id>/toggle", methods=["PATCH"])
def task_toggle(task_id):
    t = Task.query.get_or_404(task_id)
    t.done = not t.done
    db.session.commit()
    return jsonify(id=t.id, title=t.title, done=t.done)

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def task_delete(task_id):
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify(ok=True)


@app.route("/tasks/<int:task_id>")
def task_detail(task_id):
    t = Task.query.get_or_404(task_id)
    return render_template("task_detail.html", title=f"Task #{t.id}", task=t)

@app.route("/tasks/<int:task_id>/edit", methods=["POST"])
def task_edit(task_id):
    t = Task.query.get_or_404(task_id)
    title = (request.form.get("title") or "").strip()
    t.done = bool(request.form.get("done"))
    if title:
        t.title = title
    db.session.commit()
    return redirect(url_for("task_detail", task_id=t.id))

@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def task_delete_html(task_id):
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for("tasks_ui"))


@app.route("/api/tasks/<int:task_id>")
def task_get(task_id):
    t = Task.query.get_or_404(task_id)
    return jsonify(id=t.id, title=t.title, done=t.done)

@app.route("/tasks/<int:task_id>/upload", methods=["POST"])
def task_upload(task_id):
    t = Task.query.get_or_404(task_id)
    file = request.files.get("photo")
    if not file or file.filename == "":
        abort(400, "No file uploaded")
    if not allowed_file(file.filename):
        abort(400, "Unsupported file type")

    filename = f"task-{t.id}-{int(time.time())}-{secure_filename(file.filename)}"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    file.save(save_path)

    # store relative path under /static
    t.photo_path = f"uploads/{filename}"
    db.session.commit()
    return redirect(url_for("task_detail", task_id=t.id))

@app.route("/health")
def health():
    try:
        # simple DB round-trip
        db.session.execute(db.text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    return jsonify(status="ok", db=db_ok)


@app.route("/version")
def version():
    return jsonify(
        flask=flask.__version__,
        sqlalchemy=sqlalchemy.__version__,
    )


@app.route("/backup/db")
def backup_db():
    db_path = os.path.join(os.path.dirname(__file__), "shelbi.db")
    # __file__ is shelbi/routes.py; shelbi.db sits in the same folder as __init__.py, so we step to that folder:
    db_path = os.path.join(os.path.dirname(__file__), "shelbi.db")
    # If your DB path differs, you can hardcode: db_path = os.path.join(app.root_path, "shelbi", "shelbi.db")
    return send_file(db_path, as_attachment=True, download_name="shelbi.db")
