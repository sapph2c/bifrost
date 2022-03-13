import subprocess
import requests
import psutil
import platform

base_url = 'http://127.0.0.1:5000'


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def register():
    # TODO finish gathering system information
    uname = platform.uname()
    # get os
    os = f"{uname.system} {uname.release}"
    # get host_name
    host_name = uname.node
    # get ip
    ip = requests.get('https://api.ipify.org').text
    # get system memory
    ram = get_size(psutil.virtual_memory().total)
    # set info in the requests json
    json = {
        'os': os,
        'host_name': host_name,
        'ip': ip,
        'ram': ram
    }
    response = requests.post(f"{base_url}/api/1.1/add_agent", json=json)
    print(response)


if __name__ == "__main__":
    register()