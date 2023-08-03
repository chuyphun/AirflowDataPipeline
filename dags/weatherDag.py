import json
#import os
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


def load_data(ds, **kwargs):
    """
    Process the json data, check data types and insert into the
    Postgres database.
    """

    pg_hook  = PostgresHook(postgres_conn_id="cwb_id")

    file_name = f'{datetime.now().date()}.json'
    tot_name = Path(__file__).parent/f'src/data/{file_name}'

    with open(tot_name, "r", encoding="utf-8") as f:
        general_weather = json.load(f)

    i = 0
    info_i = general_weather["records"]["location"][i]
    city = str(info_i["locationName"])
    weather = "##".join(
        d["parameter"]["parameterName"]
        for d in info_i["weatherElement"][0]["time"]
    )
    pops = [
        int(d["parameter"]["parameterName"])
        for d in info_i["weatherElement"][1]["time"]
    ]
    pop = sum(pops)/len(pops)

    min_temps = [
        int(d["parameter"]["parameterName"])
        for d in info_i["weatherElement"][2]["time"]
    ]
    min_temp = sum(min_temps)/len(min_temps)

    max_temps = [
        int(d["parameter"]["parameterName"])
        for d in info_i["weatherElement"][4]["time"]
    ]
    max_temp = sum(max_temps)/len(max_temps)

    todays_date = datetime.now().date()

    row = (city, weather, pop, min_temp, max_temp, todays_date)

    insert_cmd = """INSERT INTO cwb_general
                    (city, weather, pop, min_temp, max_temp, todays_date)
                    VALUES
                    (%s, %s, %s, %s, %s, %s);"""

    pg_hook.run(insert_cmd, parameters=row)


# Define the default dag arguments.
default_args = {
    "owner" : "phunc20",
    "depends_on_past": False,
    "email": "wucf20@gmail.com",
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 5,
    "retry_delay": timedelta(minutes=1),
}


# Define the dag, the start date and how frequently it runs.
# I chose the dag to run everday by using 1440 minutes.
dag = DAG(
    dag_id="weatherDag",
    default_args=default_args,
    start_date=datetime(2023,8,2),
    schedule=timedelta(days=1),
    template_searchpath=[Path.cwd()],
)

task1 = BashOperator(
    task_id="get_weather",
    bash_command=f'python {Path(__file__).parent}/src/getWeather.py',
    dag=dag,
)

task2 = BashOperator(
    task_id="make_table",
    bash_command=f'python {Path(__file__).parent}/src/makeTable.py',
    dag=dag,
)

task3 =  PythonOperator(
    task_id="transform_load",
    python_callable=load_data,
    dag=dag,
)

task1 >> task2 >> task3
# Equiv. to
#task2.set_upstream(task1)
#task3.set_upstream(task2)
