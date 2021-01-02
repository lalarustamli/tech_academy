from flask import render_template, request, json, Response
from models import User, Course, Enrollment
from . import app, db


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
    return render_template("courses.html", courses=True, data=courseData['courseData'], term=term)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form.get('title')
    term = request.form.get('term')
    course = {
        "id": id,
        "title": title,
        "term": term
    }
    return render_template("enrollment.html", enrollment=True, data=course)

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    with open('/home/lala/Desktop/pers/Blog/web/application/templates/courses.json', 'r') as cs:
        courseData = json.load(cs)['courseData']
    if (idx==None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata),mimetype="application/json")



@app.route("/user")
def user():
    User(user_id=1,first_name="Ivan",last_name="Ivanich",email="iveniv",password="12345").save()
    users = User.objects.all()
    return render_template("user.html",users=users)
