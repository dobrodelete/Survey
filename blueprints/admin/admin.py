import json

from flask import Blueprint, request, render_template, redirect, url_for, make_response

from models.User import User

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin.route("/", methods=["GET"])
def admin_panel():
    if "is_admin" in request.cookies:
        return render_template("admin/base.html", title="Админ панель")
    else:
        return redirect(url_for(".admin_login"), 301)


@admin.route("/data", methods=["GET"])
def admin_data():
    if "is_admin" in request.cookies:
        return render_template("admin/base.html", title="Админ панель")
    else:
        return redirect(url_for(".admin_login"), 301)

@admin.route("/login")
def admin_login():
    return render_template("admin/login.html", title="Авторизация")


@admin.route("/auth", methods=["POST"])
def admin_auth():
    if request.method == "POST":
        user = User()
        response = make_response(redirect(url_for(".admin_panel"), 301))
        if user.check_auth(request.form.get("username"), request.form.get("password")):
            response.set_cookie("is_admin", "True", max_age=50 * 60 * 24 * 30)
            return response
        return redirect(url_for(".admin_login"), 301)


@admin.route("/survey", methods=["GET"])
def admin_survey():
    if "is_admin" in request.cookies:
        with open("static/json/surveyv2.json", "r", encoding="utf-8") as file:
            survey = json.load(file)
        return render_template("admin/survey.html", title="Админ/Опросник", survey=survey)
    else:
        return redirect(url_for(".admin_login"), 301)
