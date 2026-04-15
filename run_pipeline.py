import argparse
import os
import subprocess
import sys
from pathlib import Path

ENV_FILE = Path('.env')

STAGES = [
    'azure',
    'resume_extract',
    'matching',
    'aws_upload',
    'gcp_load',
]

COMMANDS = {
    'azure': ['python', 'azure_pipeline/azure_pipeline.py'],
    'resume_extract': ['python', 'resume_text_extract.py'],
    'matching': ['python', 'matching_engine/resume_job_matcher.py'],
    'aws_upload': ['python', 'aws_pipeline/upload_resumes_to_s3.py'],
    'gcp_load': ['python', 'gcp_pipeline/load_to_bigquery.py'],
}


def run_stage(name):
    cmd = COMMANDS[name]
    print(f'\n=== Running stage: {name} ===')
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f'ERROR: stage {name} failed with exit code {result.returncode}')
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description='Run multi-cloud job analytics pipeline stages')
    parser.add_argument('--stages', nargs='+', choices=STAGES, default=STAGES, help='Pipeline stages to execute')
    args = parser.parse_args()

    if not ENV_FILE.exists():
        print('ERROR: .env file not found. Copy .env.example to .env and update it.')
        sys.exit(1)

    for stage in args.stages:
        run_stage(stage)

    print('\nPipeline completed successfully.')


if __name__ == '__main__':
    main()
