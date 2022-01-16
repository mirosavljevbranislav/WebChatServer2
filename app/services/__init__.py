from pymongo import MongoClient

CONNECTION_URI = "mongodb+srv://Bangie:1mirosavljev1@cluster0.zcy3e.mongodb.net/test"
client = MongoClient(CONNECTION_URI)
user_db = client.WebChatApp.Users
groups_db = client.WebChatApp.Groups