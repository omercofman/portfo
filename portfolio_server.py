from pprint import pprint as print
from flask import Flask, render_template, request, redirect
from datetime import datetime
import csv

app = Flask(__name__)

DATABASE_STRATEGY = "csv"


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


@app.route("/")
def my_home():
    return html_page("index.html")


def write_to_txt(contact):
    with open("./database.txt", "a") as database:
        database.write(
            f"""
        Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        Email: {contact['email']}
        Subject: {contact['subject']}
        Message: {contact['message']}
        """
        )


def write_to_csv(contact):
    with open("./database.csv", "a", newline="") as database:
        csv_writer = csv.writer(
            database,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        csv_writer.writerow(
            [
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                contact["email"],
                contact["subject"],
                contact["message"],
            ]
        )


def save_contact(contact, database_strategy=DATABASE_STRATEGY):
    database_types = {
        "txt": write_to_txt,
        "csv": write_to_csv,
    }
    return database_types[database_strategy](contact)


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            save_contact(data)
            return redirect("/thank_you.html")
        except:
            return "Did not save to database"
    return "Error sbmitting form"
