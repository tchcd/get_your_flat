FROM python:3.7

ARG AIRFLOW_VERSION=2.3.4
ARG AIRFLOW_USER_HOME=usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

RUN pip install apache-airflow==${AIRFLOW_VERSION}
RUN pip install apache-airflow-providers-ssh

COPY airflow_cfg/run.sh ${AIRFLOW_HOME}/run.sh
COPY airflow_cfg/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY airflow_cfg/ssh_conn ${AIRFLOW_HOME}/.ssh/ssh_conn

RUN pip install psycopg2

RUN chmod +x /usr/local/airflow/run.sh

EXPOSE 8080

ENTRYPOINT ["/usr/local/airflow/run.sh"]