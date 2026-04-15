from google.cloud import bigquery
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# GCP BigQuery Configuration
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
DATASET_ID = os.getenv('GCP_BIGQUERY_DATASET')
TABLE_ID = 'job_postings'  # Example table name

def load_job_postings_to_bigquery(csv_path):
    # Initialize BigQuery client
    client = bigquery.Client(project=PROJECT_ID)

    # Read CSV
    df = pd.read_csv(csv_path)

    # Define table reference
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID)

    # Configure the load job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip header row
        autodetect=True,  # Auto-detect schema
    )

    # Load data
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"Loaded {len(df)} rows into {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")

if __name__ == "__main__":
    # Example usage
    load_job_postings_to_bigquery('data/processed/job_postings_clean.csv')