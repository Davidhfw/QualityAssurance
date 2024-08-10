import time

from flask import Flask, request
from apitest.api.framework.excepts import *
from apitest.api.framework.auth import create_jwt, secure
from apitest.api.framework.data_gen import *
from apitest.api.framework.validators import *
from apitest.sql.sql_executor import DBExecutor

app = Flask(__name__)
db = DBExecutor('localhost', 'apitest', 'root', 'test@123456')


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return ClientParameterFailed(msg="request body should not be null")
    if 'username' not in data or 'password' not in data:
        return ClientParameterFailed(msg="required parameters 'username' or 'password' missed")
    if data['username'] == "" or data['password'] == "":
        return ClientParameterFailed(msg="'username' or 'password' should not be null")
    payload = {'username': data['username'], 'password': data['password']}
    token = create_jwt(payload)
    return HttpOk(data=token, msg="Create Token Successfully")


@app.route('/CreateCluster', methods=['POST'])
def create_cluster():

    # 获取请求头中的Authorization
    auth_token = request.headers.get('Authorization')
    # 验证token是否合法
    secure(auth_token)
    data = request.json

    # 判断请求体是否为空
    if not data:
        return ClientParameterFailed(msg="request body should not be null")
    # 判断请求体中必填字段是否缺失
    if 'name' not in data or 'version' not in data or 'cni_plugin' not in data:
        return ClientParameterFailed(msg="required parameter 'name' or 'version' or 'cni_plugin' missed")
    name = data['name']
    version = data['version']
    cni_plugin = data['cni_plugin']
    # 检查所有输入参数类型是否合法
    if not isinstance(name, str):
        return ClientParameterFailed(msg="name instance type is not str, please check input again")
    if not validate_cluster_name(name):
        return ClientParameterFailed(msg="name value is invalid, please check input again")

    if not isinstance(version, str):
        return ClientParameterFailed(msg="version instance type is not str, please check input again")
    if version not in ["1.24", "1.26", "1.28"]:
        return ClientParameterFailed(msg="version value is invalid, please check input again")

    if not isinstance(cni_plugin, str):
        return ClientParameterFailed(msg="parameter 'cni_plugin' type not string, please check input again")

    if cni_plugin not in ["flannel", "k8s-cni", "calico"]:
        return ClientParameterFailed(msg="parameter 'cni_plugin' value is invalid, please check input again")

    if 'desc' in data and not isinstance(data['desc'], str):
        return ClientParameterFailed(msg="parameter 'desc' type not string, please check input again")
    if 'delete_protection' in data and not isinstance(data['delete_protection'], int):
        return ClientParameterFailed(msg="parameter 'delete_protection' type not string, please check input again")

    cluster_id = ""
    desc = ""
    delete_protection = 0
    # 更新其他非必填字段
    if 'desc' in data:
        desc = data['desc']
    if 'delete_protection' in data:
        delete_protection = data['delete_protection']
    try:
        status_phase = "Creating"
        status_condition_type = "Progressing"
        cluster_id = _create_cluster(name, desc, version, cni_plugin, delete_protection, status_phase,
                                     status_condition_type)
        return HttpOk(msg=cluster_id)
    except Exception as e:
        raise e
    finally:
        time.sleep(0.5)
        status_phase = "Running"
        status_condition_type = "Ok"
        _ = _update_cluster_by_status(cluster_id=cluster_id, **{"status_phase": status_phase, "status_condition_type": status_condition_type})


