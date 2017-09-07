import sys, uuid
import controller
from network import AcquireClient

if __name__ == "__main__":
    master = uuid.uuid4().hex
    a = Controller(master)
    b = AcquireClient()
    b.set_id(master)

