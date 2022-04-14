# ❄️ Bifrost ❄️

Bifrost is a Flask app that allows communication between implants and a centralized command
and control server.

## How to get started:

### Server side:

git clone https://github.com/AshleyNikr/Bifrost.git

cd Bifrost

pip install -r requirements.txt

python3 db_create.py

flask run --host=0.0.0.0

### Client side:

python3 implant.py

### Important

- Make sure to change the base url in the implant to the IP you're hosting
the server on

### Planned Features:

- Bot Authentication
- Https
- Modularity
- Documentation
- Group commands
- Remote hosting
- Easy deployment
- Nil goated
