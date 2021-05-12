import json
import os
from flask import Blueprint
from flask import request
from werkzeug.utils import secure_filename
from flask import send_from_directory

rice = Blueprint("rice", __name__)


@rice.route('/index')
def index():
    return "rice Blueprint!"


@rice.route('/ajaxtest')
def ajaxtest():
    return "ajaxtest"


@rice.route('/ajaxget')
def ajaxget():
    server_name = request.args.get('server_name')
    server_ip = request.args.get('server_ip')
    return "server_name is: {0} ,server_ip is: {1}".format(server_name, server_ip)


@rice.route('/ajaxpost', methods=['get', 'post'])
def ajaxpost():
    info = request.get_data()
    info = json.loads(info)
    print(info)
    return info['username']
    # return "username is: {0} ,password is: {1}".format( username, password )


@rice.route('/upload', methods=["get", "post"])
def upload():
    servers = request.files.get("servers")
    filename = secure_filename(servers.filename)
    print(filename)
    servers.save('/tmp/{0}'.format(filename))
    return "upload success"


@rice.route('/download')
def download():
    # print(os.path.relpath(__file__))
    curses_dir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(curses_dir + "/static", "1.txt", as_attachment=True)


@rice.route('/get')
def hello_get():
    print(request.args)
    server_name = request.args.get("server_name")
    server_ip = request.args.get("server_ip")
    return "server_name is: {} server_ip is: {}".format(server_name, server_ip)


@rice.route('/post', methods=["get", "post"])
def hello_post():
    print(request.form)
    username = request.form.get("username")
    password = request.form.get("password")
    return "username is: {} password is: {}".format(username, password)
