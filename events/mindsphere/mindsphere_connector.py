
from mindsphere_core import RestClientConfig
from mindsphere_core import UserToken

# Import the MindsphereError from mindsphere_core.exceptions module
from mindsphere_core.exceptions import MindsphereError
from mindsphere_core.mindsphere_credentials import AppCredentials

# Import the TimeseriesClient from timeseries module
from timeseries.clients.time_series_client import TimeSeriesClient
from timeseries.models.timeseries import Timeseries

# Import the GetTimeseriesRequest from timeseries.models module
from timeseries.models import GetTimeseriesRequest
from timeseries.models import PutTimeseriesRequest


import os
from datetime import datetime
from events.aws.secrete_manager  import SecretsManager


class MindSphereConnector:
    def __init__(self):
        os.environ['HOST_ENVIRONMENT'] = "eu1"
        os.environ['MDSP_HOST_TENANT'] = "usppaldv"

        os.environ['MDSP_KEY_STORE_CLIENT_ID'] = "key"
        os.environ['MDSP_KEY_STORE_CLIENT_SECRET'] = "secret"
        os.environ['MDSP_OS_VM_APP_NAME'] = "javareat"
        os.environ['MDSP_OS_VM_APP_VERSION'] = "1.0.0"
        os.environ['MDSP_USER_TENANT'] = "usppaldv"

        os.environ['MINDSPHERE_CLIENT_ID'] = "client id"
        os.environ['MINDSPHERE_CLIENT_SECRET'] = "client secrete"
        os.environ['MINDSPHERE_SUB_TENANT'] = "javareat.javareat"
        os.environ['MINDSPHERE_TENANT'] = "usppaldv"
        print("environment variables: ", os.environ)
        self._id_key_loaded = False

        self._config = RestClientConfig()

    def getTimeSeriesClient(self):
        try:
            cred = AppCredentials(app_name=os.environ['MDSP_OS_VM_APP_NAME'], app_version=os.environ['MDSP_OS_VM_APP_VERSION'], key_store_client_id=os.environ['MDSP_KEY_STORE_CLIENT_ID'],
                                  key_store_client_secret=os.environ['MDSP_KEY_STORE_CLIENT_SECRET'], host_tenant=os.environ['MDSP_HOST_TENANT'], user_tenant=os.environ['MDSP_USER_TENANT'])
            # Create the TimeSeriesClient object using the RestClientConfig and UserToken objects
            timeseriesClient = TimeSeriesClient(
                rest_client_config=self._config, mindsphere_credentials=cred)
            return timeseriesClient
        except Exception as err:
            print(
                "mindshpere_connector: getTimeSeriesClient: Exception in getting client: ", err)
        return None

    def load_client_id_secrete(self):
        if self._id_key_loaded == False:
            secretsManager = SecretsManager()

            os.environ['MDSP_KEY_STORE_CLIENT_ID'] = secretsManager.get_client_id()
            os.environ['MDSP_KEY_STORE_CLIENT_SECRET'] = secretsManager.get_client_secret()

            os.environ['MINDSPHERE_CLIENT_ID'] = secretsManager.get_client_id()

            os.environ['MINDSPHERE_CLIENT_SECRET'] = secretsManager.get_client_secret()

            self._timeseriesClient = self.getTimeSeriesClient()

            self._id_key_loaded = True

    def _get_utc_string(self, time):
        time = time / 1000  # convert to seconds
        return datetime.utcfromtimestamp(time).strftime('%Y-%m-%dT%H:%M:%SZ')

    def write(self, entity, propertysetname, timestamp, time_series_data_fields):
        try:
            # get client id if required
            self.load_client_id_secrete()
            time_series_data_list = []
            i = 0
            for time in timestamp:
                time_series_data = Timeseries()
                time_series_data.time = self._get_utc_string(
                    time)  # datetime.now
                time_series_data.fields = time_series_data_fields[i]
                i = i + 1
                time_series_data_list.append(time_series_data)

            # Create the request object
            # ML1 entity id, receied through postman request
            request = PutTimeseriesRequest(
                timeseries=time_series_data_list,
                entity=entity,  # "c9cae0d910974388990557526fa0706d",
                propertysetname=propertysetname  # "01"
            )

            # Initiate Get Timeseries API call
            self._timeseriesClient.put_timeseries(request)
            return 0

        except MindsphereError as err:
            # Exception Handling
            print(
                "mindshpere_connector: write_to_mindsphere: Exception in getting client: ", err)
        return -1
