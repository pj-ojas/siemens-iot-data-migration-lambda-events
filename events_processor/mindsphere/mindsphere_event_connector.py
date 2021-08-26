import os
from datetime import datetime
import json

from mindsphere.mindsphere_authentication import MindSphereAuthentication
from aws.secrete_manager import SecretsManager
import requests


class MindSphereEventConnector:
    def __init__(self):
        self._token = ""
        self.typeId = "c3dc304c-b25e-4db1-9a1a-48676016fbf2"
        self._events_url = "https://gateway.eu1.mindsphere.io/api/eventmanagement/v3/events"

        self._id_key_loaded = False
        self._headers = None

    def _loadToken(self):
        try:
            self._token = MindSphereAuthentication().getToken()
        except Exception as err:
            print(
                "mindshpere_connector: _loadToken: Exception in getting token: ", err)
        return None

    def getHeaders(self):
        self._loadToken()
        self._headers = {'Accept': 'application/hal+json', 'Content-Type': 'application/json',
                         'Authorization': 'Bearer '+str(self._token)}

    def _get_utc_string(self, time):
        time = time / 1000  # convert to seconds
        return datetime.utcfromtimestamp(time).strftime('%Y-%m-%dT%H:%M:%SZ')

    def write(self, entityId, eventUuid, value, newState, oldState, metricType, policyName, beaconName, timestamp, timestampCleared):
        response = None
        try:
            if self._headers == None:
                print("Error: Failed to get headers")
                return False
            print(
                f"mindsphere_event_connector.py: {timestamp} {entityId} {eventUuid} {value} {newState} {oldState} {metricType} {policyName} {beaconName}")
            body_params = {
                "typeId": self.typeId,
                "timestamp": timestamp,
                "entityId": entityId,
                "eventUuid": eventUuid,
                "value": value,
                "newState": newState,
                "oldState": oldState,
                "timestampCleared": timestampCleared,
                "metricType": metricType,
                "policyName": policyName,
                "beaconName": beaconName
            }

            payload = json.dumps(body_params)
            response = requests.request(
                method='POST',
                url=self._events_url,
                params=None,
                headers=self._headers,
                data=payload
            )
            response.raise_for_status()
            # if response.text:
            #     json_data = json.loads(response.text)
            #     print("response.text: ", json_data)

            return True

        except Exception as err:
            print(
                f"Exception mindshpere_connector: write_to_mindsphere:  {err} response {response}")
        return False
