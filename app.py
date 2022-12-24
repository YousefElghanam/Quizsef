import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""

    # Store user's balance
    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # Store shares
    shares = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])

    # To iterate over the list "stock"'s elements in jinja
    iter = range(len(shares))

    # A list that holds stocks' prices
    stock = []
    for i in range(len(shares)):
        stock.append(lookup(shares[i]["stock"])["price"])

    # Render index.html
    return render_template("index.html", balance=balance, stock=stock, packed=zip(shares, iter))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # If user inputs and submits Buy, POST
    if request.method == "POST":

        # Ensure symbol was submitted and exists
        if not request.form.get("symbol"):
            return apology("must provide stock's symbol")
        elif not lookup(request.form.get("symbol")):
            return apology("symbol doesn't exist")

        # Ensure shares are entered and is a positive integer
        if not request.form.get("shares"):
            return apology("must provide shares (a positive integer)")

        try:
            if int(request.form.get("shares")) < 1:
                return apology("must provide a positive integer")
        except (TypeError, ValueError):
            return apology("shares must be an integer number")
        # Store stock's info
        stock = lookup(request.form.get("symbol"))

        # Store user's balance
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Store shares
        symbol_shares = db.execute("SELECT amount FROM shares WHERE user_id = ? AND stock = ?", session["user_id"], stock["symbol"])

        # Ensure user's balance is sufficient
        if stock["price"] * float(request.form.get("shares")) > balance[0]["cash"]:
            return apology("your balance is insufficient")

        # If balance is sufficient

        # Add a new row in history table
        db.execute("INSERT INTO history(type, user_id, stock, stock_price, amount, total_price) VALUES('buy', ?, ?, ?, ?, ?)",
                   session["user_id"], stock["symbol"], stock["price"], request.form.get("shares"), stock["price"] * float(request.form.get("shares")))

        # Update user's balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   balance[0]["cash"] - stock["price"] * float(request.form.get("shares")), session["user_id"])

        # Add new row to shares table if there isn't one with user's id and stock's symbol
        if not db.execute("SELECT * FROM shares WHERE user_id = ? AND stock = ?", (session["user_id"]), stock["symbol"]):
            db.execute("INSERT INTO shares(user_id, stock, amount) VALUES(?, ?, ?)",
                       session["user_id"], stock["symbol"], request.form.get("shares"))

        # Edit shares table for current user and entered symbol
        else:
            db.execute("UPDATE shares SET amount = ? WHERE stock = ? AND user_id = ?",
                       int(request.form.get("shares")) + symbol_shares[0]["amount"], stock["symbol"], session["user_id"])

        # Redirect to home page
        return redirect("/")

    # If user visits Buy, GET
    else:
        return render_template("buy.html")


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # When user input and submit, POST
    if request.method == "POST":

        # Ensure stock symbol exists
        if not request.form.get("symbol"):
            return apology("must provide stock's symbol")

        # Ensure symbol exists
        if not lookup(request.form.get("symbol")):
            return apology("no stock exists with that symbol", 400)

        # Get symbol's stock price
        stock = lookup(request.form.get("symbol"))

        # Render quoted.html and pass price as price
        return render_template("quoted.html", stock=stock)

    # When user visit Quote, GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure username does not already exist
        elif len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) == 1:
            return apology("username already exists", 400)

        # Ensure password and confirmation ware submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Confirmation does not match Password", 400)

        # Add user to database
        db.execute("INSERT INTO 'users' ('username','hash') VALUES (?)",
                   (request.form.get("username"),
                    generate_password_hash(password=request.form.get("password"), method='pbkdf2:sha256', salt_length=8)))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # At submission
    if request.method == "POST":

        # Store shares of selected stock
        stocks_shares = db.execute("SELECT * FROM shares WHERE stock = ? AND user_id = ?",
                                   request.form.get("symbol"), session["user_id"])

        # Store user's balance
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Store stock's info
        stock = lookup(request.form.get("symbol"))

        # If no symbol was chosen
        if not request.form.get("symbol"):
            return apology("Must choose a stock's symbol")

        # If no shares were entered or entered 0
        try:
            if not request.form.get("shares") or int(request.form.get("shares")) < 1:
                return apology("Must enter a positive number of shares")

        except (TypeError, ValueError):
            return apology("shares must be an integer number")

        # If no shares are owned for chosen symbol
        if not stocks_shares:
            return apology("You don't have shares for that stock")

        # If not own enough shares
        elif int(request.form.get("shares")) > stocks_shares[0]["amount"]:
            return apology("You don't have that many shares")

        # If conditions are met

        # Update shares
        db.execute("UPDATE shares SET amount = ? WHERE user_id = ? AND stock = ?",
                   stocks_shares[0]["amount"] - int(request.form.get("shares")),
                   session["user_id"], stocks_shares[0]["stock"])

        # Update user's balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   balance[0]["cash"] + int(request.form.get("shares")) * lookup(request.form.get("symbol"))["price"],
                   session["user_id"])

        # Add a new row in history table
        db.execute("INSERT INTO history(type, user_id, stock, stock_price, amount, total_price) VALUES('sell', ?, ?, ?, ?, ?)",
                   session["user_id"], stock["symbol"], stock["price"], request.form.get("shares"), stock["price"] * float(request.form.get("shares")))

        # Delete rows with 0 shares
        db.execute("DELETE FROM shares WHERE amount = 0")

        # Redirect user to home page
        return redirect("/")

    # On visiting "/sell"
    else:
        # Store all owned shares
        shares = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])

        # Render sell.html
        return render_template("sell.html", shares=shares)


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
        return render_template("settings.html")