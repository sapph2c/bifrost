# ❄️ Bifrost ❄️

Bifrost is a Flask app that allows communication between implants and a centralized command
and control server.

## How to get started:

### Server side:
Clone the repo
```
git clone https://github.com/AshleyNikr/Bifrost.git
```
Change into the C2 directory
```
cd Bifrost
```
Install dependencies
```
pip install -r requirements.txt
```
Create the database
```
python3 db_create.py
```
Start the server
```
flask run --host=0.0.0.0
```
### Client side:
Run the implant on the agent
```
sudo ./implant
```
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
