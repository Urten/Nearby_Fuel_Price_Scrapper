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
        """        Initialize a new instance of the class with the given collection name.

        Args:
            collection_name (str): The name of the collection to be used.
        """

        self.client = MongoClient(uri)
        self.db = self.client["telegram_petrol_pump_users"]
        self.collection = self.db[collection_name]

    def search_one(self, query):
        """        Retrieve a single document from the collection based on the provided query.

        Args:
            query (dict): A dictionary representing the query to be executed.

        Returns:
            dict: A single document matching the query criteria, excluding the '_id' field.
        """

        return self.collection.find_one(query, {'_id': 0})

    def search(self, query):
        """        Search for documents in the collection based on the given query.

        Args:
            query (dict): A dictionary representing the query to be executed.

        Returns:
            pymongo.cursor.Cursor: A cursor object pointing to the result set of the query.
        """

        return self.collection.find(query, {'_id': 0})

    def post(self, data):
        """        Insert a document into the collection.

        Args:
            data (dict): A dictionary representing the document to be inserted.

        Returns:
            pymongo.results.InsertOneResult: An object representing the result of the insertion.
        """

        return self.collection.insert_one(data)

    def delete(self, query):
        """        Delete a single document from the collection based on the provided query.

        Args:
            query (dict): A dictionary representing the query to match the document to be deleted.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """

        return self.collection.delete_one(query)

    def update(self, value, new_value):
        """        Update the value in the collection with the new value.

        Args:
            value (dict): The previous data to be updated.
            new_value (dict): The new data to replace the previous data.


        Raises:
            Exception: If an error occurs during the update process.
        """

        try:
            prev_data = value
            new_data = {"$set": new_value}

            self.collection.update_one(prev_data, new_data)
            return print("Data updated successfully")

        except Exception as e:
            print(e)

    def find_and_update(self, value, new_value):
        """        Find a document in the collection and update it with new values.

        Args:
            value (dict): The query to find the document to be updated.
            new_value (dict): The new values to be set in the document.
        """

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
