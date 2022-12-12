# CRUD methods for mongoDB
from pymongo import MongoClient
from bson.objectid import ObjectId


class Connection:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data):
        return self.collection.insert_one(data)

    def find(self, query):
        return self.collection.find(query)

    def find_one(self, query):
        return self.collection.find_one(query)

    def find_by_id(self, id):
        return self.collection.find_one({'_id': ObjectId(id)})

    def update(self, query, data):
        return self.collection.update_one(query, {'$set': data}, upsert=False)

    def delete(self, query):
        return self.collection.delete_one(query)

    def delete_by_id(self, id):
        return self.collection.delete_one({'_id': ObjectId(id)})

    def delete_all(self):
        return self.collection.delete_many({})

    def count(self):
        return self.collection.count_documents({})

    def count_by_query(self, query):
        return self.collection.count_documents(query)
