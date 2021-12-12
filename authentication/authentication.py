from flask import Blueprint, render_template

authentication_blueprint = Blueprint('authentication', __name__,
                                     template_folder='templates',
                                     static_folder='static')


@authentication_blueprint.route("/register")
def register():
    temp = "register"
    return render_template("authentication/auth.html", temp=temp)


@authentication_blueprint.route("/login")
def login():
    temp = "login"
    return render_template("authentication/auth.html", temp=temp)


@authentication_blueprint.route("/")
def home_page():
    temp = "HOME"
    return render_template("authentication/auth.html", temp=temp)
