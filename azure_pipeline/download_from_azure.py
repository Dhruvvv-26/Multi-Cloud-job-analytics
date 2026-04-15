from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_NAME = os.getenv(AZURE_STORAGE_ACCOUNT_NAME)
ACCOUNT_KEY = os.getenv(AZURE_STORAGE_ACCOUNT_KEY)
CONTAINER_NAME = os.getenv(AZURE_PROCESSED_CONTAINER)
BLOB_NAME = job_postings_processed.csv
LOCAL_FILE = data/job_postings_processed.csv

blob_service_client = BlobServiceClient(
    account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
    credential=ACCOUNT_KEY
)

blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

with open(LOCAL_FILE, "wb") as f:
    data = blob_client.download_blob().readall()
    f.write(data)

print("Downloaded processed CSV from Azure Blob to local file.")
