import requests
import pytest

from apitest.api.utils.utils import generate_random_string


class TestCreateCluster:
    def __init__(self, uri, api_name):
        self.uri = uri
        self.api_name = api_name
        self.url = self.uri + "/" + api_name


    def test_create_cluster_ok(self, name, desc, version, cni_plugin, delete_protection):

        payload = {
            "name": name,
            "desc": desc,
            "version": version,
            "cniPlugin": cni_plugin,
            "deleteProtection": delete_protection
        }

        headers = {}

        response = requests.request("POST", self.url, headers=headers, data=payload)
        assert response.url == self.url
        assert response.status_code == 200
        print(response.text)


if __name__ == "__main__":

    uri = "http://127.0.0.1:5000"
    api_name = "CreateCluster"

    cc = TestCreateCluster(uri=uri, api_name=api_name)
    name = generate_random_string("autotest", 10)
    desc = "faf"
    version = "1.24"
    cni_plugin = "flannel"
    delete_protection = 0
    cc.test_create_cluster_ok(name, desc, version, cni_plugin, delete_protection)