from pymongo import mongo_client, MongoClient
import pymongo
from modules.config import settings

client = MongoClient(settings.DB_URL)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect to the MongoDB server.")

db = client[settings.DB_NAME]

#User
User = db.Users
User.create_index([("email", pymongo.ASCENDING)], unique=True)




