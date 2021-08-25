class SecretsManager():
    def __init__(self):
        print("SecretsManager")
        self.client_id = "invalid id"
        self.client_secret = "invalid secrete"
        self.load()

    def load(self):
       # load these secretes from aws
        self.client_id = "usslcsop-etl-v1.0.1-88821532"
        self.client_secret = "VeNMmFFuF4Nbhw1JDU5a4ivK3ClJXrIL4Spjc5HRqg7"

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret
