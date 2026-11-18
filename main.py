import sqlite3
import pandas as pd
from extract import extract_jobs
from transform import transform_jobs
from load import log_progress, load_to_excel, load_to_parquet, load_to_db


def run_pipeline():
    # 1. Project configurations (links and output file names)
    url = "https://remoteok.com"
    excel_path = "remote_data_jobs.xlsx"
    parquet_path = "remote_data_jobs.parquet"
    db_name = "RemoteJobs.db"
    table_name = "Data_Jobs"

    log_progress("ETL pipeline started.")

    # 2. Extract
    raw_df = extract_jobs(url)
    log_progress(f"Extraction complete: {len(raw_df)} jobs collected.")
    print(f"Job openings found on the website:", len(raw_df))

    # 3. Transform
    clean_df = transform_jobs(raw_df)
    log_progress(f"Transformation complete: {len(clean_df)} unique jobs cleaned.")

    # 4. Load
    load_to_excel(clean_df, excel_path)
    load_to_parquet(clean_df, parquet_path)
    load_to_db(clean_df, db_name, table_name)
    log_progress("Data successfully saved to Excel, Parquet, and SQLite.")

    # 5. Business SQL Queries
    with sqlite3.connect(db_name) as conn:
        query_1 = f"SELECT COUNT(*) AS Total_Jobs FROM {table_name}"
        query_2 = f"SELECT Job_Title, Company, Salary FROM {table_name} WHERE Salary_Disclosed = 'Yes' LIMIT 5"

        print("\n--- Total Jobs Collected ---")
        print(pd.read_sql(query_1, conn))

        print("\n--- Sample Jobs with Disclosed Salary ---")
        print(pd.read_sql(query_2, conn))

    log_progress("ETL pipeline finished successfully.")


if __name__ == "__main__":
    run_pipeline()