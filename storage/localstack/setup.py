import json
import os

import boto3

BUCKET_NAME = os.getenv("S3__BUCKET", "videohosting")
REGION = os.getenv("S3__REGION_NAME", "us-east-1")
ENDPOINT_URL = "http://localhost:4566"
ACCESS_KEY = os.getenv("S3__ACCESS_KEY")
SECRET_KEY = os.getenv("S3__SECRET_KEY")

s3 = boto3.client(
    "s3",
    region_name=REGION,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

# Создать бакет если не существует
existing = s3.list_buckets().get("Buckets", [])
if not any(b["Name"] == BUCKET_NAME for b in existing):
    if REGION == "us-east-1":
        s3.create_bucket(Bucket=BUCKET_NAME)
    else:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )
    print(f"[localstack] Bucket '{BUCKET_NAME}' created")
else:
    print(f"[localstack] Bucket '{BUCKET_NAME}' already exists")

# Сделать бакет публичным на чтение (для отдачи файлов без авторизации)
public_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*",
        }
    ],
}
s3.put_bucket_policy(Bucket=BUCKET_NAME, Policy=json.dumps(public_policy))
print(f"[localstack] Public read policy applied to '{BUCKET_NAME}'")

# Настроить CORS для бакета
cors_config = {
    "CORSRules": [
        {
            "AllowedOrigins": ["*"],
            "AllowedMethods": ["GET", "HEAD", "PUT", "POST", "DELETE"],
            "AllowedHeaders": ["*"],
            "MaxAgeSeconds": 3000,
        }
    ]
}
s3.put_bucket_cors(Bucket=BUCKET_NAME, CORSConfiguration=cors_config)
print(f"[localstack] CORS policy applied to '{BUCKET_NAME}'")
