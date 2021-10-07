import os
from datetime import datetime
import json

from mindsphere.mindsphere_authentication import MindSphereAuthentication
from aws.secrete_manager import SecretsManager
import requests


class MindSphereEventConnector:
    def __init__(self):
        self._token = ""
        self.typeId = ""
        self._events_url = "https://gateway.eu1.mindsphere.io/api/eventmanagement/v3/events"
        self._create_events_jobs_url = "https://gateway.eu1.mindsphere.io/api/eventmanagement/v3/createEventsJobs"

        self._id_key_loaded = False
        self._headers = None
        self.secretManager = SecretsManager()
        self._events = []

    def _loadToken(self):
        try:
            mindsphereAuthentication = MindSphereAuthentication(
                self.secretManager)
            self._token = mindsphereAuthentication.getToken()
            self.typeId = self.secretManager.get_event_typeid()
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

    def write(self, entityId, eventUuid, value, newState, oldState, metricType, policyName, beaconName, timestamp, timestampCleared, beaconId):
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
                "beaconName": beaconName,
                "beaconId": beaconId
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
            if response.text:
                json_data = json.loads(response.text)
                print("response.text: ", json_data)

            return True

        except Exception as err:
            print(
                f"Exception mindshpere_connector: write_to_mindsphere:  {err} response {response}")
        return False

    def addEvent(self, entityId, eventUuid, value, newState, oldState, metricType, policyName, beaconName, timestamp, timestampCleared, beaconId):
        event = {
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
            "beaconName": beaconName,
            "beaconId": beaconId
        }
        self._events.append(event)
        return True

    def write_events(self):
        response = None
        try:
            if self._headers == None:
                print("Error: Failed to get headers")
                return False
            # write event records not more than 50 at once
            # if more than 50 records are in the self._events, return false for now
            # TODO batch and send 50 at a time
            if len(self._events) == 0:
                print("Error: write_events: No records available to write")
                return False
            if len(self._events) > 50:
                print("Error: write_events: More than 50 records")
                return False
            print("write_events: records count: ", len(self._events))
            payload = {
                "events": self._events
            }
            payload = json.dumps(payload)
            response = requests.request(
                method='POST',
                url=self._create_events_jobs_url,
                params=None,
                headers=self._headers,
                data=payload
            )
            response.raise_for_status()
            if response.text:
                json_data = json.loads(response.text)
                print("mindshpere_connector: write_events: response.text: ", json_data)

            # Flush records
            self._events = []
            return True
        except Exception as err:
            print(
                f"Exception mindshpere_connector: write_to_mindsphere:  {err} response {response}")
        return False
