import base64


class KinesisRecords:
    def __init__(self):
        self._data = ""

    def process_records(self, events):
        print("KinesisRecords: processRecords")

        if "Records" not in events:
            print("KinesisRecords: processRecords: Records are not present in events")
            return False
        if len(events["Records"]) <= 0:
            print("KinesisRecords: processRecords: Zero Records")
            return False
        for record in events["Records"]:
            if "kinesis" not in record:
                print(
                    "KinesisRecords: processRecords: kinesis is not present in record")
                continue
            kinesis_record = record["kinesis"]
            if "data" not in kinesis_record:
                print(
                    "KinesisRecords: processRecords: data is not present in kinesis record")
                continue
            data = kinesis_record["data"]
            data_decoded = base64.b64decode(data)
            self._data.append(data_decoded)

        print(self._data)
        return True
