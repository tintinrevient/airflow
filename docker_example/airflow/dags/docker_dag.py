import os
from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(
    dag_id="docker_dag",
    description="Get and rank the movie ratings",
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2019, 1, 5),
    schedule_interval="@daily"
) as dag:

    get_ratings = DockerOperator(
        task_id="get_ratings",
        image="tintinrevient/get-ratings",
        command=[
            "get",
            "--start_date",
            "{{ds}}",
            "--end_date",
            "{{next_ds}}",
            "--output_path",
            "/data/ratings/{{ds}}.json",
            "--username",
            os.environ["API_USER"],
            "--password",
            os.environ["API_PASSWORD"],
            "--host",
            os.environ["API_HOST"]
        ],
        network_mode="host",
        mounts=["/tmp/airflow/data:/data"]
    )

    rank_ratings = DockerOperator(
        task_id="rank_ratings",
        image="tintinrevient/rank-ratings",
        command=[
            "rank",
            "--input_path",
            "/data/ratings/{{ds}}.json",
            "--output_path",
            "/data/rankings/{{ds}}.csv"
        ],
        mounts=["/tmp/airflow/data:/data"]
    )

    get_ratings >> rank_ratings
