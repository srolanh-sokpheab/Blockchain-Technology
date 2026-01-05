from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "dev-change-me"  # Required for flash messages

DB_PATH = "identity.db"

# --- Database Utilities ---
def get_db():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionary-like objects
    return conn

def init_db():
    """Initialize the database and create table if not exists."""
    Path(DB_PATH).touch(exist_ok=True)
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        conn.commit()

# Initialize database on startup
init_db()

# --- Routes ---

# Route 1: Home & Registration Form
@app.route("/", methods=["GET", "POST"])
def register():
    """
    GET: Show the registration form.
    POST: Insert new user into the database.
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()

        if not name or not email:
            flash("Name and Email are required.", "warning")
            return redirect(url_for("register"))

        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (name, email)
                )
                conn.commit()
            flash("Identity registered successfully!", "success")
            return redirect(url_for("list_users"))
        except sqlite3.IntegrityError:
            flash("Email already exists. Please use another email.", "danger")
            return redirect(url_for("register"))

    return render_template("form.html")

# Route 2: List All Users
@app.route("/users")
def list_users():
    """Display all registered users."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, name, email FROM users ORDER BY id DESC"
        ).fetchall()
    return render_template("users.html", users=rows)

# Route 3: Update User
@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Update user details."""
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()

    if not name or not email:
        flash("Name and Email are required.", "warning")
        return redirect(url_for("get_user", user_id=user_id))

    with get_db() as conn:
        conn.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, email, user_id)
        )
        conn.commit()
    flash("User updated successfully.", "info")
    return redirect(url_for("list_users"))

# Route 4: Delete User
@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user by ID."""
    with get_db() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
    flash("User deleted successfully.", "info")
    return redirect(url_for("list_users"))

if __name__ == "__main__":
    app.run(debug=True)