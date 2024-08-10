import requests


class CreateCluster:
    def __init__(self, url):
        self.url = url

    def create_cluster(self, headers, payload, method, expected):
        res = requests.request(method, self.url, headers=headers, data=payload)

