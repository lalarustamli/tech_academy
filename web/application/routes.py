import json
from flask import render_template

from . import app

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)

@app.route("/login")
def login():
    return render_template("login.html", login=True)

@app.route("/register")
def register():
    return render_template("register.html", register=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Resul 2021"):
    with open('/home/lala/Desktop/pers/Blog/web/application/templates/courses.json', 'r') as cs:
        courseData = json.load(cs)
    return render_template("courses.html", courses=True, courseData=courseData['courseData'], term=term)

