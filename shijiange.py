from flask import Blueprint
shijiange = Blueprint("shijiange", __name__)

@shijiange.route('/index')
def index():
    return "shijiange Blueprint!"