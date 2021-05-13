import json
import os
import tool_db
from flask import Blueprint
from flask import request
from flask import redirect
from flask import make_response
from flask import session
from werkzeug.utils import secure_filename
from flask import send_from_directory

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['get', 'post'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    sql = "select * from user where username = %s and password = %s"
    result = tool_db.updateByParameters(sql, (username, password))
    print(result)
    if result:
        session['username'] = username
        return redirect('/views/servers')
        # response = make_response(redirect("/views/servers"))
        # response.set_cookie('username',username,max_age=86400)
        # return response
    else:
        return redirect("/static/login.html")


@auth.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect("/static/login.html")
    # response = make_response(redirect("/static/login.html"))
    # response.delete_cookie('username')
    # return response
