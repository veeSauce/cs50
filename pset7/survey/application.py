import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request, url_for

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

students = []
x = 0



@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():



    name = request.form.get("Name")
    car = request.form.get("Car")
    male = request.form.get("male")
    female = request.form.get("female")

    if not name or not car:
        return render_template("error.html", message= name + " " + car)

    print(male)
    print(female)

    if not male and not female:

        return render_template("error.html", message= "no gender selected")

    if male:
        students.append(f"{name} drives a {car} and is a male")
    else:
        students.append(f"{name} drives a {car} and is a female")

    with open("survey.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "car"])
        global x
        if x == 0:
            writer.writeheader()
            x = x + 1
        writer.writerow({"name": name, "car": car})
    return redirect(url_for('get_sheet'))


@app.route("/sheet", methods=["GET"])
def get_sheet():

    with open("survey.csv", "r") as file:
        reader = csv.DictReader(file)
        users = list(reader)

        print(users)

    return render_template("registered.html", users=users)