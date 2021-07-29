import boto3
import uuid


class KinesisTestApi:
    def __init__(self):
        self._kinesis = boto3.client('kinesis')
        self._partition_key = str(uuid.uuid4())

    def get_consumer(self):
        return ""

    def put_record(self, data):
        d1 = self._kinesis.put_record(
            StreamName="siemens-events", Data=data, PartitionKey=self._partition_key)
        print("before printing result...\n")
        print(d1)
        print(d1["ShardId"])
        if "ShardId" not in d1 and "SequenceNumber" not in d1:
            return True
        return False
