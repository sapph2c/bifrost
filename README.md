![Bifrost](docs/img/Bifrost.png)

[![GitHub license](https://img.shields.io/github/license/AshleyNikr/Bifrost)](https://github.com/AshleyNikr/Bifrost/blob/master/LICENSE)[![GitHub stars](https://img.shields.io/github/stars/AshleyNikr/Bifrost)](https://github.com/AshleyNikr/Bifrost/stargazers)[![Test coverage](docs/img/coverage.svg)]
## Basic Overview
**Bifrost** is a Flask app that allows communication between implants and a centralized command and control server.
## Getting Started:
### Server side:
Clone the repo
```bash
git clone https://github.com/AshleyNikr/Bifrost.git
```
Change into the server directory
```bash
cd Bifrost/server
```
Make sure the docker service is running
```bash
sudo systemctl restart docker.service
```
Start the docker container
```bash
sudo docker-compose up --force-recreate --build
```
Naviage to the local signup endpoint  
```
https://127.0.0.1:5000/signup
```
### Client side:
Run the implant on the agent
```
sudo ./implant
```
### Planned Features:
- Modularity
- Documentation
- Group commands
