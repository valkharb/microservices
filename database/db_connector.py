import json
import pymongo

from config import DATABASE
from config import REDIS

BASE_CONNECTION_URI = (
    'mongodb://{user}:{password}@{hosts}/{database}'
)


def parse_conn_data(config: dict):
    hosts = json.loads(config['DB_HOSTS'])
    return {
        'DB_USER': config.get('DB_USER'),
        'DB_PASSWORD': config.get('DB_PASSWORD'),
        'DB_HOSTS': hosts,
        'DB_PORT': config.get('DB_PORT'),
        'DB_NAME': config.get('DB_NAME'),
    }


CONFIG = parse_conn_data(DATABASE)

db_name = CONFIG['DB_NAME']
hosts_str = ','.join(
    [
        host + ':' + CONFIG['DB_PORT']
        for host in CONFIG['DB_HOSTS']
    ]
)


def generate_redis_connection_string():
    return 'redis://{host}:{port}'.format(
        host=REDIS['host'],
        port=REDIS['port']
    )


def generate_mongo_connection_string():
    return BASE_CONNECTION_URI.format(
        user=CONFIG['DB_USER'],
        password=CONFIG['DB_PASSWORD'],
        hosts=hosts_str,
        database=db_name,
    )


class Database(pymongo.database.Database):
    users = pymongo.database.Collection


def connect() -> Database:
    mongo_connection_uri = generate_mongo_connection_string()

    client = pymongo.MongoClient(
            mongo_connection_uri,
            connect=False
        )
    return client.get_database(db_name)
