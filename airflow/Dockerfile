FROM python:3.7

ARG AIRFLOW_VERSION=2.3.4
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

RUN pip install apache-airflow==${AIRFLOW_VERSION}
#RUN pip install SQLAlchemy==1.3.23

RUN mkdir /get_your_flat

COPY airflow_cfg/ /get_your_flat/airflow_cfg/
COPY airflow_cfg/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

RUN chmod +x /get_your_flat/airflow_cfg/run.sh

EXPOSE 8080

ENTRYPOINT ["/get_your_flat/airflow_cfg/run.sh"]