@app.route('/UpdateCluster', methods=['PUT'])
def update_cluster():
    # 获取请求头中的Authorization
    auth_token = request.headers.get('Authorization')
    # 验证token是否合法
    secure(auth_token)

    data = request.json

    # 判断请求体是否为空
    if not data:
        return ClientParameterFailed(msg="request body should not be null")
    cluster_id = ""
    desc = ""
    delete_protection = 0
    name = ""
    # 判断请求体中必填字段是否缺失
    if 'cluster_id' not in data:
        return ClientParameterFailed(msg="required parameter 'cluster_id' missed")
    else:
        cluster_id = data['cluster_id']

    # 检查输入参数类型是否合法
    if 'name' in data:
        if not isinstance(data['name'], str) or validate_cluster_name(data['name']):
            return ClientParameterFailed(msg="parameter 'name' type not str or invalid, please check it again")
        else:
            name = data['name']

    else:
        name = None

    if 'delete_protection' in data:
        if not isinstance(data['delete_protection'], int) or data['delete_protection'] not in [0, 1]:
            return ClientParameterFailed(msg="parameter 'delete_protection' type not int or invalid, please check it again")
        else:
            delete_protection = data['delete_protection']
    else:
        delete_protection = None

    if 'desc' in data:
        if not isinstance(data['desc'], str) or validate_cluster_desc(desc):
            return ClientParameterFailed(msg="parameter 'desc' type not str or invalid, please check it again")
        else:
            desc = data['desc']
    else:
        desc = None

    # 集群更新
    try:
        cluster_id = _update_cluster(cluster_id, name, desc, delete_protection)
        return HttpOk(msg=cluster_id)
    except Exception as e:
        return ServerErrorInternalServerError(msg=str(e))
    finally:
        db.close()


@app.route('/DescribeClusters', methods=['GET'])
def describe_cluster():
    # 获取请求头中的Authorization
    auth_token = request.headers.get('Authorization')
    # 验证token是否合法
    secure(auth_token)

    data = request.json

    # 判断请求体是否为空
    if not data:
        return ClientParameterFailed(msg="request body should not be null")
    cluster_id = ""
    desc = ""
    delete_protection = 0
    name = ""
    # 判断请求体中必填字段是否缺失
    if 'cluster_id' not in data:
        return ClientParameterFailed(msg="required parameter 'cluster_id' missed")
    else:
        cluster_id = data['cluster_id']

    # 检查输入参数类型是否合法
    if 'name' in data:
        if not isinstance(data['name'], str) or validate_cluster_name(data['name']):
            return ClientParameterFailed(msg="parameter 'name' type not str or invalid, please check it again")
        else:
            name = data['name']

    else:
        name = None

    if 'delete_protection' in data:
        if not isinstance(data['delete_protection'], int) or data['delete_protection'] not in [0, 1]:
            return ClientParameterFailed(
                msg="parameter 'delete_protection' type not int or invalid, please check it again")
        else:
            delete_protection = data['delete_protection']
    else:
        delete_protection = None

    if 'desc' in data:
        if not isinstance(data['desc'], str) or validate_cluster_desc(data['name']):
            return ClientParameterFailed(msg="parameter 'desc' type not str or invalid, please check it again")
        else:
            desc = data['desc']
    else:
        desc = None

    # 处理查询逻辑
    try:
        result = _describe_cluster(cluster_id, name, desc, delete_protection)
        return HttpOk(msg=cluster_id, data=result)
    except Exception as e:
        return ServerErrorInternalServerError(msg=str(e))

@app.route('/DeleteCluster', methods=['DELETE'])
def delete_cluster():
    # 获取请求头中的Authorization
    auth_token = request.headers.get('Authorization')
    # 验证token是否合法
    secure(auth_token)

    data = request.json
    cluster_id = ""
    name = ""
    # 判断请求体中必填字段是否缺失
    if 'cluster_id' not in data:
        return ClientParameterFailed(msg="required parameter 'cluster_id' missed")
    else:
        cluster_id = data['cluster_id']

    # 检查输入参数类型是否合法
    if 'name' in data:
        if not isinstance(data['name'], str) or validate_cluster_name(data['name']):
            return ClientParameterFailed(msg="parameter 'name' type not str or invalid, please check it again")
        else:
            name = data['name']

    else:
        name = None

    if 'delete_protection' in data:
        if not isinstance(data['delete_protection'], int) or data['delete_protection'] not in [0, 1]:
            return ClientParameterFailed(
                msg="parameter 'delete_protection' type not int or invalid, please check it again")
        else:
            delete_protection = data['delete_protection']
    else:
        delete_protection = None

    if delete_protection == 1:
        return ServerErrorInternalServerError(msg="Cluster set not deleted")
    # 处理查询逻辑
    try:
        _ = _delete_cluster(cluster_id, name)
        return HttpOk(msg=f"delete_cluster {cluster_id} successfully")
    except Exception as e:
        return ServerErrorInternalServerError(msg=str(e))


