import base64
import json

from mindsphere.mindsphere_event_connector import MindSphereEventConnector


class KinesisRecords:
    def __init__(self):
        self._data = []
        self._beacon_mapping = {}

    def load_configuration(self):
        try:
            with open('./mindsphere/beacon_mapping.json') as json_file:
                mapping_data = json.load(json_file)
                for beacon in mapping_data["beacons"]:
                    id = list(beacon.keys())[0]
                    self._beacon_mapping[id] = beacon[id]
                return True
        except Exception as e:
            print("Exception: KinesisRecords: load_configuration: ", e)
            return False

    def process_records(self, events):
        if "Records" not in events:
            print(
                "Error: KinesisRecords: processRecords: Records are not present in events")
            return False
        if len(events["Records"]) <= 0:
            print("Error: KinesisRecords: processRecords: Zero Records")
            return False
        for record in events["Records"]:
            if "kinesis" not in record:
                print(
                    "Warning: KinesisRecords: processRecords: kinesis is not present in record")
                continue
            kinesis_record = record["kinesis"]
            if "data" not in kinesis_record:
                print(
                    "Warning: KinesisRecords: processRecords: data is not present in kinesis record")
                continue
            data = kinesis_record["data"]
            data_in_bytes = base64.b64decode(data)
            data_decoded = data_in_bytes.decode("utf-8")
            data_dict = json.loads(data_decoded)
            self._data.append(data_dict)

        return self._process_records()

    def _process_records(self):
        result = False
        try:
            mindsphere_event_connector = MindSphereEventConnector()
            mindsphere_event_connector.getHeaders()
            events_counter = 0
            for record in self._data:
                if not "uniqueDeviceId" in record:
                    print(
                        "Error: kinesis_records: _process_records: uniqueDeviceId is not found. skipping record...")
                    continue
                beacon_id = record["uniqueDeviceId"]

                # if not "beaconName" in record:
                #     print(
                #         "Error: kinesis_records: _process_records: beaconName is not found. skipping record...")
                #     continue
                # beaconName = record["beaconName"]

                # find the beacon_id in mapping data
                if not beacon_id in self._beacon_mapping:
                    print(
                        f"Error: kinesis_records: _process_records: beacon_id {beacon_id} is not found. skipping record...")
                    continue
                beacon_data = self._beacon_mapping[beacon_id]

                # if beaconName != beacon_data["device_name"]:
                #     print(
                #         f"Error: kinesis_records: _process_records: beaconName: {beaconName} is not configured in mapping. skipping record...")
                #     continue

                entityId = beacon_data["entityId"]

                result = mindsphere_event_connector.addEvent(entityId=entityId, eventUuid=record["eventUuid"], value=record["value"], newState=record["newState"],
                                                             oldState=record["oldState"], metricType=record["metricType"], policyName=record["policyName"], beaconName=record["beaconName"], timestamp=record["timestamp"], timestampCleared=record["timestampCleared"], beaconId=record["uniqueDeviceId"])
                if result == False:
                    return result
                events_counter += 1

                if events_counter == 50:
                    result = mindsphere_event_connector.write_events()
            # End of For loop

            # write any remaining events unwritte to mindsphere
            result = mindsphere_event_connector.write_events()
            return result
        except Exception as e:
            print("Exception: kinesis_record: _process_record: ", e)
        return False


# the following is example event data
# {
#   "beaconName": "VSU-SS2-OU",
#   "blufiId": "0",
#   "eventUuid": "8c957950-e2b2-4047-7c29-3aaea42169b2",
#   "metricType": "TEMPERATURE",
#   "namespace": "BEACON",
#   "newState": "VIOLATING",
#   "oldState": "OK",
#   "policyId": 203000,
#   "policyName": "36",
#   "projectId": 78460,
#   "timestamp": 1629432919768,
#   "timestampCleared": 1629432919768,
#   "uniqueDeviceId": "4292002323941335760",
#   "value": "36.25 leaves the range of [
#     0.00,
#   36.00
# ]"
# }


# {"beaconName": "CS2-17",
# "blufiId": "0",
# "eventUuid": "6f904893-a1fc-49f6-5fc5-c93d37e0181f",
# "metricType": "VIBRATION_THRESHOLD",
# "namespace": "BEACON",
# "newState": "VIOLATING",
# "oldState": "OK",
# variable: xvRms

#  "policyId": 203034,
# "policyName": "0.28",
# "projectId": 78460,
# "timestamp": 1629935595252,
# "timestampCleared": 1629935595252,
# "uniqueDeviceId": "1225101039184540586",
# "value": "v:0.298086,a:X,m:VELOCITY_RMS,u:in/s,t:0.280000"}
