import boto3
from datetime import datetime
import json
from pytz import timezone


def upload(data, ticker):
    now = datetime.now(timezone("Asia/Seoul"))
    s3 = boto3.client("s3")
    bucket_name = "financial-tracking"
    # JSON Data 생성
    filename = f'{now.strftime("%Y-%m-%d %H:%M:%S")}_{ticker}.json'
    json_data = json.dumps(data)
    s3.put_object(Bucket=bucket_name, key=filename, Body=json_data)
