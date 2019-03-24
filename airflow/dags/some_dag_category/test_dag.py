from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import timedelta, datetime

from settings import environment

default_args = {
  "owner": "data",
  "depends_on_past": False,
  "start_date": datetime(2019, 3, 13),
  "end_date": datetime.today(),
  "email": ["email@example.com"],
  "email_on_failure": True,
  "email_on_retry": False,
  "retries": 1,
  "retry_delay": timedelta(minutes=5),
}


with DAG("test_dag", schedule_interval='@daily', default_args=default_args) as dag:
    test_task = DockerOperator(
      image="task-worker:latest",
      network_mode="airflow_net",
      command="python3 tasks/test.py",  
      task_id="test",
      environment=environment,
      dag=dag)
    
    test_task