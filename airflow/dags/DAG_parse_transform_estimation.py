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
    'schedule_interval': '00 12 */2 * *',
}
dag = DAG(
    'etl_and_estimation',
    default_args=default_args,
    catchup=False
)

ssh = SSHHook(ssh_conn_id='etl_conn')

keyfile = open(ssh.key_file, "r")
keystr = keyfile.read()
ssh.pkey = ssh._pkey_from_private_key(private_key=keystr, passphrase='tarantino')

t1 = SSHOperator(
    task_id='parser',
    ssh_hook=ssh,
    command='python /app/src/data_processing/avito_etl.py',
    dag=dag)

t2 = SSHOperator(
    task_id='transformation',
    ssh_hook=ssh,
    command='python /app/src/models_processing/transform_data.py',
    dag=dag)

t3 = SSHOperator(
    task_id='estimation',
    ssh_hook=ssh,
    command='python /app/src/models_processing/evaluate_new_items.py',
    dag=dag)


t1 >> t2 >> t3
