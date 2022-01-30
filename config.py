import pymongo
import certifi

mongo_url = "mongodb+srv://mongodb:<password>@cluster0.ga4c1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url, tlsCAFile=certifi.where())


db = client.get_database("freshfruit")
