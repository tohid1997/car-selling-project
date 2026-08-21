from flask import Blueprint, request, render_template, redirect, url_for, session
from app.services.auth_service import authenticate_user
from app.services.auth_service import (
    authenticate_user,
    register_user
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = authenticate_user(username, password)

        if user:
            session.permanent = True
            session["loggedin"] = True
            session["username"] = user[1]

            return redirect(url_for("main.home"))

        error = "نام کاربری یا رمز عبور شما اشتباه است!"
        return render_template("login.html", error=error)

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)

    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "loggedin" in session and session["username"] == "tohid":

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            register_user(username, password)

            return redirect(url_for("main.home"))

        return render_template("register.html")

    return redirect(url_for("auth.login"))