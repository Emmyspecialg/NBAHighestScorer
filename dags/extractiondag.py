#importing request to get info from api, pandas is used for data modeling 
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator 
from airflow.models.dag import DAG 
import requests
import pandas as pd
import json
from datetime import datetime 

#when the '22-'23 season started 
#date = "2022-10-18"


date = "{{ ds }}"

def api_extraction(date):
    test = requests.get(f"https://www.balldontlie.io/api/v1/stats?dates[]={date}&per_page=100")
    #print(test.json()) -- shows the data thats extracted from API 
    #creating our own model with variables 
    df = pd.DataFrame(test.json()["data"])
    df.to_csv("testdata.csv")
    ids = df.player.apply(lambda x: x["id"])
    first_name = df.player.apply(lambda x: x["first_name"])
    last_name = df.player.apply(lambda x: x["last_name"])
    points = df.pts

    nbascores = pd.DataFrame(
        columns=["id", "first_name", "last_name", "points"],
    data=zip(ids, first_name, last_name, points),
    )

    #creates csv table of data from the date listed above 
    nbascores.to_csv(f"scores_{date}.csv")
    print(nbascores)
    return nbascores.to_json()



with DAG(dag_id="GameScoreExtraction", start_date=datetime(2022, 10, 18), schedule_interval="@daily") as dag:
    extraction_operator=PythonOperator(python_callable=api_extraction, task_id="scorers", op_kwargs={"date":"{{ ds }}"})
    show_scores = BashOperator(task_id="show_scorers", bash_command="pwd")
    extraction_operator >> show_scores


#f"cat scores_{date}.csv"