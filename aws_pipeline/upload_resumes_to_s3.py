import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# AWS S3 Configuration
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
RESUME_DIR = 'data/resumes_pdf'

def upload_resumes_to_s3():
    if not os.path.exists(RESUME_DIR):
        print(f"Directory {RESUME_DIR} does not exist.")
        return

    for filename in os.listdir(RESUME_DIR):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(RESUME_DIR, filename)
            s3_key = f"resumes/{filename}"

            try:
                s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
                print(f"Uploaded {filename} to s3://{BUCKET_NAME}/{s3_key}")
            except Exception as e:
                print(f"Failed to upload {filename}: {e}")

if __name__ == "__main__":
    upload_resumes_to_s3()