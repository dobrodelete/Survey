from flask import Blueprint, render_template

site = Blueprint("site", __name__, template_folder="templates", static_folder="static")


@site.route("/")
def index():
    return render_template("site/index.html", title="Главная")


@site.route("/about")
def about():
    return render_template("site/about.html", title="О нас")


@site.route("/feedback")
def feedback():
    return render_template("site/feedback.html", title="Обратная связь")


@site.route("/privacy-policy")
def privacy_policy():
    return render_template("site/privacy-policy.html", title="Политика конфиденциальности")


@site.errorhandler(404)
def pageNotFound(error):
    return render_template("site/page404.html", title="Page not Found")