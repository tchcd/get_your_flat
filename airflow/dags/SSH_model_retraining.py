#from airflow.contrib.operators.ssh_operator import SSHOperator
import airflow
from airflow import DAG
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import timedelta, datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime.now() - timedelta(minutes=20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval':'@daily',
}
dag = DAG(
    'ssh_model_retrainer',
    default_args=default_args,
    description='some description',
    catchup=False
)

ssh = SSHHook(ssh_conn_id='ssh_retrain')

keyfile = open(ssh.key_file, "r")
keystr = keyfile.read()
ssh.pkey = ssh._pkey_from_private_key(private_key=keystr, passphrase='lololo')

ssh_retrain = SSHOperator(
    task_id='ssh_model_retraining',
    ssh_hook=ssh,
    #command='docker exec -ti app python /app/src/data_processing/pypy.py', #'get_your_flat/src/models_processing/test.sh', # arg1 arg2',
    command='ls -l',
    dag=dag)
