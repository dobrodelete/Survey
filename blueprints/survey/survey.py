import json

from flask import Blueprint, request, redirect, url_for, render_template, make_response

from models.dbwriter import create_answer_dict, write_one_page_answer
from models.xlsxwriter import writedata

survey = Blueprint("survey", __name__, template_folder="templates", static_folder="static")


@survey.route("/")
def index():
    return redirect(url_for(".survey_login"), 301)


@survey.route("/login", methods=["POST", "GET"])
def survey_login():
    with open("static/json/iogvv2.json", "r", encoding="utf8") as file:
        iogv = json.load(file)
    return render_template("survey/login.html", title="Авторизация", iogv=iogv, js_true=True)


@survey.route("/instruction", methods=["GET", "POST"])
def survey_instruction():
    resp = make_response(render_template("survey/instruction.html", title="Инструкция"))
    if request.method == "POST":
        resp = make_response(render_template("survey/instruction.html", title="Инструкция"))
        resp.set_cookie("subdivision", request.values.get("subdivision"), max_age=50*60*24*30)
        resp.set_cookie("post", request.values.get("post"), max_age=50*60*24*30)
        resp.set_cookie("iogv", request.values.get("iogv"), max_age=50*60*24*30)
        return resp

    if request.method == "GET":
        if request.cookies.get("subdivision") is None or request.cookies.get("post") or request.cookies.get("iogv"):
            return redirect(url_for(".survey_login"), 301)


@survey.route("/start", methods=["GET", "POST"])
def survey_start():
    if request.method == "GET":
        if request.cookies.get("subdivision") is None or request.cookies.get("post") is None or request.cookies.get("iogv") is None:
            return redirect(url_for(".survey_login"), 301)

    if request.method == "POST":
        data = request.form.to_dict()
        data["iogv"] = request.cookies.get("iogv")
        data["post"] = request.cookies.get("post")
        data["subdivision"] = request.cookies.get("subdivision")
        answer = create_answer_dict(data)
        writedata(answer)
    with open("static/json/surveyv2.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    resp = make_response(render_template("survey/start.html", title="Опрос", data=data))
    return resp


@survey.route("/one_page", methods=["GET", "POST"])
def survey_one_page():
    if request.method == "POST":
        data = request.form.to_dict()
        answer = create_answer_dict(data)
        writedata(answer)
        write_one_page_answer(answer)


    with open("static/json/surveyv2.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    with open("static/json/iogvv2.json", "r", encoding="utf8") as file:
        iogv = json.load(file)
    return render_template("survey/one_page.html", title="Опрос", data=data, iogv=iogv, js_true=True)
