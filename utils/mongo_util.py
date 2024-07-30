# -*- coding:utf-8 -*-
from pymongo import MongoClient


class MongoUtil:

    def __init__(self, config):
        host = config.get("host")
        port = config.get("port")
        db = config.get("db")
        username = config.get("username")
        password = config.get("password")
        uri = f"mongodb://{username}:{password}@{host}:{port}/{db}"
        self.client = MongoClient(uri, uuidRepresentation="standard")
        self.baike = self.client["local"]["baike"]

    def insert_one_doc(self, doc):
        self.baike.insert_one(doc)
