FROM ubuntu
ADD . /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN python3 -V
RUN pip3 install -r requirements.txt
RUN chmod 777 start.sh
CMD ["./start.sh"]
