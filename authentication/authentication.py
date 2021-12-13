from flask import Blueprint, render_template, request, session, redirect

from database import mongo, bcrypt
from .utility import register_user, fetch_user

authentication_blueprint = Blueprint('authentication', __name__,
                                     template_folder='templates',
                                     static_folder='static')


@authentication_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("authentication/register.html")

    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    if fetch_user(mongo, email):
        return render_template("authentication/register.html", error="Username is taken.")
    elif password != confirm:
        return render_template("authentication/register.html", error="Password is not matching.")
    else:
        password = bcrypt.generate_password_hash(password)
        msg = register_user(mongo, email, password)
        return render_template("authentication/register.html", msg=msg)


@authentication_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("authentication/login.html")

    email = request.form.get('email')
    password = request.form.get('password')

    if not fetch_user(mongo, email):  # if user does not exist then None will toggled to True using not
        return render_template("authentication/login.html", error="Username does not exist.")
    else:
        user_details = fetch_user(mongo, email)
        hashed_password = user_details["password"]
        if bcrypt.check_password_hash(hashed_password, password):
            session["email"] = email
            return redirect("/user")
        else:
            return render_template("authentication/login.html", error="Wrong Password.")


@authentication_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    session["email"] = None     # assigned to None
    session.clear()
    return redirect("/login")


@authentication_blueprint.route("/forgotPassword", methods=["POST"])
def forgot_password():
    session["email"] = None     # assigned to None
    return redirect("authentication/forgot_password.html")


@authentication_blueprint.route("/")
def home_page():
    temp = "HOME"
    return render_template("authentication/auth.html", temp=temp)
