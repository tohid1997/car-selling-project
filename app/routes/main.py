from flask import Blueprint, render_template, redirect, url_for, session


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if "loggedin" in session:
        return render_template("home.html")

    return redirect(url_for("auth.login"))


@main_bp.route("/home")
def home():
    if "loggedin" in session:
        return render_template("home.html")

    return redirect(url_for("auth.login"))