from datetime import datetime, timedelta

from airflow.decorators import dag, task

import pandas as pd
import sys

#include

sys.path.append("/usr/local/airflow/include")

default_args ={
    'owner': 'Rahul yadav',
    'depends_on_past': False,
    'start_date': datetime(2026,4,25),
    'retries':1,
    'retry_delay': timedelta(minutes=1),
    'catchup': False,
    'schedule': '@weekly',
}

@dag(
    default_args=default_args,
    description="Sales Forecast Trainig DAG",
    tags=['ml','training','sale_forecast','sales'],
)

def sales_forecast_training():

    @task()
    def extract_date_task():
        from utils.data_generator import RealisticSalesDataGenerator

        data_output_dir='/tmp/sales_data'

        generator = RealisticSalesDataGenerator(
            start_date="2022-02-22",
            end_date="2025-08-09",
        )

        print("Generating realistic sales data...")
        file_paths=generator.generate_sales_data(output_dir=data_output_dir)