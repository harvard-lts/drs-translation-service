import json
import logging
import os
import time

import stomp

logfile = os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel = os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel, format="%(asctime)s:%(levelname)s:%(message)s")


class ConnectionParams:
    def __init__(self, conn, queue, host, port, user, password, ack="client-individual"):
        self.conn = conn
        self.queue = queue
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ack = ack


def get_process_mq_connection(queue=None):
    logging.debug("************************ MQUTILS - GET_PROCESS_MQ_CONNECTION *******************************")
    try:
        host = os.getenv('PROCESS_MQ_HOST')
        port = os.getenv('PROCESS_MQ_PORT')
        user = os.getenv('PROCESS_MQ_USER')
        password = os.getenv('PROCESS_MQ_PASSWORD')
        if (queue is None):
            process_queue = os.getenv('PROCESS_QUEUE_CONSUME_NAME')
        else:
            process_queue = queue
        conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
        connection_params = ConnectionParams(conn, process_queue, host, port, user, password)
        conn.connect(user, password, wait=True)
    except Exception as e:
        logging.error(e)
        raise (e)
    return connection_params


def notify_ingest_status_process_message(package_id, status, urn=None, queue=None):
    '''Creates a json message to notify the DIMS that the drs ingest has finished an ingest attempt'''
    logging.debug("************************ MQUTILS - CREATE_PROCESS_MESSAGE *******************************")
    message = "No message"
    try:
        if (queue is None):
            process_queue = os.getenv('PROCESS_QUEUE_PUBLISH_NAME')
        else:
            process_queue = queue

        msg_json = {
            "package_id": package_id,
            "application_name": "Dataverse",
            "batch_ingest_status": status,
            "drs_url": urn,
            "admin_metadata": {
                "original_queue": process_queue,
                "retry_count": 0
            }

        }

        expiration = _get_expiration()

        logging.debug("msg json:")
        logging.debug(msg_json)
        message = json.dumps(msg_json)
        connection_params = get_process_mq_connection(process_queue)
        connection_params.conn.send(process_queue, message, headers={"persistent": "true", "expires": expiration})
        logging.debug("MESSAGE TO QUEUE create_initial_queue_message")
        logging.debug(message)
    except Exception as e:
        logging.error(e)
        raise e
    return message


def _get_expiration():
    # Default to one hour from now
    now_in_ms = int(time.time()) * 1000
    expiration = int(os.getenv('MESSAGE_EXPIRATION_MS', 36000000)) + now_in_ms
    return expiration
