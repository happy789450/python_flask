import datetime
import requests
from flask import request
from flask import Flask
from flask import render_template
from rice import rice
from views import views
from sersers import servers
from auth import auth
from flask import redirect
from flask import session
from deploy import deploy

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'
app.permanent_session_lifetime=datetime.timedelta(minutes=60)
app.register_blueprint(rice, url_prefix="/rice")
app.register_blueprint(views, url_prefix="/views")
app.register_blueprint(servers, url_prefix="/servers")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(deploy, url_prefix="/deploy")

@app.route('/')
def index():
    return render_template("test/index.html")


@app.before_request
def before_request():
    if request.path == "/static/login.html" or request.path == "/auth/login" or request.path.endswith(
            ".js") or request.path.endswith(".css"):
        pass
    else:
        # username = request.cookies.get('username')
        username = session.get('username')
        if not username:
            return redirect('/static/login.html')


@app.route('/user2')
def hello_user2():
    return render_template("test/user2.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5600')
