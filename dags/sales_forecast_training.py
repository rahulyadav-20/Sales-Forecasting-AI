from datetime import datetime, timedelta

from airflow.sdk import dag, task
import sys

sys.path.append("/opt/airflow/include")

default_args = {
    'owner': 'Rahul yadav',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


@dag(
    default_args=default_args,
    start_date=datetime(2026, 4, 25),
    schedule='@weekly',
    catchup=False,
    description="Sales Forecast Trainig DAG",
    tags=['ml', 'training', 'sale_forecast', 'sales'],
)
def sales_forecast_training():
    @task()
    def extract_data_task():
        from utils.data_generator import RealisticSalesDataGenerator

        data_output_dir = "/tmp/sales_data"
        generator = RealisticSalesDataGenerator(
            start_date="2021-01-01", end_date="2021-12-31"
        )
        print("Generating realistic sales data...")
        file_paths = generator.generate_sales_data(output_dir=data_output_dir)
        total_files = sum(len(paths) for paths in file_paths.values())
        print(f"Generated {total_files} files:")
        for data_type, paths in file_paths.items():
            print(f"  - {data_type}: {len(paths)} files")
        return {
            "data_output_dir": data_output_dir,
            "file_paths": file_paths,
            "total_files": total_files,
        }

    extract_data_task()


sales_forecast_training_dag = sales_forecast_training()
