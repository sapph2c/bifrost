#sudo docker run -p 5000:5000 <id>
FROM python:3.8-slim-buster
WORKDIR /app
RUN apt-get update
RUN apt-get install wget -y
RUN apt-get install git -y
RUN wget https://go.dev/dl/go1.18.1.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.18.1.linux-amd64.tar.gz 
#RUN go version
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /app/implant/payloads
RUN /usr/local/go/bin/go build
WORKDIR /app/c2
RUN python3 db_create.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
