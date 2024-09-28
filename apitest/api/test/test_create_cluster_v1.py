import http
import json
import os

import requests
import pytest
import allure

from apitest.api.framework.data_gen import *
from apitest.api.framework.auth import login
from apitest.api.framework.data_gen.data_gen_v1 import generate_random_string, generate_name_data


@allure.epic("CreateCluster API Tests")
class TestCreateCluster:
    api_url = "http://127.0.0.1:5000/CreateCluster"


    @allure.feature("测试接口访问权限")
    def test_create_cluster_auth(self, api_url=api_url):

        auth_test_data = [
            ("", "Negative"),
            ("fadaf", "Negative"),
        ]
        for auth_data in auth_test_data:
            auth = auth_data[0]
            flag = auth_data[1]
            headers = {"Authorization": auth}
            name = generate_random_string("cc", 10)
            payload = json.dumps({
                    "name": name,
                    "desc": "",
                    "cni_plugin": "flannel",
                    "version": "1.24",
                    "delete_protection": 0,
                })

            res = requests.post(api_url, headers=headers, data=payload)
            assert res.url == api_url, "request url not equal response url"
            if flag == "Positive":
                assert res.status_code == 200, "HTTP Code not equal to 200"
            else:
                assert res.status_code != 200, "HTTP Code not equal to 200"


if __name__ == "__main__":
    pytest.main(['--alluredir', '../report', '--clean-alluredir'])
    #os.system('allure generate ../results -o ./report --clean')