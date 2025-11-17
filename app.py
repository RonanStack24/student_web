import sys

from db.dbhelper import *

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/")
def index():
    students = getall("students")
    return render_template("index.html", studentlist=students)

@app.route("/add_student", methods=["POST"])
def add_student():
    idno = request.form["idno"]
    lastname = request.form["lastname"]
    firstname = request.form["firstname"]
    course = request.form["course"]
    level = request.form["level"]

    existing = getrecord("students", idno=idno)
    if existing:
        updaterecord("students", idno=idno, lastname=lastname,
                     firstname=firstname, course=course, level=level)
    else:
        addrecord("students", idno=idno, lastname=lastname,
                  firstname=firstname, course=course, level=level)
    return redirect(url_for("index"))

@app.route("/delete_student/<idno>")
def delete_student(idno):
    deleterecord("students", idno=idno)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
