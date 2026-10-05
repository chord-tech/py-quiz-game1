# Py Quiz Game — Project Specification

**Repository:** [chord-tech/py-quiz-game1](https://github.com/chord-tech/py-quiz-game1)  
**Version:** 1.0  
**Date:** October 2026  

---

## 1. Overview

Py Quiz Game is a full-stack web application that lets users create an account or sign in, read brief play instructions on a welcome page, then complete a **10-question Python basics quiz** under a **5-minute** time limit. Answers are scored on the server, results are shown immediately, and scores are stored per user in a local SQLite database.

### 1.1 Goals

- Provide a simple, polished learning tool for Python fundamentals.
- Enforce username/password validation rules at registration.
- Require authentication before accessing the quiz.
- Deliver a clear user flow: **Sign in → Home → Quiz → Results**.
- Persist users and scores without external services (SQLite).

### 1.2 Scope

**In scope:** web UI (login, home, quiz), Flask backend, session auth, validation, timer, scoring, and local database.

**Out of scope for this version:** production deployment hardening, email verification, OAuth, multiplayer, admin panel, and mobile native apps.

---

## 2. User Flow

1. User opens `http://127.0.0.1:5000` and sees the Create account / Sign in page.
2. After successful registration or login, the server redirects to `/home`.
3. Home greets the user by name and shows how-to-play instructions.
4. User clicks **Start quiz** and is taken to `/quiz`. The 5-minute timer starts.
5. User answers questions (navigate with Back / Continue), then submits (or time expires).
6. Results page shows score, percentage, time used, and correct answers per question.
7. User may Retry, return to Home, or Sign out.

---

## 3. Features

### 3.1 Authentication & validation

- Create account and Sign in modes on one page (segmented control).
- Live client-side rule checklists for username and password.
- Server-side validation and password hashing (Werkzeug).
- Session cookies (HTTP-only, SameSite=Lax) for logged-in state.
- Protected routes: `/home` and `/quiz` require an active session.

### 3.2 Home (welcome) page

- Personalized greeting with username.
- Four-step how-to-play guide.
- Summary facts: 10 questions, 5:00 timer, A/B/C choices.
- **Start quiz** and **Sign out** actions.

### 3.3 Quiz challenge

- 10 multiple-choice Python questions served without answers to the client.
- Progress bar, answered count, and step dots.
- 5-minute countdown; visual warn/danger states; auto-submit at 0:00.
- Previous / Next navigation; Submit on last question.
- Results: circular score indicator, message, time used, per-question review.

### 3.4 Data persistence

- SQLite database `users.db` created on first run.
- Tables:
  - `users` — id, username, password_hash, created_at
  - `scores` — id, user_id, score, total, percentage, created_at
- API for past scores: `GET /api/quiz/my-scores`

---

## 4. Validation Rules

| Field | Rules |
|-------|--------|
| **Username** | Minimum 8 characters; no spaces; no digits |
| **Password** | Minimum 7 characters; at least one digit; at least one uppercase letter |
| **Confirm password** | Must match password (registration only) |

---

## 5. Architecture

Flask serves static HTML pages and JSON APIs. Login/register use traditional form POST with server redirects for reliable session cookies. The quiz uses client-side JavaScript calling JSON APIs with the same session cookie.

### 5.1 Tech stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3, Flask, Flask-CORS |
| Auth / hashing | Flask sessions, Werkzeug password hashing |
| Database | SQLite (`users.db`) |
| Frontend | HTML5, CSS3, vanilla JavaScript |
| Fonts / UI | Inter (Google Fonts), dark neutral + indigo theme |

### 5.2 Project structure

```
py-quiz-game1/
├── app.py                  # Flask app: routes, validation, quiz API, DB
├── index.html              # Create account / Sign in
├── home.html               # Welcome + how to play
├── quiz.html               # Timed quiz + results
├── username_password.py    # Original CLI validator (legacy)
├── requirements.txt        # flask, flask-cors
├── users.db                # Auto-created at runtime
├── docs/
│   └── SPECIFICATION.md    # This document
└── README.md
```

---

## 6. Routes & API

### 6.1 Page routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Sign-in page; redirects to `/home` if already logged in |
| POST | `/auth/register` | Form register → session → redirect `/home` |
| POST | `/auth/login` | Form login → session → redirect `/home` |
| GET | `/home` | Welcome page (session required) |
| GET | `/quiz` | Quiz page (session required) |

### 6.2 JSON API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/me` | Current user or 401 |
| POST | `/api/logout` | Clear session |
| GET | `/api/flash` | Flash messages after form errors |
| GET | `/api/quiz/questions` | Questions without answers (auth) |
| POST | `/api/quiz/submit` | Grade answers, save score (auth) |
| GET | `/api/quiz/my-scores` | Past scores for current user (auth) |
| POST | `/api/register` | JSON register (API alternative) |
| POST | `/api/login` | JSON login (API alternative) |

---

## 7. Quiz Content

Questions are defined in `app.py` as a Python list. Each item has `id`, question text, options (`a`/`b`/`c`), and the correct answer key. The GET questions endpoint strips the answer field before sending data to the browser.

**Topics covered:** operator precedence, `def`, mutable types, `type([])`, floor division, `print`/`input`, loops, `len`, and lists vs tuples/strings.

**Scoring:** one point per correct choice; percentage = (score / 10) × 100, rounded to two decimals. A row is inserted into `scores` on every successful submit.

---

## 8. User Interface

- Dark theme: zinc neutrals (`#09090b` background) with indigo (`#6366f1`) primary accent.
- Typography: Inter for a clean product-style look.
- Login: segmented Create account / Sign in control, focus rings, validation checklists.
- Home: numbered steps, fact cards, primary Start quiz CTA.
- Quiz: thin progress track, step dots, selectable choice cards, timer with warn/danger states.
- Results: conic-gradient score ring, list of correct/incorrect per question.
- Responsive padding for narrow screens.

---

## 9. Installation & Run

```bash
git clone https://github.com/chord-tech/py-quiz-game1.git
cd py-quiz-game1
pip install -r requirements.txt
python3 app.py
```

Open **http://127.0.0.1:5000** in a browser. Do not open the HTML files as `file://` paths — the app must be served by Flask so sessions and APIs work.

**Dependencies:** `flask >= 3.0.0`, `flask-cors >= 4.0.0`.

---

## 10. Security Notes

- Passwords are hashed with Werkzeug (not stored in plain text).
- Session cookie is HTTP-only; SameSite=Lax for local development.
- Default `secret_key` is for development only — change via `SECRET_KEY` env in production.
- `SESSION_COOKIE_SECURE` should be `True` when serving over HTTPS.
- This is a learning/demo project, not production-hardened (no rate limiting, CSRF tokens on forms, etc.).
- Do not commit `users.db` if it contains real credentials.

---

## 11. Possible Future Enhancements

- Shuffle questions each attempt.
- Score history UI on the home page.
- More questions and difficulty levels.
- Review mode for wrong answers only.
- Leaderboard (optional).
- Deploy to a free host (Render, Railway, etc.).
- Light/dark theme toggle.

---

## 12. Document Control

| Item | Value |
|------|--------|
| Project name | Py Quiz Game |
| Repository | chord-tech/py-quiz-game1 |
| Primary language | Python (Flask) + HTML/CSS/JS |
| Specification version | 1.0 |
| Based on | Application state as of October 2026 commits |

This specification describes the system as implemented in the repository. It is intended for developers, reviewers, and portfolio documentation.
