from airflow import DAG
from airflow.operators.bash_operator import BashOperator
#from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


dag = DAG('parser_and_estimate', start_date=datetime(2022, 9, 9), schedule_interval='@daily')

t1 = BashOperator(task_id='start_parse', bash_command="http://localhost/src/data_processing/avito_etl.py", dag=dag)

t2 = BashOperator(task_id='start_estimate', bash_command="chmod +x http://localhost/src/data_processing/transform_data.py", dag=dag)


t1 >> t2