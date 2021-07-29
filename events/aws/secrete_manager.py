class SecretsManager():
    def __init__(self):
        print("SecretsManager")
        self.client_id = "invalid id"
        self.client_secret = "invalid secrete"
        self.load()

    def load(self):
       # load these secretes from aws
        self.client_id = "usppaldv-javareat-1.0.0"
        self.client_secret = "09FHU70HCQhRxYf9DTTYG5HqiAqSuH30VAACwpbaL9b"

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret
