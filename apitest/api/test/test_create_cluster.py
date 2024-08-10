import http
import json
import os

import requests
import pytest
import allure

from apitest.api.framework.data_gen import *
from apitest.api.framework.auth import login


@allure.feature("CreateCluster API Tests")
class TestCreateCluster:
    api_url = "http://127.0.0.1:5000/CreateCluster"
    auth_test_data = [
        ("", "Positive"),
        ("", "Negative"),
        ("fadaf", "Negative"),
    ]

    @allure.feature("测试接口访问权限")
    @pytest.mark.parametrize("auth, flag", auth_test_data)
    def test_create_cluster_auth(self, auth, flag, api_url=api_url):

        if flag == "Positive":
            auth = login("abc", "pwd")
        headers = {"Authorization": auth}
        payload = {}

        res = requests.request("POST", api_url, headers=headers, data=payload)
        assert res.url == api_url, "request url not equal response url"
        if flag == "Positive":
            assert res.status_code == 200, "HTTP Code not equal to 200"
        else:
            assert res.status_code != 200, "HTTP Code not equal to 200"

    para_name_test_data = []
    name_valid_data = generate_valid_data(nums=10)
    new_name_valid_data = []
    for i, val in enumerate(name_valid_data):
        if is_valid(val):
            new_name_valid_data.append(val)
            para_name_test_data.append((val, "Valid"))
    name_invalid_data = generate_invalid_data()
    for i, val in enumerate(name_invalid_data):
        para_name_test_data.append((val, "Invalid"))
    name_wrong_type = generate_wrong_type_data("name")
    for i, val in enumerate(name_wrong_type):
        para_name_test_data.append((val, "WrongType"))

    @allure.feature("测试创建集群参数校验-名称")
    @pytest.mark.parametrize("name, flag", generate_name_data())
    def test_create_cluster_by_name(self, name, flag, api_url=api_url):

        # 获取正确的登录认证
        auth = login("root", "pwd")

        headers = {"Authorization": auth,
                   "Content-Type": "application/json"}

        # 组装Payload
        payload = {}
        try:
            payload = json.dumps({
                "name": name,
                "desc": "",
                "cni_plugin": "flannel",
                "version": "1.24",
                "delete_protection": 0,
            })
        except Exception as e:
            print(e)

        print("payload is ", payload)
        res = requests.post(api_url, headers=headers, data=payload)
        print("res json is ", res.json())
        assert res.url == api_url, "url not equal after request"
        if flag == "WrongType":
            with allure.step("验证错误的输入类型"):
                # 校验HTTP状态码
                assert res.status_code == 400, "HTTP Code not equal to 400"
                # 校验自定义错误msg
                assert "400" in res.text

        elif flag == "Invalid":
            with allure.step("验证不符合输入规则参数"):
                # 校验HTTP状态码
                assert res.status_code == 400, "HTTP Code not equal to 400"
                # 校验自定义错误msg
                assert "400" in res.text
        elif flag == "Valid":
            with allure.step("验证符合输入规则的参数"):
                # 校验HTTP状态码
                assert res.status_code == 200, "HTTP Code not equal to 200"


if __name__ == "__main__":
    pytest.main(['--alluredir', '../report', '--clean-alluredir'])
    #os.system('allure generate ../results -o ./report --clean')