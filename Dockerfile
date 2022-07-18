FROM python:3.8-slim-buster
WORKDIR /Bifrost
RUN apt-get update
RUN apt-get install wget -y
RUN apt-get install git -y
RUN wget https://go.dev/dl/go1.18.1.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.18.1.linux-amd64.tar.gz 
COPY . .
RUN pip3 install -r requirements.txt
WORKDIR /Bifrost/src/agent/
RUN /usr/local/go/bin/go build
WORKDIR /Bifrost/src/c2/
RUN rm -rf migrations/
RUN python3 -m flask db init
RUN python3 -m flask db migrate -m "initial migration."
RUN python3 -m flask db upgrade
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
