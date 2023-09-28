import json
import os
import shutil
import zipfile

from flask import Blueprint, request, render_template, redirect, url_for, make_response, session, current_app, \
    send_from_directory

from config import DB_NAME
from models.User import User

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = '/reports'

@admin.route("/", methods=["GET"])
def admin_panel():
    if "is_admin" in session:
        return render_template("admin/base.html", title="Админ панель")
    else:
        return redirect(url_for(".admin_login"), 301)


@admin.route("/login")
def admin_login():
    return render_template("admin/login.html", title="Авторизация")

@admin.route("/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for(".admin_login"))


@admin.route("/auth", methods=["POST"])
def admin_auth():
    if request.method == "POST":
        user = User()
        response = make_response(redirect(url_for(".admin_panel"), 301))
        if user.check_auth(request.form.get("username"), request.form.get("password")):
            session["is_admin"] = True
            return response
        return redirect(url_for(".admin_login"), 301)


@admin.route("/survey", methods=["GET"])
def admin_survey():
    if "is_admin" in session:
        with open("static/json/surveyv2.json", "r", encoding="utf-8") as file:
            survey = json.load(file)
        return render_template("admin/survey.html", title="Админ/Опросник", survey=survey)
    else:
        return redirect(url_for(".admin_login"), 301)


@admin.route("/user_data", methods=["GET"])
def admin_data():
    if "is_admin" in session:
        return render_template("admin/user_data.html", title="Админ панель")
    else:
        return redirect(url_for(".admin_login"), 301)


@admin.route("/download/<type>")
def download(type):
    if "is_admin" in session:
        uploads = os.getcwd() + UPLOAD_FOLDER
        print(uploads)
        os.path.normpath(uploads)
        if type == "json":
            shutil.make_archive('reports/json', 'zip', 'reports/json')
            return send_from_directory(uploads, "json.zip", as_attachment=True)
        elif type == "xlsx":
            shutil.make_archive('reports/xlsx', 'zip', f'reports/xlsx')
            return send_from_directory(uploads, "xlsx.zip", as_attachment=True)
        elif type == "database":
            return send_from_directory(os.getcwd(), DB_NAME, as_attachment=True)
    else:
        return redirect(url_for(".admin_login"), 301)


@admin.route("/statistics", methods=["GET"])
def admin_statistics():
    if "is_admin" in session:
        data = []
        return render_template("admin/statistics.html", title="Данные опрашиваемых", data=data);
    else:
        return redirect(url_for(".admin_login"), 301)

