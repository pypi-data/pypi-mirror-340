from typing import Any
import os
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

class mongo_operation:
    __collection = None  # protected class-level variable
    __database = None

    def __init__(self, client_url: str, database_name: str, collection_name: str = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name

    def create_mongo_client(self) -> MongoClient:
        return MongoClient(self.client_url, server_api=ServerApi('1'))

    def create_database(self) -> Any:
        if mongo_operation.__database is None:
            client = self.create_mongo_client()
            self.database = client[self.database_name]
            mongo_operation.__database = self.database
        return mongo_operation.__database

    def create_collection(self, collection: str = None) -> Any:
        if collection is None:
            collection = self.collection_name

        if mongo_operation.__collection is None:
            database = self.create_database()
            self.collection = database[collection]
            mongo_operation.__collection = collection
        elif mongo_operation.__collection != collection:
            database = self.create_database()
            self.collection = database[collection]
            mongo_operation.__collection = collection
            
        return self.collection

    def insert_record(self, record: dict, collection_name: str) -> Any:
        if type(record) == list:
            for data in record:
                if type(data) != dict:
                    raise TypeError("record must be a dictionary")
                collection = self.create_collection(collection_name)
                collection.insert_many(record)
        elif type(record) == dict:
            collection = self.create_collection(collection_name)
            collection.insert_one(record)

    def bulk_insert(self, datafile: str, collection_name: str = None):
        self.path = datafile

        if self.path.endswith('.csv'):
            dataframe = pd.read_csv(self.path, encoding='utf-8')
        elif self.path.endswith('.xlsx'):
            dataframe = pd.read_excel(self.path, encoding='utf-8')
        else:
            raise ValueError("Unsupported file type. Only .csv and .xlsx are supported.")

        datajson = json.loads(dataframe.to_json(orient='records'))
        collection = self.create_collection(collection_name)
        collection.insert_many(datajson)