def _create_cluster(name, desc, version, cni_plugin, delete_protection, status_phase, status_condition_type):
    try:
        db.connect()
        cluster_id = generate_random_string("cc", 10)
        create_query_new = "INSERT INTO cluster (cluster_id, name, description, version, cni_plugin, delete_protection, status_phase, status_condition_type) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        create_data = (cluster_id, name, desc, version, cni_plugin, delete_protection, status_phase, status_condition_type)
        db.insert_sql(create_query_new, create_data)
    except Exception as e:
        raise e
    finally:
        db.close()

    return cluster_id


def _describe_cluster(cluster_id, name, desc, delete_protection):
    try:
        db.connect()
        select_query = ""
        data = ()
        if cluster_id and not name and not desc and not delete_protection:
            select_query = "select * from cluster where cluster_id = %s"
            data = (cluster_id,)
        elif not cluster_id and name and not desc and not delete_protection:
            select_query = "select * from cluster where name = %s"
            data = (name,)
        elif not cluster_id and not name and desc and not delete_protection:
            select_query = "select * from cluster where description = %s"
            data = (desc,)
        elif not cluster_id and not name and not desc and delete_protection:
            select_query = "select * from cluster where delete_protection = %d"
            data = (delete_protection,)
        elif cluster_id and name and desc and delete_protection:
            select_query = "select * from cluster where cluster_id = %s and name = %s and description = %s and delete_protection = %d"
            data = (cluster_id, name, desc, delete_protection)

        result = db.describe_sql(select_query, data)
    except Exception as e:
        raise e
    finally:
        db.close()
    return result


def _delete_cluster(cluster_id, name):
    try:
        db.connect()
        delete_sql = ""
        data = ()
        if cluster_id and not name:
            delete_sql = "delete from cluster where cluster_id = %s"
            data = (cluster_id,)
        elif not cluster_id and name:
            delete_sql = "delete from cluster where name = %s"
            data = (name,)

        result = db.describe_sql(delete_sql, data)
    except Exception as e:
        raise e
    finally:
        db.close()
    return result


def _update_cluster(cluster_id, name, desc, delete_protection):
    try:
        db.connect()
        update_query = ""
        data = ()

        if cluster_id and name:
            update_query = "UPDATE cluster SET name = %s WHERE cluster_id = %s"
            data = (name, cluster_id)

        elif cluster_id and desc:
            update_query = "UPDATE cluster SET description = %s WHERE cluster_id = %s"
            data = (desc, cluster_id)

        elif cluster_id and delete_protection:
            update_query = "UPDATE cluster SET delete_protection = %d WHERE cluster_id = %s"
            data = (delete_protection, cluster_id)

        elif cluster_id and name and desc:
            update_query = "UPDATE cluster SET name = %s, description = %s WHERE cluster_id = %s"
            data = (name, desc, cluster_id)

        elif cluster_id and name and delete_protection:
            update_query = "UPDATE cluster SET name = %s, delete_protection = %s WHERE cluster_id = %s"
            data = (name, delete_protection, cluster_id)

        elif cluster_id and desc and delete_protection:
            update_query = "UPDATE cluster SET delete_protection = %d , description = %s WHERE cluster_id = %s"
            data = (desc, delete_protection, cluster_id)

        elif cluster_id and name and desc and delete_protection:
            update_query = "UPDATE cluster SET name = %s, description = %s,  delete_protection = %d WHERE cluster_id = %s"
            data = (name, desc, delete_protection, cluster_id)

        db.update_sql(update_query, data)
    except Exception as e:
        raise e
    finally:
        db.close()
    return cluster_id


def _update_cluster_by_status(cluster_id, **kwargs):
    try:
        db.connect()
        phase = kwargs.get("status_phase")
        condition_type = kwargs.get("status_condition_type")
        update_query = "UPDATE cluster SET status_phase = %s, status_condition_type = %s WHERE cluster_id = %s"
        data = (phase, condition_type, cluster_id)
        db.update_sql(update_query, data)
    except Exception as e:
        raise e
    finally:
        db.close()
    return cluster_id


if __name__ == "__main__":
    app.run(debug=True)
