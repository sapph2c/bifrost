
```▄▄▄▄    ██▓  █████▒██▀███   ▒█████    ██████ ▄▄▄█████▓
▓█████▄ ▓██▒▓██   ▒▓██ ▒ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒
▒██▒ ▄██▒██▒▒████ ░▓██ ░▄█ ▒▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░
▒██░█▀  ░██░░▓█▒  ░▒██▀▀█▄  ▒██   ██░  ▒   ██▒░ ▓██▓ ░ 
░▓█  ▀█▓░██░░▒█░   ░██▓ ▒██▒░ ████▓▒░▒██████▒▒  ▒██▒ ░ 
░▒▓███▀▒░▓   ▒ ░   ░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   
▒░▒   ░  ▒ ░ ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░    
 ░    ░  ▒ ░ ░ ░     ░░   ░ ░ ░ ░ ▒  ░  ░  ░    ░      
 ░       ░            ░         ░ ░        ░           
      ░
```

Bifrost is a Flask app that allows communication between implants and a centralized command
and control server.

## How to get started:

### Server side:
Clone the repo
```
git clone https://github.com/AshleyNikr/Bifrost.git
```
Change into the server directory
```
cd Bifrost/server
```
Make sure the docker service is running
```
sudo systemctl restart docker.service
```
Start the docker container
```
sudo docker-compose up --force-recreate --build
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
