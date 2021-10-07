import boto3

PROJECT_PATH = "/78460/san/prod-env"
EVENTS_TYPEID = "/events/typeid"
CLIENT_ID = "/app-creds/id"
CLIENT_SECRET = "/app-creds/secret"


class SecretsManager():

    def __init__(self):
        self.client_id = "invalid id"
        self.client_secret = "invalid secrete"
        self.event_typeid = "invalid typeid"  # "c3dc304c-b25e-4db1-9a1a-48676016fbf2"
        self.ssm = boto3.client('ssm', region_name='us-east-2')
        self.load()

    def load(self):
       # load these secretes from aws
        self.client_id = ""  # "usslcsop-etl-v1.0.1-88821532"
        self.client_secret = ""  # "VeNMmFFuF4Nbhw1JDU5a4ivK3ClJXrIL4Spjc5HRqg7"
        names = []
        names.append(PROJECT_PATH+CLIENT_ID)
        names.append(PROJECT_PATH+CLIENT_SECRET)
        names.append(PROJECT_PATH+EVENTS_TYPEID)
        response = self.ssm.get_parameters(
            Names=names, WithDecryption=False)
        print("system Manager get_parameters response: ", response)

        for parameter in response['Parameters']:
            if parameter['Name'] == PROJECT_PATH+CLIENT_ID:
                self.client_id = parameter['Value']
            elif parameter['Name'] == PROJECT_PATH+CLIENT_SECRET:
                self.client_secret = parameter['Value']
            elif parameter['Name'] == PROJECT_PATH+EVENTS_TYPEID:
                self.event_typeid = parameter['Value']

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret

    def get_event_typeid(self):
        return self.event_typeid
