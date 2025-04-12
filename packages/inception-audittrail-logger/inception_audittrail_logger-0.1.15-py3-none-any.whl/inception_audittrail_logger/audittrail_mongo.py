from pymongo import MongoClient
from settings_audittrail import get_audittrail_setting
from datetime import datetime
import uuid
audittrail_setting = get_audittrail_setting()
# Connect to MongoDB
client_audittrail = MongoClient(audittrail_setting.mongodb_url)
db_audittrail = client_audittrail[audittrail_setting.mongodb_database]
collection_audittrail = db_audittrail[audittrail_setting.mongodb_collection]

def insert_document(document: dict):
    collection_audittrail.insert_one(document)

def search_documents(query: dict):
    return collection_audittrail.find(query)
