#!/bin/bash
#sudo docker run --rm -p 5432:5432 -p 5672:5672 -p 5671:5671 -p 15672:15672 --name inf qio0/rmq_psql /bin/bash ./start.sh &
#sleep 2m
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

