from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
RAW_CONTAINER = os.getenv("AZURE_RAW_CONTAINER")
PROCESSED_CONTAINER = os.getenv("AZURE_PROCESSED_CONTAINER")

blob_service_client = BlobServiceClient(
    account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
    credential=ACCOUNT_KEY
)

# Download CSV from Azure Blob
blob_client = blob_service_client.get_blob_client(container=RAW_CONTAINER, blob="job_postings_clean.csv")
data = blob_client.download_blob().readall()

df = pd.read_csv(BytesIO(data))
print("Rows:", len(df))

# Simple transformation example
df["title"] = df["title"].str.lower()

# Upload processed file
processed_blob_client = blob_service_client.get_blob_client(container=PROCESSED_CONTAINER, blob="job_postings_processed.csv")

csv_bytes = df.to_csv(index=False).encode("utf-8")
processed_blob_client.upload_blob(csv_bytes, overwrite=True)

print("Processed data uploaded to Azure Blob Storage.")
