import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from utils import apology, login_required


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///qusef.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    
    # If user is teacher
    isteacher = db.execute("SELECT isteacher FROM users WHERE id = ?", session["user_id"])
    
    if isteacher[0]["isteacher"]:
        
        # Store rows of exams table
        exams = db.execute("SELECT * FROM exams WHERE user_id = ?", session["user_id"])
        
        return render_template("teacherindex.html", exams=exams, isteacher=isteacher)
    
    # If user is student
    else:
        return render_template("studentindex.html")
        

@app.route("/makeexam")
@login_required
def make_exam():
    """ make exam """


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Store rows of history table
    history = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        
        # Store input
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        usertype = request.form.get("usertype")
        
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure email was submitted
        elif not email:
            return apology("must provide email", 400)

        # Ensure username does not already exist
        elif len(db.execute("SELECT * FROM users WHERE username = ?", username)) == 1:
            return apology("username already exists", 400)

        elif len(db.execute("SELECT * FROM users WHERE email = ?", email)) == 1:
            return apology("email already exists", 400)

        # Ensure password and confirmation were submitted
        elif not password:
            return apology("must provide password", 400)

        elif not confirmation:
            return apology("must provide confirmation", 400)

        # Ensure password and confirmation match
        elif not password == confirmation:
            return apology("Confirmation does not match Password", 400)
        
        elif not usertype:
            return apology("please choose student or teacher")

        # Add user to database
        db.execute("INSERT INTO 'users' ('username','email','hash','isteacher') VALUES (?,?,?,?)",
                   (username), (email),
                    generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8), (1 if usertype=="teacher" else None))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """ Edit settings and change password """

    # At submission
    if request.method == "POST":

        # Query database for user id
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure old password was submitted
        if not request.form.get("old_password"):
            return apology("must provide old password", 403)

        # Ensure old password is correct
        elif not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("Wrong old password")

        # Ensure new password and its confirmation were submitted
        elif not request.form.get("new_password") or not request.form.get("confirmation"):
            return apology("must provide new password and confirmation", 403)

        # Ensure new and old passwords don't match
        elif request.form.get("new_password") == request.form.get("old_password"):
            return apology("Really ? Choose a NEW password, please")

        # Ensure password and confirmation match
        elif not request.form.get("new_password") == request.form.get("confirmation"):
            return apology("Confirmation does not match New Password", 403)

        # Update users' table with new password
        db.execute("UPDATE users SET hash = ? WHERE id = ? ",
                   generate_password_hash(password=request.form.get("new_password"), method='pbkdf2:sha256', salt_length=8),
                   session["user_id"])

        # Redirect to home page
        return redirect("/")

    # On visiting "/settings"
    else:
        # If user is teacher
        isteacher = db.execute("SELECT isteacher FROM users WHERE id = ?", session["user_id"])
        
        return render_template("settings.html", isteacher=isteacher)