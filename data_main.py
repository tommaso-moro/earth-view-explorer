from data_fetcher import Fetcher
import pymongo
import os
from dotenv import load_dotenv
load_dotenv('.env')


def main():
    uri = os.getenv('MONGO_URI')
    db_name = os.getenv('DB_NAME')
    col_name = os.getenv('COLLECTION_NAME')
    mongo_client = pymongo.MongoClient(uri)
    mongo_collection = mongo_client.get_database(db_name)[col_name]

    #example usage:
    #fetcher = Fetcher(mongo_collection, batch_size=30)
    #fetcher.fetch()

    print("Done")


if __name__ == "__main__":
    main()