import requests
import json
import os

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


def json_loads(data):
    return json.loads(data)

def json_loads_file(file):
    with open(file, 'r') as f:
        return json.load(f)

def json_dumps(data):
    return json.dumps(data)

def json_dumps_file(data, file):
    with open(file, 'w') as f:
        json.dump(data, f)

def json_loads_string(data):
    return json.loads(data)

def json_dumps_string(data):
    return json.dumps(data)

def json_loads_bytes(data):
    return json.loads(data.decode('utf-8'))

def json_dumps_bytes(data):
    return json.dumps(data).encode('utf-8')


# os

def os_path_exists(path):
    return os.path.exists(path)

def os_path_isfile(path):
    return os.path.isfile(path)

def os_path_isdir(path):
    return os.path.isdir(path)

def os_path_join(path, *paths):
    return os.path.join(path, *paths)

def os_path_split(path):
    return os.path.split(path)

def os_path_basename(path):
    return os.path.basename(path)

def os_path_dirname(path):  
    return os.path.dirname(path)

def os_path_abspath(path):
    return os.path.abspath(path)

def os_path_realpath(path):
    return os.path.realpath(path)

def os_path_normpath(path):
    return os.path.normpath(path)

def os_path_expanduser(path):
    return os.path.expanduser(path)

def os_path_expandvars(path):
    return os.path.expandvars(path)

def os_path_isabs(path):
    return os.path.isabs(path)

def os_path_ismount(path):
    return os.path.ismount(path)

def os_path_getsize(path):
    return os.path.getsize(path)

def os_path_getmtime(path):
    return os.path.getmtime(path)

def os_path_getatime(path):
    return os.path.getatime(path)

def os_path_getctime(path):
    return os.path.getctime(path)

def os_path_getuid(path):
    return os.path.getuid(path)

def os_path_getgid(path):
    return os.path.getgid(path)

def os_path_getowner(path):
    return os.path.getowner(path)

def os_path_getgroup(path):
    return os.path.getgroup(path)

def os_path_getmode(path):
    return os.path.getmode(path)

def os_path_getlink(path):
    return os.path.getlink(path)

def os_system(command):
    os.system(command)

def os_remove(path):
    os.remove(path)

def os_rmdir(path):
    os.rmdir(path)

def os_mkdir(path):
    os.mkdir(path)

def os_makedirs(path):
    os.makedirs(path)

def os_rename(src, dst):
    os.rename(src, dst)

def os_listdir(path):
    return os.listdir(path)

def os_walk(path):
    return os.walk(path)

def os_chdir(path):
    os.chdir(path)

def os_getcwd():
    return os.getcwd()

def os_getenv(key, default=None):
    return os.getenv(key, default)

def os_setenv(key, value):
    os.environ[key] = value

# shutil
import shutil

def shutil_copy(src, dst):
    shutil.copy(src, dst)

def shutil_copy2(src, dst):
    shutil.copy2(src, dst)

def shutil_copyfile(src, dst):
    shutil.copyfile(src, dst)

def shutil_copytree(src, dst):
    shutil.copytree(src, dst)   

def shutil_rmtree(path):
    shutil.rmtree(path)

def shutil_move(src, dst):
    shutil.move(src, dst)

def shutil_which(cmd):
    return shutil.which(cmd)

def shutil_disk_usage(path):
    return shutil.disk_usage(path)

