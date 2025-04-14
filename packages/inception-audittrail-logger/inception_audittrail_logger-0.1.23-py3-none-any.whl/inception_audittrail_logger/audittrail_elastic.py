from elasticsearch import Elasticsearch
from inception_audittrail_logger.settings_audittrail import (
    get_audittrail_setting,
    logger,
)

audittrail_setting = get_audittrail_setting()
# Connect to ES
es = Elasticsearch(audittrail_setting.elasticsearch_url)

# ✅ Confirm connection
if es.ping():
    logger.info("✅ Successfully connected to Audittrail Elasticsearch!")
else:
    logger.error("❌ Failed to connect to Audittrail Elasticsearch.")


def index_document(document_id: str, body: dict):
    response = es.index(
        index=audittrail_setting.elasticsearch_index, id=document_id, document=body
    )
    logger.info(f"✅ Successfully indexed document into Elasticsearch: {document_id}")
    return response


def search_es_documents(query: dict):
    response = es.search(index=audittrail_setting.elasticsearch_index, body=query)
    logger.info(f"✅ Successfully searched Elasticsearch: {response}")
    return response
