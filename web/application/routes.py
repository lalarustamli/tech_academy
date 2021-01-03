from flask import render_template, request, json, Response, redirect, flash
from .models import User, Course, Enrollment
from .forms import LoginForm, RegisterForm
from . import app, db


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are logged in!","success")
            return redirect("/index")
        else:
            flash("Sorry mate","danger")
    return render_template("login.html", form=form, login=True)


@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        print("USER_ID" + str(user_id))
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user_s = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user_s.set_password(password)
        user_s.save()

        flash("You are successfully registered!", "success")
        return redirect("/index")
    else:
        print("NOT")
    return render_template("register.html", title="Register", form=form, register=True)


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
