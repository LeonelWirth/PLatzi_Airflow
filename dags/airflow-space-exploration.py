from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime


def _generate_platzi_data(**kwargs):
    import pandas as pd
    data = pd.DataFrame({"student": ["Maria Cruz", "Daniel Crema",
    "Elon Musk", "Karol Castrejon", "Freddy Vega"],
    "timestamp": [kwargs['logical_date'],
    kwargs['logical_date'], kwargs['logical_date'], kwargs['logical_date'],
    kwargs['logical_date']]})
    data.to_csv(f"/tmp/platzi_data_{kwargs['ds_nodash']}.csv",
    header=True)

def ver_data(**kwargs):
    print(f"ls /tmp && head /tmp/platzi_data_{kwargs['ds_nodash']}.csv")

with DAG(dag_id="airflow-space-exploration",
         description="",
         start_date=datetime(2024,8,1),
         schedule_interval="@daily") as dag:
    
    tarea1 = BashOperator(task_id="Autorizacion_NASA",
                          bash_command="sleep 20 && echo 'Confirmación de la NASA, pueden proceder' > /tmp/response_{{ds_nodash}}.txt")
    
    tarea2 = BashOperator(task_id="Lectura_Datos_NASA",
                          bash_command="ls /tmp && head /tmp/response_{{ds_nodash}}.txt")
    
    tarea3 = BashOperator(task_id="SpaceX_Data",
                          bash_command="curl -o /tmp/history.json -L'https://api.spacexdata.com/v4/history'")
    
    tarea4 = PythonOperator(task_id="Respuesta_Satelite",
                            python_callable=_generate_platzi_data)
    
    tarea5 = BashOperator(task_id="Ver_data",
                          bash_command="ls /tmp && head /tmp/platzi_data_{{ds_nodash}}.csv")
    
    email = EmailOperator(task_id='notify_analysts',
                    to = ['email@gmail.com', 'email@gmail.com'],
                    subject = "Notification Satellite Data",
                    html_content = "Notice to analysts, the data is available")    

    tarea1 >> tarea2 >> tarea3 >> tarea4 >> tarea5 >> email
