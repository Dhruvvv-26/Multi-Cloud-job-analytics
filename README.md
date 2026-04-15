# Multi-Cloud Job Market Insights & Resume Intelligence Platform

## Overview

This repository delivers a deployable, multi-cloud data engineering and analytics pipeline for job postings and resume intelligence. The platform is built with real Azure Blob Storage integration for dataset management, while AWS and GCP components provide storage, processing, and analytics capabilities.

## Architecture

- **Azure**: Primary data lake and ETL pipeline.
  - Stores raw and processed job posting data in Azure Blob Storage.
  - Executes Python-based cleaning and transformation of job posting datasets.
- **AWS**: Resume storage and processing.
  - Stores PDF resumes in Amazon S3.
  - Provides a safe, free-tier-compatible resume upload flow using `boto3`.
- **GCP**: Analytics and reporting.
  - Loads processed job posting data into BigQuery.
  - Supports SQL analytics and dashboarding via Looker Studio.

## Key Features

- Azure Blob-based ETL for dataset ingestion and processing
- Local resume parsing from PDF to structured text
- AWS S3 resume upload support
- GCP BigQuery dataset creation and CSV load support
- TF-IDF + cosine similarity resume-to-job matching engine
- Environment-driven configuration using `.env`

## Project Structure

```text
multi_cloud_job_analytics/
├── aws_pipeline/
│   └── upload_resumes_to_s3.py
├── azure_pipeline/
│   ├── azure_pipeline.py
│   └── download_from_azure.py
├── gcp_pipeline/
│   └── load_to_bigquery.py
├── matching_engine/
│   └── resume_job_matcher.py
├── data/
│   ├── job_postings_raw.csv
│   ├── job_postings_processed.csv
│   ├── processed/
│   │   ├── job_postings_clean.csv
│   │   └── resumes_text.csv
│   └── resumes_pdf/
├── .env.example
├── README.md
├── requirements.txt
├── data_cleaning.py
├── resume_text_extract.py
└── docker-compose.yml
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Azure Storage Account with Blob Storage
- AWS CLI configured locally
- Google Cloud project and service account JSON key
- `git` installed

### Local environment setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Dhruvvv-26/Multi-Cloud-job-analytics.git
   cd Multi-Cloud-job-analytics
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the sample environment file:
   ```bash
   cp .env.example .env
   ```
5. Populate `.env` with your Azure, AWS, and GCP credentials and resource names.

### Azure pipeline

1. Verify the Azure Storage Account and blob containers exist:
   - `raw-data`
   - `processed-data`
   - `logs`
2. Set the Azure credentials in `.env`.
3. Run the Azure ETL pipeline:
   ```bash
   python azure_pipeline/azure_pipeline.py
   ```
4. Download processed output locally:
   ```bash
   python azure_pipeline/download_from_azure.py
   ```

### Resume parsing

1. Place PDFs into `data/resumes_pdf/`
2. Extract resume text:
   ```bash
   python resume_text_extract.py
   ```

### AWS setup

1. Create an S3 bucket named in `AWS_S3_BUCKET_NAME`.
2. Upload resumes to S3:
   ```bash
   python aws_pipeline/upload_resumes_to_s3.py
   ```

### GCP setup

1. Create or select a Google Cloud project.
2. Create a service account with BigQuery permissions.
3. Set `GOOGLE_APPLICATION_CREDENTIALS` in `.env` to the service account JSON path.
4. Load processed data to BigQuery:
   ```bash
   python gcp_pipeline/load_to_bigquery.py
   ```

### Matching engine

Run the resume matching engine after processing job and resume data:

```bash
python matching_engine/resume_job_matcher.py
```

### End-to-end orchestration

Optionally run the full pipeline or select specific stages with:

```bash
python run_pipeline.py --stages azure resume_extract matching
```

Or run the full available pipeline:

```bash
python run_pipeline.py
```

## Current Status

### Completed

- Azure Storage Account integration for dataset ingestion and processing
- Local resume PDF text extraction
- AWS S3 resume upload script
- GCP BigQuery upload script with dataset creation support
- Matching engine using TF-IDF and cosine similarity

### Planned for future

- AWS Lambda serverless processing (pending free-tier validation)
- AWS Comprehend NLP integration (pending cost assessment)
- Looker Studio dashboards on BigQuery
- REST API or UI layer for resume-job matching

## Cloud cost and free-tier guidance

- **Azure Blob Storage**: free-tier and educational credits are suitable for small datasets
- **AWS S3**: free-tier includes 5 GB of standard storage; resume PDFs are low size
- **Google BigQuery**: free-tier includes 10 GB of storage and 1 TB of monthly query processing
- **Avoid enabling paid services** such as Comprehend unless you understand the billing model

## Notes

- Keep `.env` out of source control. Use `.env.example` to share configuration structure.
- Remove large raw datasets from git if they exceed GitHub limits.
- Run the pipeline in controlled batches to avoid data ingestion or query costs.

## Author

Multi-Cloud Job Market Insights & Resume Intelligence Platform
