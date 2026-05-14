import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pripojeni

import secrets
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import mysql.connector.errors

app = Flask(__name__)
app.secret_key = "shieldbash_secret_2026_kladno"
app.permanent_session_lifetime = timedelta(days=7)

active_tokens = {}


def get_db():
    return mysql.connector.connect(
        host=pripojeni.HOST,
        user=pripojeni.USER,
        password=pripojeni.PASSWORD,
        database=pripojeni.DATABASE,
        use_pure=True,
    )


def _init_db():
    """Vytvor tabulky pri startu pokud neexistuji."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users67 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS highscores67 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                score INT NOT NULL,
                datum DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users67(id)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        pass  # DB neni dostupna - flask pojede dal, chyby se ukazi az pri pouziti

_init_db()


@app.route('/')
def home():
    return render_template("indexhome.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            error = "Zadej jméno i heslo."
        else:
            try:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users67 (username, password_hash) VALUES (%s, %s)",
                    (username, generate_password_hash(password))
                )
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('login'))
            except mysql.connector.errors.IntegrityError:
                error = "Toto jméno je již obsazeno."
            except mysql.connector.Error as e:
                error = f"Chyba databáze: {e}"
    return render_template("register.html", error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, password_hash FROM users67 WHERE username = %s", (username,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row and check_password_hash(row[1], password):
                session.permanent = True
                session['user_id'] = row[0]
                session['username'] = username
                return redirect(url_for('home'))
            else:
                error = "Nesprávné jméno nebo heslo."
        except mysql.connector.Error as e:
            error = f"Chyba databáze: {e}"
    return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/leaderboard')
def leaderboard():
    scores = []
    all_scores = {}
    error = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        # Top skore kazdeho hrace (1 radek na hrace)
        cursor.execute("""
            SELECT u.username, MAX(h.score) AS best, COUNT(h.id) AS games
            FROM highscores67 h
            JOIN users67 u ON h.user_id = u.id
            GROUP BY h.user_id, u.username
            ORDER BY best DESC
            LIMIT 10
        """)
        scores = cursor.fetchall()
        # Vsechny hry pro kazdeho hrace v TOP 10
        for username, _, _ in scores:
            cursor.execute("""
                SELECT h.score, h.datum
                FROM highscores67 h
                JOIN users67 u ON h.user_id = u.id
                WHERE u.username = %s
                ORDER BY h.score DESC
            """, (username,))
            all_scores[username] = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        error = f"Chyba databáze: {e}"
    return render_template("leaderboard.html", scores=scores, all_scores=all_scores, error=error)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '')
    password = data.get('password', '')
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users67 WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row and check_password_hash(row[1], password):
            token = secrets.token_hex(16)
            active_tokens[token] = row[0]
            return jsonify({"success": True, "token": token})
        return jsonify({"success": False, "error": "Nesprávné jméno nebo heslo."})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "error": f"Chyba databáze: {e}"})


@app.route('/api/score', methods=['POST'])
def api_score():
    data = request.get_json(silent=True) or {}
    token = data.get('token', '')
    score = data.get('score', 0)
    user_id = active_tokens.get(token)
    if not user_id:
        return jsonify({"success": False, "error": "Neplatný token."})
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO highscores67 (user_id, score) VALUES (%s, %s)",
            (user_id, score)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "error": f"Chyba databáze: {e}"})


if __name__ == '__main__':
    app.run()
