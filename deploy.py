import tool_db
import datetime
import json
import subprocess
import threading
from flask import Blueprint
from flask import request

time1 = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
deploy_log = "deploy" + time1 + ".log"

deploy = Blueprint("deploy", __name__)


def shellRun(command):
    (status, output) = subprocess.getstatusoutput(command)
    return "status,output"


@deploy.route('/deploy_by_id')
def deploy_by_id():
    id = int(request.args.get('id'))
    sql = "select * from deploy where id = %s"
    result = tool_db.selectByParameters(sql, params=(id,))[0]
    runcommand = """/usr/local/bin/ansible -i {0} {1} -m {2} -a '{3}' -f {4} """.format(
        result['hosts_path'],
        result['hosts_pattern'],
        result['module'],
        result['args'],
        result['forks'],
    )
    command = """/usr/local/bin/ansible -i {0} {1} -m {2} -a '{3}' -f {4} >>static/logs/{5} 2>&1 ;printf "\n\t\t\t"  >>static/logs/{6} """.format(
        result['hosts_path'],
        result['hosts_pattern'],
        result['module'],
        result['args'],
        result['forks'],
        deploy_log, deploy_log)
    t1 = threading.Thread(target=shellRun, args=(command,))
    t1.start()
    return json.dumps({"command": runcommand, "log_name": deploy_log})


@deploy.route('/update', methods=['get', 'post'])
def update():
    info = request.get_data()
    info = json.loads(info)
    sql = 'replace into deploy (id,name,hosts_path,hosts_pattern,module,args,forks) values(%s,%s,%s,%s,%s,%s,%s);'
    params = (
        info['id'], info['name'], info['hosts_path'], info['hosts_pattern'], info['module'], info['args'],
        info['forks'])
    tool_db.updateByParameters(sql, params)
    return "success"


@deploy.route('/get_by_id')
def get_by_id():
    id = int(request.args.get('id'))
    sql = "select * from deploy where id = %s"
    result = tool_db.selectByParameters(sql, params=(id,))
    return json.dumps(result)


@deploy.route('/get_by_page', methods=['get', 'post'])
def get_by_page():
    info = request.get_data()
    info = json.loads(info)
    pagenow = info['pagenow']
    pagesize = info['pagesize']
    search = info['search']
    search = "%{0}%".format(search)
    sql = 'select * from deploy where name like %s  limit %s,%s'
    params = (search, (pagenow - 1) * pagesize, pagesize)
    result = tool_db.selectByParameters(sql, params=params)
    return json.dumps(result)
