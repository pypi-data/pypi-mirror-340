from pymongo import MongoClient, errors
from inception_audittrail_logger.settings_audittrail import get_audittrail_setting

audittrail_setting = get_audittrail_setting()

# Connect to MongoDB
client_audittrail = MongoClient(audittrail_setting.mongodb_url)
try:
    client_audittrail.admin.command("ping")
    print("✅ Successfully connected to Audittrail MongoDB!")
except errors.ServerSelectionTimeoutError as e:
    print("❌ Failed to connect to Audittrail MongoDB.")

db_audittrail = client_audittrail[audittrail_setting.mongodb_database]
collection_audittrail = db_audittrail[audittrail_setting.mongodb_collection]


def insert_document(document: dict):
    collection_audittrail.insert_one(document)
    print(
        f"✅ Successfully inserted document into Audittrail MongoDB: {document}"
    )


def search_documents(query: dict):
    return collection_audittrail.find(query)
