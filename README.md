# Py Quiz Game

An interactive **Python basics quiz** with account registration, login, difficulty levels, a timed challenge, shuffled questions, responsive UI, and saved scores.

## Live demo

**Play here:** [https://py-quiz-game.onrender.com](https://py-quiz-game.onrender.com)

> Free Render tier may take a few seconds to wake up if the app was idle.

## Features

- **Create account / Sign in** with live username & password validation
- **Welcome home page** with how-to-play instructions
- **Difficulty levels:** Easy · Medium · Hard · Mixed
- **10 multiple-choice questions** per attempt (drawn from a larger bank)
- **Shuffled questions and answer options** every attempt
- **5-minute countdown timer** (auto-submits when time runs out)
- **Progress bar** and question step indicators
- **Results screen** with score percentage and per-question review
- **Responsive layout** — works on phone, tablet, and laptop (about **90% width** on larger screens)
- **Passwords hashed** and stored in **SQLite**
- Scores saved per user (including difficulty)
- **Deployed on** [Render](https://render.com) (Gunicorn + `render.yaml`)

## How to run (local)

```bash
cd py-quiz-game1
git pull
pip install -r requirements.txt
python3 app.py
```

Open in your browser:

**http://127.0.0.1:5000**

> Use the Flask URL above — do not open the HTML files directly in the browser.

### Flow

1. **Create account** or **Sign in**
2. Land on the **Home** page (welcome + instructions)
3. Choose a difficulty: **Easy**, **Medium**, **Hard**, or **Mixed**
4. Click **Start quiz**
5. Answer 10 questions within 5 minutes
6. View your score and correct answers

## Difficulty levels

| Level | What you get |
|-------|----------------|
| **Easy** | 10 questions from the easy bank |
| **Medium** | 10 questions from the medium bank |
| **Hard** | 10 questions from the hard bank |
| **Mixed** | 4 easy + 3 medium + 3 hard |

Each level’s bank has **12** questions. Every attempt picks **10** at random and shuffles both question order and A/B/C option order.

## Validation rules

| Field | Rules |
|-------|--------|
| **Username** | At least 8 characters, no spaces, no digits |
| **Password** | At least 7 characters, at least one digit, at least one uppercase letter |

## Project structure

```
py-quiz-game1/
├── app.py                  # Flask backend (auth, routes, quiz API, DB)
├── questions.py            # Question bank by difficulty level
├── index.html              # Create account / Sign in
├── home.html               # Welcome page, difficulty picker, how to play
├── quiz.html               # Timed quiz + results
├── username_password.py    # Original CLI validator (optional)
├── requirements.txt        # flask, flask-cors, gunicorn
├── render.yaml             # Render.com deploy config
├── users.db                # Created automatically on first run (local)
├── docs/
│   └── SPECIFICATION.md    # Project specification
└── README.md
```

## Main routes

| Route | Description |
|-------|-------------|
| `GET /` | Sign in / register page |
| `POST /auth/register` | Create account → redirect to `/home` |
| `POST /auth/login` | Sign in → redirect to `/home` |
| `GET /home` | Welcome + difficulty selection (login required) |
| `GET /quiz?level=easy` | Quiz challenge (login required; `level` = easy, medium, hard, or mixed) |

## API overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/me` | Current logged-in user |
| `POST` | `/api/logout` | End session |
| `GET` | `/api/quiz/questions?level=` | 10 shuffled questions for the level (no answers) |
| `POST` | `/api/quiz/submit` | Grade answers against the session answer key, save score |
| `GET` | `/api/quiz/my-scores` | Your past scores (includes difficulty) |

## How scoring works

1. Starting a quiz builds a random attempt and stores the **answer key in the server session** (not sent to the browser).
2. On submit, answers are checked against that key.
3. Score, total, percentage, and **difficulty** are saved in SQLite.

## Deploy on Render

**Live URL:** [https://py-quiz-game.onrender.com](https://py-quiz-game.onrender.com)

This repo includes a **`render.yaml`** for a free web service:

- **Build:** `pip install -r requirements.txt`
- **Start:** `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Env vars:** `SECRET_KEY` (auto), `COOKIE_SECURE=1`, `FLASK_DEBUG=0`

### Deploy steps (summary)

1. Push this repo to GitHub.
2. In [Render](https://dashboard.render.com), create a new **Web Service** from the repo (or use Blueprint with `render.yaml`).
3. Wait for the deploy to finish, then open the public URL.

### Production notes

- On the **free tier**, the disk is **ephemeral**: `users.db` can be reset when the instance restarts. For lasting data, use a managed database later.
- Free services may **spin down** after idle time; the first request after that can be slow.
- Do not commit a real `users.db` with production passwords.

## Responsive UI

| Screen | Layout |
|--------|--------|
| **Phone** | Full width with side padding |
| **Tablet / laptop / desktop** | Content uses about **90% of the viewport width** |

After pulling UI changes, **hard-refresh** the browser (`Ctrl+Shift+R` / `Cmd+Shift+R`) so old CSS is not cached.

## Notes

- Local: use **http://127.0.0.1:5000** (Flask), not opening HTML files as `file://`.
- `users.db` is created on first run.
- Questions live in `questions.py` — edit that file to add or change questions.
- This is a learning/demo project — not production-hardened security.
