#!/bin/bash

airflow db init
sleep 10
airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
airflow webserver -p 8080
sleep 10
airflow scheduler

