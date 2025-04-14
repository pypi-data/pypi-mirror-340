import requests


def post(uri, data=None, json=None, headers=None, cookies=None, auth=None, timeout=None):
    requests.post(url=uri, data=data, json=json, headers=headers, cookies=cookies, auth=auth, timeout=timeout)

def get(uri, params=None, headers=None, cookies=None, auth=None, timeout=None):
    requests.get(url=uri, params=params, headers=headers, cookies=cookies, auth=auth, timeout=timeout)

def put(uri, data=None, json=None, headers=None, cookies=None, auth=None, timeout=None):
    requests.put(url=uri, data=data, json=json, headers=headers, cookies=cookies, auth=auth, timeout=timeout)

def delete(uri, headers=None, cookies=None, auth=None, timeout=None):
    requests.delete(url=uri, headers=headers, cookies=cookies, auth=auth, timeout=timeout)

def patch(uri, data=None, json=None, headers=None, cookies=None, auth=None, timeout=None):
    requests.patch(url=uri, data=data, json=json, headers=headers, cookies=cookies, auth=auth, timeout=timeout)

def head(uri, headers=None, cookies=None, auth=None, timeout=None):
    requests.head(url=uri, headers=headers, cookies=cookies, auth=auth, timeout=timeout)

def options(uri, headers=None, cookies=None, auth=None, timeout=None):
    requests.options(url=uri, headers=headers, cookies=cookies, auth=auth, timeout=timeout)

def request(method, uri, data=None, json=None, params=None, headers=None, cookies=None, auth=None, timeout=None):
    requests.request(method=method, url=uri, data=data, json=json, params=params, headers=headers, cookies=cookies, auth=auth, timeout=timeout)

