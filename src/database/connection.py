from pymongo import MongoClient


def connect(url):
    return MongoClient(url)


def create_database(client, db_name):
    return client[db_name]
