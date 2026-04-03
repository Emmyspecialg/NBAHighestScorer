# importing request to get info from api, pandas is used for data modeling
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models.dag import DAG
import os
import psycopg2
import requests
import pandas as pd
import json
from datetime import datetime

# when the '22-'23 season started
# date = "2022-10-18"


date = "{{ ds }}"


def api_extraction(date, **kwargs):
    test = requests.get(
        f"https://www.balldontlie.io/api/v1/stats?dates[]={date}&per_page=100"
    )
    # print(test.json()) -- shows the data thats extracted from API
    # creating our own model with variables
    df = pd.DataFrame(test.json()["data"])
    df.to_csv("testdata.csv")
    ids = df.player.apply(lambda x: x["id"])
    first_name = df.player.apply(lambda x: x["first_name"].replace("'", ""))
    last_name = df.player.apply(lambda x: x["last_name"].replace("'", ""))
    points = df.pts

    nbascores = pd.DataFrame(
        columns=["player_id", "first_name", "last_name", "points"],
        data=zip(ids, first_name, last_name, points),
    )

    # creates csv table of data from the date listed above
    nbascores.to_csv(f"scores_test.csv", index=False)
    nba_scores_json = nbascores.to_json(orient="records")
    print(nbascores)
    print(nba_scores_json)
    # print(nbascores.to_json(orient="records", compression='gzip', lines=True))
    # table_keys = ["player_id","first_name","last_name","scores"]
    # scores_data = [tuple(x) for x in nbascores.to_records(index=False)]
    # data = [dict(zip(table_keys, score)) for score in scores_data]
    # json_data = json.dumps(data, indent=4)
    # print(json_data)
    kwargs["ti"].xcom_push(key=f"scores", value=nba_scores_json)


with DAG(
    dag_id="GameScoreExtraction",
    start_date=datetime(2022, 10, 18),
    schedule_interval="@daily",
) as dag:
    extraction_operator = PythonOperator(
        python_callable=api_extraction,
        task_id="scorers",
        do_xcom_push=True,
        op_kwargs={"date": "{{ ds }}"},
    )
    # show_scores = BashOperator(task_id="show_scorers", bash_command="echo {{ ti.xcom_pull(task_ids='scorers', key=None) }}")

    # create_players_table = PostgresOperator(
    #     task_id="create_players_table",
    #     postgres_conn_id="postgres_localhost",
    #     sql="""sql/raw_infra/create_players_schema.sql""",
    # )
    # create_games_table = PostgresOperator(
    #     task_id="create_games_table",
    #     postgres_conn_id="postgres_localhost",
    #     sql="""sql/raw_infra/create_games_schema.sql""",
    # )
    create_scores_table = PostgresOperator(
        task_id="create_scores_table",
        postgres_conn_id="django-db-connection",
        sql="""sql/raw_infra/create_scores_schema.sql""",
    )

    def insert_scores(**kwargs):
        ti = kwargs["ti"]
        scores_json = ti.xcom_pull(task_ids="scorers", key="scores")
        scores = json.loads(scores_json)

        db_user = os.environ.get("POSTGRES_USER")
        db_password = os.environ.get("POSTGRES_PASSWORD")
        if not db_user or not db_password:
            raise RuntimeError("POSTGRES_USER and POSTGRES_PASSWORD environment variables must be set.")

        conn = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB", "django_db"),
            user=db_user,
            password=db_password,
            host=os.environ.get("POSTGRES_HOST", "django-db"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
        )
        try:
            cur = conn.cursor()
            try:
                insert_query = """
                    INSERT INTO score_table (player_id, first_name, last_name, points)
                    VALUES (%s, %s, %s, %s)
                """
                data = [
                    (row["player_id"], row["first_name"], row["last_name"], row["points"])
                    for row in scores
                ]
                cur.executemany(insert_query, data)
                conn.commit()
            finally:
                cur.close()
        finally:
            conn.close()

    insert_scores_operator = PythonOperator(
        task_id="insert_data",
        python_callable=insert_scores,
        provide_context=True,
    )

    extraction_operator >> create_scores_table >> insert_scores_operator


# f"cat scores_{date}.csv"
