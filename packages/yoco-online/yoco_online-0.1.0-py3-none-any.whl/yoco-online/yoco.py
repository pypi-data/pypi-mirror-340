

class Yoco:

    _SECRET_KEY: str

    def __init__(self, secret_key: str):
        self._SECRET_KEY = secret_key

    def create_checkout(self, amount):
        print("Creating YOCO checkout coming soon")
        