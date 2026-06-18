from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "ngo123"


# Database Connection
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create Database Table
def create_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


create_db()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# About Page
@app.route("/about")
def about():

    data = [
        0,
        "We help poor and needy people through education, healthcare and social welfare activities.",
        "Service, Transparency, Equality and Humanity.",
        "Food Donation, Education Support, Health Camps and Women Empowerment.",
        "Vikas, Rahul, Sneha and Priya"
    ]

    return render_template("about.html", data=data)


# Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                """
                INSERT INTO users(name,email,password)
                VALUES(?,?,?)
                """,
                (name, email, password)
            )

            conn.commit()

            return redirect("/login")

        except sqlite3.IntegrityError:
            return "Email already registered"

        finally:
            conn.close()

    return render_template("register.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            session["user"] = user["name"]
            return redirect("/dashboard")

        return "Wrong Email or Password"

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=session["user"]
    )


# Logout
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# Run App
if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )