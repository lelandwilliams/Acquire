
from network import AcquireClient

class randomAI(AcquireClient):
    def __init__(self, name, acquire_id):
        super().__init__()
        self.set_id(acquire_id)
        self.name = name


