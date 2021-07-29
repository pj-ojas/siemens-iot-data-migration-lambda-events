

class EventProcessor:
    def __init__(self):
        print("EventProcessor")

    def process_event_data(self, event_data):
        print("process event data")
        if self._validate_data() == False:
            return False
        

    def _validate_data(self, event_data):
        try:
            if event_data.has_key("beaconName") and event_data.has_key("metricType") and event_data.has_key("uniqueDeviceId") and event_data.has_key("timestamp"):
                return True
        except Exception as e:
            return False
        return False
