import sys
import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from db.dbhelper import *

app = Flask(__name__)

# Ensure upload folder exists
UPLOAD_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

@app.route("/upload-photo", methods=["POST"])
def upload_photo():
    if "photo" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["photo"]
    idno = request.form.get("idno")

    if not idno:
        return jsonify({"message": "IDNO is required"}), 400

    if file.filename == "":
        return jsonify({"message": "Empty filename"}), 400

    # Force image to use IDNO filename
    extension = file.filename.rsplit(".", 1)[-1]  # jpg/png/jpeg
    imagename = f"{idno}.jpg"  # convert everything to jpg

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], imagename)
    file.save(save_path)

    print("Saved file to:", save_path)

    return jsonify({
        "message": "Photo uploaded successfully!",
        "image_url": f"/static/images/{imagename}"
    })

if __name__ == "__main__":
    app.run(debug=True)
