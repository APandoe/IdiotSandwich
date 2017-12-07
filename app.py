from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import os
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import errormsg, login_required, lookup, scraper

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("postgres://hxhwhraafiphgj:3c315ee92c27124cf87245ed36165e820fbda34cf40ebdcda8dd0db5dbcae78e@ec2-54-235-123-153.compute-1.amazonaws.com:5432/d7rd8mp8rv5ifv"
)

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    """Show home page"""
    # if not os.environ.get("API_KEY"):
    #     raise RuntimeError("API_KEY not set")
    # return render_template("home.html", key=os.environ.get("API_KEY"))
    # IMPORTANT: API_KEY IS 8cd06460

    # User reached route simply via "/", displays mealtime options
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        print (request.form.get("meal"))

        # if not int(request.form.get("meal")):
            # return render_template("/home.html", meal = "no meal chosen")

        mealtime = request.form.get("meal")

        menu = scraper(mealtime)

    # Eventually want it to show:
        # TOP 5 popular items in dhall that day
        # TOP 5 popular dhall recipes that day
        # link to menu/dhall checklist

        # Display relevant information to user based off of mealtime option chosen
        if int(mealtime) == 0:
            return render_template("/hacks.html", menu = menu, meal = "BREKKIE", mealtime="0")
        if int(mealtime) == 1:
            return render_template("/hacks.html", menu = menu, meal = "LUNCH", mealtime="1")
        if int(mealtime) == 2:
            return render_template("/hacks.html", menu = menu, meal = "DINNER", mealtime="2")

    if request.method == "GET":
        return render_template("/home.html")


@app.route("/theusual")
@login_required
def theusual():
    """Show history of past recipes, liked food options (but only if those food items are available that day as well)"""

    # can also make it a get/post kinda thing
        # should involve some sort of interaction with dhall hacks

    # Display all data
    return render_template("/theusual.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return errormsg("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return errormsg("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return errormsg("invalid username and/or password", 403)

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


@app.route("/hacks", methods=["GET", "POST"])
@login_required
def hacks():
    """Get dining hall menu and allow user to choose ingredients."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        ingredients = request.form.get("ingredient")
        results = lookup(ingredients)

        return render_template("hacks.html", string = "postrequest")

    # User reach route via GET (clicking link)
    else:
        return render_template("hacks.html", string = "getrequest")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure password field completed
        if not request.form.get("password"):
            return errormsg("must input password", 400)

        # Ensure confirmation field completed
        if not request.form.get("confirmation"):
            return errormsg("must input confirmation", 400)

        # Ensure username field completed
        if not request.form.get("username"):
            return errormsg("must provide username", 400)

        # Ensure password and confirmation field completed
        if not request.form.get("password") == request.form.get("confirmation"):
            return errormsg("passwords must match", 400)

        # Create new rows with newUser's data
        newUser = db.execute("INSERT INTO users (username, hash) VALUES(:username, :passhash)",
                             username=request.form.get("username"), passhash=generate_password_hash(request.form.get("password")))

        print (newUser)

        # Ensure newUser is unique (id is primary key, cannot insert newUser with same id as other entry)
        if not newUser:
            return errormsg("username already in use", 400)

        # Save userid
        session["user_id"] = newUser

        # Send to home
        return render_template("/home.html")

    # User reach route via GET (clicking link)
    else:
        return render_template("/register.html")


@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    """Set dietary preferences"""

    # If method is POST retrieve data from user to send to home
    if request.method == "POST":

        return render_template("/preferences.html", string="postrequest")

    # if method is GET (show user available stocks)
    else:
        return render_template("/preferences.html", string="getrequest")


def errorhandler(e):
    """Handle error"""
    return errormsg(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
