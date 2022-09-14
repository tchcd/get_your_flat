pass
# from airflow import DAG
# #from airflow.operators.bash_operator import BashOperator
# from airflow.operators.python_operator import PythonOperator
# from src.models_processing import model_retraining
# from datetime import datetime, timedelta
#
#
# dag = DAG('model_retraining', start_date=datetime(2022, 9, 9), schedule_interval='@daily')
#
# #t1 = BashOperator(task_id='start_retraining', bash_command="${AIRFLOW_HOME}/src/model_retraining.py ", dag=dag)
# t1 = PythonOperator(task_id='start_parse', python_callable=model_retraining, dag=dag)
#
# t1
# #t2