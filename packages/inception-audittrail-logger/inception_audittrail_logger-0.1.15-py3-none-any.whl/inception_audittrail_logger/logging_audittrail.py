from datetime import datetime
from format_data import format_audittrail_data, format_sys_error_data
from audittrail_mongo import insert_document
from audittrail_elastic import index_document
import asyncio
import sys

async def log(data: dict, user: dict, correlation_id: str, user_agent_str: str, ip_address: str):
    """
    Asynchronously format and log audit trail data to MongoDB and Elasticsearch.
    """
    try:
        formatted_data = await format_audittrail_data(data, user, correlation_id, user_agent_str, ip_address)
        results = await asyncio.gather(
            insert_document(formatted_data),
            index_document(formatted_data)
        )

        if all(results):
            print("✅ Audit trail saved to both MongoDB and Elasticsearch")
        else:
            print("⚠️ One or more logging targets failed")
            print(results)

        return results
    except Exception as e:
        # Optional: Add logging here
        print(f"[ERROR] Audit trail logging failed: {e}", file=sys.stderr)
        return None

async def log_audittrail(data: dict, user: dict, correlation_id: str, user_agent_str: str, ip_address: str):
    """
    Asynchronously format and log audit trail data to MongoDB and Elasticsearch.
    """
    try:
        if asyncio.get_event_loop().is_running():
            # If in an existing event loop, create a task
            asyncio.create_task(log(data, user, correlation_id, user_agent_str, ip_address))
        else:
            asyncio.run(log(data, user, correlation_id, user_agent_str, ip_address))
    except RuntimeError as e:
        print(f"[ERROR] Unable to log audit trail: {e}", file=sys.stderr)


async def log_sys_error(data: dict, user: dict, correlation_id: str, user_agent_str: str, ip_address: str):
    """
    Asynchronously format and log system error data to Elasticsearch.
    """
    try:
        formatted_data = await format_sys_error_data(data, user, correlation_id, user_agent_str, ip_address)
        results = await index_document(formatted_data)
        return results
    except Exception as e:
        print(f"[ERROR] System error logging failed: {e}", file=sys.stderr)
        return None
