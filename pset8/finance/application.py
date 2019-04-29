import os
import time

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    userId = session["user_id"]

    user = db.execute("SELECT username FROM users WHERE id=':userId'", userId=userId )

    print(user)

    #stocks = db.execute("SELECT DISTINCT stock_name FROM 'transactions' WHERE id = ':userId'", userId=userId)

    stockShares = db.execute('SELECT "symbol", sum("shares") FROM transactions WHERE id = :userId GROUP BY symbol', userId=userId)

    time.sleep(2)
    cash = db.execute("SELECT cash FROM users WHERE id=':userId'", userId=userId )

    print(stockShares)
    symbol_info = []

    index = 0

    for stock in stockShares:
        symbol_info.append(lookup(stock["symbol"]))
        index += 1

    if len(symbol_info) == 1:
            symbol_info[0]["shares"] = stockShares[0]['sum("shares")']


    index = 0
    elem = symbol_info[index]["symbol"]
    print(elem)
    for stock in stockShares:
            for sym in symbol_info:
                if stock["symbol"].lower() == sym["symbol"].lower():
                    print("match found")
                    sym["shares"] = stock['sum("shares")']

    print("check above this line")


    print (symbol_info)

    totalValue = 0

    for sym in symbol_info:
        print(sym)
        sym["total"] = sym["price"] * sym["shares"]
        sym["price"] = usd(sym["price"])
        totalValue = float(sym["total"]) + totalValue
        sym["total"] = float("{:.2f}".format(sym["total"]))

    cash = float("{:.2f}".format(cash[0]['cash']))

    print(cash)

    totalValue = totalValue + cash

    totalValue = float("{:.2f}".format(totalValue))

    print(totalValue)

    return render_template("index.html", user=user[0]["username"], stocks=symbol_info, cash=cash, totalValue=totalValue)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol or not shares:
            return render_template("buy.html", showAlert=True, message="symbol or shares not entered")
        if shares <= 0:
            return apology("please enter a value greater than 0 for shares")

    stockInfo = lookup(symbol)
    if stockInfo == None:
        return apology("Please enter valid stock")

    userId=session.get("user_id")

    userCash = db.execute("SELECT cash FROM 'users' WHERE id=':userId';", userId=userId )
    cash = userCash[0]["cash"]
    cost = float(stockInfo["price"] * shares)

    if float(cash) < cost:
        return render_template("buy.html", showAlert=True, message="you dont have enough money to buy this stock")

    db.execute("INSERT INTO 'transactions' ('symbol','shares', 'id') VALUES (:symbol,':shares', ':userId')", symbol=symbol, shares=shares, userId=userId )

    db.execute("UPDATE users SET cash = ':cash' WHERE id = ':userId'", cash = float(cash) - cost, userId = userId)

    return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/addCash", methods=["POST"])
def addCash():
    """ Add cash value to account """

    userId = session["user_id"]

    userCash = db.execute("SELECT cash FROM 'users' WHERE id=':userId';", userId=userId )
    cash = userCash[0]["cash"]

    addCash = request.form.get("cash")
    addCash = float(addCash)
    cash = float(cash)

    newCash = float("{:.2f}".format(cash)) + float("{:.2f}".format(addCash))

    db.execute("UPDATE users SET cash = ':cash' WHERE id = ':userId'", cash = newCash, userId = userId)

    return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    userId = session["user_id"]

    transactions = db.execute('SELECT * FROM "transactions" WHERE id = ":userId"', userId=userId)

    print(transactions)

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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

    if request.method == "GET":
        return render_template("quote.html")

    elif request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("No stock symbol provided")

        stockInfo = lookup(symbol)
        if stockInfo == None:
            return apology("MEEOW ! That stock doesn't exist !")

        print(stockInfo)

        price = usd(stockInfo['price'])
        company = stockInfo['name']
        return render_template("quoted.html", name=company, price=price, symbol=symbol)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        passwordRepeat = request.form.get("passwordRepeat")

        if not name or not password or not passwordRepeat:
            return apology("empty values cannot be accepted")

        if password != passwordRepeat:
            return apology("passwords do not match")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username = name)
        if len(rows) >= 1:
            return render_template("register.html", showAlert=True)

    # so far user does not exist
    password_hash = generate_password_hash(password)

    someId = db.execute("INSERT INTO 'users' ('id','username','hash') VALUES (NULL,:user,:password_hash)", user=name, password_hash=password_hash)

    return render_template("register.html", showAlert=True, message= "User successfully registered")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    userId = session["user_id"]

    if request.method == "GET":

        userId=session.get("user_id")

        options = db.execute("SELECT DISTINCT symbol FROM 'transactions' WHERE id=':userId'", userId=userId )

        for option in options:
            option['symbol'] = option['symbol'].upper()

        return render_template("sell.html", options = options)

    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    cash = db.execute('SELECT cash FROM "users" WHERE id = ":userId"', userId=userId)

    if not shares or not symbol:
        return apology("no symbol selected or shares entered")

    if int(shares) < 0:
        return apology("not a valid share number")

    sharesOwned = db.execute('SELECT symbol, sum("shares") FROM transactions WHERE id = ":userId" and symbol=:symbol GROUP BY symbol', userId=userId, symbol=symbol)

    print(sharesOwned)

    if int(shares) > int(sharesOwned[0]['sum("shares")']):
        return apology("meeow you dont have enough shares to sell")


    #update database with a negative transaction for stock
    db.execute('INSERT INTO "transactions" ("symbol","shares","id") VALUES (:symbol,-:shares, ":userId")', symbol=symbol, shares=shares, userId=userId)

    #update database with added cash value
    #get market value of stock. multiply by the number of shares and add to the existing cash amount

    stock_info = lookup(symbol)

    print(stock_info)

    cashAdd = float(stock_info['price']) * int(shares)

    totalCash = float(cash[0]['cash']) + cashAdd

    totalCash = float("{:.2f}".format(totalCash))

    print(totalCash)

    db.execute('UPDATE "users" SET cash=":totalCash" WHERE id = ":userId"', totalCash=totalCash, userId=userId)

    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
