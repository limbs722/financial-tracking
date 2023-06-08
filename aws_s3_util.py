import boto3
from datetime import datetime
import json
from pytz import timezone

client = boto3.client("s3")
bucket_name = "financial-tracking"


def upload(data, ticker):
    now = datetime.now(timezone("Asia/Seoul"))
    # JSON Data 생성
    filename = f'{now.strftime("%Y-%m-%dT%H:%M")}_{ticker}.json'
    json_data = json.dumps(data)

    client.put_object(Bucket=bucket_name, Key=filename, Body=json_data)


def get_json_data(date, ticker):
    filename = f"{date}_{ticker}.json"
    obj = client.get_object(Bucket=bucket_name, Key=filename)
    json_value = json.dumps(json.loads(obj["Body"].read().decode("utf-8")))
    return json.loads(json_value)
