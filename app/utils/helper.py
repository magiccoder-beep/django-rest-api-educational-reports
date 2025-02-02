import random
import time


def generateUniqueID():
    return (
        f"{int(time.time() * 1000)}x{random.randint(100000000000000, 999999999999999)}"
    )
