import base64
import requests
import json
from aws.secrete_manager import SecretsManager


class MindSphereAuthentication:
    def __init__(self, secretManager):
        self.secretsManager = secretManager

    def getToken(self):

        key_store_client_id = self.secretsManager.get_client_id()
        key_store_client_secret = self.secretsManager.get_client_secret()

        authorization = base64.b64encode(
            (key_store_client_id + ":" + key_store_client_secret).encode())
        authorization = authorization.decode()
        headers = {'Accept': 'application/hal+json', 'Content-Type': 'application/json',
                   'X-SPACE-AUTH-KEY': 'Basic '+str(authorization)}
        api_url = 'https://gateway.eu1.mindsphere.io/api/technicaltokenmanager/v3/oauth/token'
        try:
            body_params = {
                "grant_type": "client_credentials",
                "appName":	"etl",
                "appVersion": "v1.0.1",
                "hostTenant": "usslcsop",
                "userTenant": "usslcs"
            }
            payload = json.dumps(body_params)
            response = requests.request(
                method='POST',
                url=api_url,
                params=None,
                headers=headers,
                data=payload
            )
            response.raise_for_status()

            if response.text:
                json_data = json.loads(response.text)
                access_token = json_data["access_token"]
                return access_token

        except Exception as e:
            print("Exception in getting token: ", e)
        return None
