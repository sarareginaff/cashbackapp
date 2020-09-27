import string
import random
import os

random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(64))
SECRET_KEY = key
REDIS_HOST = "localhost"
REDIS_PORT = 6379
APPROVED_CPFS = '[15350946056]'


 