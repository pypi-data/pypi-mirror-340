from elasticsearch import Elasticsearch
from inception_audittrail_logger.settings_audittrail import get_audittrail_setting

audittrail_setting = get_audittrail_setting()
# Connect to ES
es = Elasticsearch(audittrail_setting.elasticsearch_url)

# ✅ Confirm connection
if es.ping():
    print("✅ Successfully connected to Audittrail Elasticsearch!")
else:
    print("❌ Failed to connect to Audittrail Elasticsearch.")


async def index_document(document_id: str, body: dict):
    response = es.index(
        index=audittrail_setting.elasticsearch_index, id=document_id, document=body
    )
    print(f"✅ Successfully indexed document into Elasticsearch: {document_id}")
    return response


async def search_es_documents(query: dict):
    response = es.search(index=audittrail_setting.elasticsearch_index, body=query)
    print(f"✅ Successfully searched Elasticsearch: {response}")
    return response
