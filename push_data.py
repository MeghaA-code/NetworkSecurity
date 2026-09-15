import os
import sys
import json
import certifi
import pandas as pd
import pymongo

from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException


# Load .env from the same folder as push_data.py
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path, override=True)

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL was not found in the .env file")


class NetworkDataExtract:

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)

            data.reset_index(drop=True, inplace=True)

            records = list(
                json.loads(data.T.to_json()).values()
            )

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        mongo_client = None

        try:
            mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=60000,
                connectTimeoutMS=60000
            )

            # Check MongoDB connection and authentication
            mongo_client.admin.command("ping")
            print("MongoDB Atlas connection successful")

            db = mongo_client[database]
            collection_obj = db[collection]

            result = collection_obj.insert_many(records)

            return len(result.inserted_ids)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

        finally:
            if mongo_client is not None:
                mongo_client.close()


if __name__ == "__main__":

    FILE_PATH = os.path.join(
        os.path.dirname(__file__),
        "Network_Data",
        "PhisingData.csv"
    )

    DATABASE = "MEGHAAI"
    COLLECTION = "NetworkData"

    network_obj = NetworkDataExtract()

    records = network_obj.csv_to_json_convertor(FILE_PATH)

    print(f"Total records found: {len(records)}")

    no_of_records = network_obj.insert_data_mongodb(
        records,
        DATABASE,
        COLLECTION
    )

    print(f"Records inserted successfully: {no_of_records}")