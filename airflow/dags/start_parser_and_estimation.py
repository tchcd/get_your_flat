pass
# from airflow import DAG
# #from airflow.operators.bash_operator import BashOperator
# from airflow.operators.python_operator import PythonOperator
# from datetime import datetime, timedelta
# from src.data_processing import avito_etl, transform_data
# from src.models_processing import evaluate_new_items
#
#
# dag = DAG('parser_and_estimate', start_date=datetime(2022, 9, 9), schedule_interval='@daily')
#
# t1 = PythonOperator(task_id='parse', python_callable=avito_etl, dag=dag)
# t2 = PythonOperator(task_id='transform', python_callable=transform_data, dag=dag)
# t3 = PythonOperator(task_id='evaluate', python_callable=evaluate_new_items, dag=dag)
#
# #t2 = BashOperator(task_id='start_estimate', bash_command="chmod +x /usr/local/airflow/src/data_processing/transform.sh ", dag=dag)
#
# t1 >> t2 >> t3
#
