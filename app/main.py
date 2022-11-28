from fastapi import FastAPI
from pydantic import BaseModel
import json
from datetime import datetime
import jsonpickle
from typing import List
from datetime import datetime
import pytz
import configparser
import boto3

config = configparser.RawConfigParser()
config.read("config.properties")
kin = boto3.client(
    "kinesis",
    region_name=config.get("details", "region"),
    aws_access_key_id=config.get("details", "access_key"),
    aws_secret_access_key=config.get("details", "secret_key"),
)

app = FastAPI()


class JsonData(BaseModel):
    name: str
    city: str
    phone: str
    id: str


@app.get("/get-data")
def home(stream_name: str, shard_id: str, time_stamp: str):
    response = kin.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType="AT_TIMESTAMP",
        Timestamp=pytz.timezone("Asia/Kolkata")
        .localize(datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S"))
        .astimezone(pytz.utc),
    )

    result = kin.get_records(ShardIterator=response["ShardIterator"])
    return {"data": result, "len": len(result["Records"])}


@app.post("/add-json")
def add(stream_name: str, partition_key: str, data: List[JsonData]):
    data = jsonpickle.encode(data)
    payload = kin.put_record(
        StreamName=stream_name, Data=json.dumps(data), PartitionKey=partition_key
    )
    payload
    return {"resp": payload}
