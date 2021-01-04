from flask import render_template, request, json, Response, redirect, flash, session, url_for
from .models import User, Course, Enrollment
from .forms import LoginForm, RegisterForm
from . import app, db


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET","POST"])
def login():
    if session.get('username'):
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            session['user_id']=user.user_id
            session['username']=user.first_name
            flash(f"{user.first_name}, you are logged in!","success")
            return redirect("/index")
        else:
            flash("Sorry mate","danger")
    return render_template("login.html", form=form, login=True)


@app.route("/register", methods=["GET","POST"])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")


    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
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

@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Resul 2021"):
    classes = Course.objects.order_by("courseID")
    return render_template("courses.html", courses=True, data=classes, term=term)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))
    CourseID = request.form.get('courseID')
    CourseTitle = request.form.get('title')
    user_id = session.get('user_id')
    if CourseID:
        if Enrollment.objects(user_id=user_id, courseID=CourseID):
            flash(f"You have already enrolled to {CourseTitle}")
            return redirect("/courses")
        else:
            Enrollment(user_id=user_id, courseID=CourseID).save()
            flash(f"You are enrolled! Congrats")
    term = request.form.get('term')
    data = list(User.objects.aggregate(*[
        {
            '$lookup': {
                'from': 'enrollment',
                'localField': 'user_id',
                'foreignField': 'user_id',
                'as': 'r1'
            }
        }, {
            '$unwind': {
                'path': '$r1',
                'includeArrayIndex': 'r1_id',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {
                'from': 'course',
                'localField': 'r1.courseID',
                'foreignField': 'courseID',
                'as': 'r2'
            }
        }, {
            '$unwind': {
                'path': '$r2',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$match': {
                'user_id': user_id
            }
        }, {
            '$sort': {
                'courseID': 1
            }
        }
    ]))
    print(data)

    return render_template("enrollment.html", enrollment=True, data=data)

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
