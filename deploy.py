import tool_db
import tool_pass
import json
import subprocess
from flask import Blueprint
from flask import request

deploy = Blueprint("deploy", __name__)


@deploy.route('/deploy_by_id')
def deploy_by_id():
    id = int(request.args.get('id'))
    sql = "select * from deploy where id = %s"
    result = tool_db.selectByParameters(sql, params=(id,))[0]
    command = """/usr/local/bin/ansible -i {0} {1} -m {2} -a  '{3}' -f {4}""".format(result['hosts_path'], result['hosts_pattern'],
                                                                      result['module'], result['args'],
                                                                    result['forks'])
    (status,output)=subprocess.getstatusoutput(command)
    return output


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
    # print(search)
    sql = 'select * from deploy where name like %s  limit %s,%s'
    # print(sql)
    params = (search, (pagenow - 1) * pagesize, pagesize)
    # print(params)
    result = tool_db.selectByParameters(sql, params=params)
    return json.dumps(result)
