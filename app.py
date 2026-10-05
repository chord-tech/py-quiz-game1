from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    session,
    redirect,
    flash,
    get_flashed_messages,
)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import timedelta
from functools import wraps
import random

from questions import BANK, LEVELS, QUIZ_SIZE, MIXED_SPLIT

app = Flask(__name__, static_folder=".", static_url_path="")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me-in-production")

app.config.update(
    SESSION_COOKIE_NAME="pyquiz_session",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
)

CORS(app, supports_credentials=True)

DB_PATH = "users.db"



def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(scores)")]
    if "difficulty" not in cols:
        conn.execute("ALTER TABLE scores ADD COLUMN difficulty TEXT DEFAULT 'easy'")
    conn.commit()
    conn.close()


def validate_username(username: str) -> tuple[bool, str]:
    if len(username) < 8:
        return False, "Username must be at least 8 characters long"
    if " " in username:
        return False, "Username must not contain spaces"
    if any(char.isdigit() for char in username):
        return False, "Username must not contain digits"
    return True, "Username is valid"


def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 7:
        return False, "Password must be at least 7 characters long"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    return True, "Password is valid"


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"success": False, "error": "Please log in first"}), 401
        return f(*args, **kwargs)
    return decorated


def start_session(user_id, username):
    session.clear()
    session.permanent = True
    session["user_id"] = int(user_id)
    session["username"] = username


@app.route("/")
def index():
    # Already logged in? Skip login screen
    if "user_id" in session:
        return redirect("/home")
    return send_from_directory(".", "index.html")


@app.route("/home")
def home_page():
    if "user_id" not in session:
        return redirect("/")
    return send_from_directory(".", "home.html")


@app.route("/quiz")
def quiz_page():
    if "user_id" not in session:
        return redirect("/")
    return send_from_directory(".", "quiz.html")


@app.route("/auth/register", methods=["POST"])
def auth_register():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    confirm = request.form.get("confirm") or ""

    ok, msg = validate_username(username)
    if not ok:
        flash(msg, "error")
        return redirect("/")

    ok, msg = validate_password(password)
    if not ok:
        flash(msg, "error")
        return redirect("/")

    if password != confirm:
        flash("Passwords do not match", "error")
        return redirect("/")

    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()
    if existing:
        conn.close()
        flash("Username already taken — try Sign in", "error")
        return redirect("/")

    password_hash = generate_password_hash(password)
    cursor = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash),
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    start_session(user_id, username)
    return redirect("/home")


@app.route("/auth/login", methods=["POST"])
def auth_login():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    if not username or not password:
        flash("Username and password required", "error")
        return redirect("/")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        flash("Invalid username or password", "error")
        return redirect("/")

    start_session(user["id"], user["username"])
    return redirect("/home")


@app.route("/api/flash", methods=["GET"])
def api_flash():
    messages = get_flashed_messages(with_categories=True)
    return jsonify({"messages": [{"category": c, "text": t} for c, t in messages]})


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    confirm = data.get("confirm") or ""

    ok, msg = validate_username(username)
    if not ok:
        return jsonify({"success": False, "error": msg}), 400

    ok, msg = validate_password(password)
    if not ok:
        return jsonify({"success": False, "error": msg}), 400

    if password != confirm:
        return jsonify({"success": False, "error": "Passwords do not match"}), 400

    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()
    if existing:
        conn.close()
        return jsonify({"success": False, "error": "Username already taken"}), 409

    password_hash = generate_password_hash(password)
    cursor = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash),
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    start_session(user_id, username)
    return jsonify({
        "success": True,
        "message": f"Welcome, {username}!",
        "username": username,
        "redirect": "/home",
    }), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"success": False, "error": "Username and password required"}), 400

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"success": False, "error": "Invalid username or password"}), 401

    start_session(user["id"], user["username"])
    return jsonify({
        "success": True,
        "message": f"Welcome back, {username}!",
        "username": username,
        "redirect": "/home",
    })


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out"})


@app.route("/api/me", methods=["GET"])
def me():
    if "user_id" not in session:
        return jsonify({"success": False, "logged_in": False}), 401
    return jsonify({
        "success": True,
        "logged_in": True,
        "username": session.get("username"),
        "user_id": session.get("user_id"),
    })


def build_attempt(level):
    """Pick 10 questions for the level, shuffle question and option order."""
    if level == "mixed":
        picked = []
        for lvl, n in MIXED_SPLIT.items():
            picked += random.sample([q for q in BANK if q["level"] == lvl], n)
    else:
        picked = random.sample([q for q in BANK if q["level"] == level], QUIZ_SIZE)
    random.shuffle(picked)

    client, key = [], []
    for q in picked:
        opts = [q["correct"]] + q["wrong"]
        random.shuffle(opts)
        letters = dict(zip("abc", opts))
        correct_letter = next(k for k, v in letters.items() if v == q["correct"])
        client.append({"id": q["id"], "question": q["question"], "options": letters})
        key.append({"id": q["id"], "answer": correct_letter})
    return client, key


@app.route("/api/quiz/questions", methods=["GET"])
@login_required
def get_questions():
    level = request.args.get("level", "easy").lower()
    if level not in LEVELS:
        level = "easy"
    client, key = build_attempt(level)
    session["quiz"] = {"level": level, "key": key}
    return jsonify({"success": True, "questions": client, "total": len(client), "level": level})


@app.route("/api/quiz/submit", methods=["POST"])
@login_required
def submit_quiz():
    attempt = session.get("quiz")
    if not attempt:
        return jsonify({"success": False, "error": "No active quiz. Please start again."}), 400
    data = request.get_json(silent=True) or {}
    answers = data.get("answers") or {}

    score = 0
    results = []
    for n, item in enumerate(attempt["key"], start=1):
        user_ans = str(answers.get(str(item["id"])) or "").lower().strip()
        correct = user_ans == item["answer"]
        if correct:
            score += 1
        results.append({
            "number": n,
            "id": item["id"],
            "correct": correct,
            "your_answer": user_ans or None,
            "correct_answer": item["answer"],
        })

    total = len(attempt["key"])
    percentage = round((score / total) * 100, 2) if total else 0
    level = attempt["level"]
    session.pop("quiz", None)

    conn = get_db()
    conn.execute(
        "INSERT INTO scores (user_id, score, total, percentage, difficulty) VALUES (?, ?, ?, ?, ?)",
        (session["user_id"], score, total, percentage, level),
    )
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "score": score,
        "total": total,
        "percentage": percentage,
        "level": level,
        "results": results,
        "message": f"You scored {score}/{total} ({percentage}%)",
    })


@app.route("/api/quiz/my-scores", methods=["GET"])
@login_required
def my_scores():
    conn = get_db()
    rows = conn.execute(
        """SELECT score, total, percentage, difficulty, created_at
           FROM scores WHERE user_id = ?
           ORDER BY created_at DESC LIMIT 10""",
        (session["user_id"],),
    ).fetchall()
    conn.close()
    scores = [
        {
            "score": r["score"],
            "total": r["total"],
            "percentage": r["percentage"],
            "difficulty": r["difficulty"],
            "created_at": r["created_at"],
        }
        for r in rows
    ]
    return jsonify({"success": True, "scores": scores})


if __name__ == "__main__":
    init_db()
    print("Database ready. Open http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
