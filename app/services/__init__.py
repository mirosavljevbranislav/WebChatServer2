from pymongo import MongoClient

CONNECTION_URI = "mongodb+srv://Bangie:1mirosavljev1@cluster0.zcy3e.mongodb.net/test"
client = MongoClient(CONNECTION_URI)
app_db = client.WebChatApp.Users
