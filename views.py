from flask import Blueprint
from flask import render_template
views = Blueprint("views", __name__)

@views.route("/test")
def test():
    return render_template("test/test.html")

@views.route("/servers")
def servers():
    return render_template("test/servers.html")