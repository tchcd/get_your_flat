from airflow import DAG
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import timedelta, datetime


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@qu.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime.now() - timedelta(minutes=20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@weekly',
}
dag = DAG(
    'model_retraining_DAG',
    default_args=default_args,
    catchup=False
)

ssh = SSHHook(ssh_conn_id='model_retraining_conn')

keyfile = open(ssh.key_file, "r")
keystr = keyfile.read()
ssh.pkey = ssh._pkey_from_private_key(private_key=keystr, passphrase='tarantino')

retraining_model = SSHOperator(
    task_id='model_retraining_task',
    ssh_hook=ssh,
    command='python /app/src/models_processing/model_retraining.py',
    dag=dag)
