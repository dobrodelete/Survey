import json
import os.path

from flask import Blueprint, jsonify, send_file, send_from_directory, current_app

api = Blueprint("api", __name__)



@api.route("/get_iogv", methods=["GET"])
def get_iogv():
    with open("static/json/list_iogv.json", "r", encoding="utf-8") as file:
        iogv = json.load(file)

    return jsonify(iogv)