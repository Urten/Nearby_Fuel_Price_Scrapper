from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

mongodb_pass = os.getenv("mongodb_pass")
mongodb_username = os.getenv("mongodb_username")

uri = f"mongodb+srv://{mongodb_username}:{mongodb_pass}@cluster0.odv1cn6.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


class MongoDB:
    def __init__(self, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client["telegram_petrol_pump_users"]
        self.collection = self.db[collection_name]

    def search_one(self, query):
        return self.collection.find_one(query, {'_id': 0})

    def search(self, query):
        return self.collection.find(query, {'_id': 0})

    def post(self, data):
        return self.collection.insert_one(data)

    def delete(self, query):
        return self.collection.delete_one(query)

    def update(self, value, new_value):
        try:
            prev_data = value
            new_data = {"$set": new_value}

            self.collection.update_one(prev_data, new_data)
            return print("Data updated successfully")

        except Exception as e:
            print(e)

    def find_and_update(self, value, new_value):
        self.collection.find_one_and_update(value, {"$set": new_value})


if __name__ == '__main__':
    # Usage
    db = MongoDB("users_petrol_pump")

    # Search
    for doc in db.search({"name": "John Doe"}):
        print(doc)

    # Post
    result = db.post({"name": "John Doe", "age": 30})
    print(f"Inserted with ID: {result.inserted_id}")
