from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import db, User
from app.forms import LoginForm, RegistrationForm

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    return redirect(url_for("main.login"))


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("main.login"))
        session["username"] = user.username
        return redirect(url_for("main.index"))
    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("main.index"))
