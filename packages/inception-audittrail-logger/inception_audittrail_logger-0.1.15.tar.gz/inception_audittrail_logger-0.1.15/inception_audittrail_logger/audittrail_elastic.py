from elasticsearch import Elasticsearch
from settings_audittrail import get_audittrail_setting

# Connect to ES
es = Elasticsearch(get_audittrail_setting().elasticsearch_url)

def index_document(index_name: str, document_id: str, body: dict):
    response = es.index(index=index_name, id=document_id, document=body)
    print(response)
    return response

def search_es_documents(index_name: str, query: dict):
    response = es.search(index=index_name, body=query)
    print(response)
    return response

