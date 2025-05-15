import redis
from constants import REDIS_HOST, REDIS_PORT

redis_connection = None


def get_connection():
    global redis_connection
    if redis_connection is None:
        redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return redis_connection
