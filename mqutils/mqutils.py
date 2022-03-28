import os, json, stomp, logging

logfile=os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel)

class ConnectionParams:
    def __init__(self, conn, queue, host, port, user, password):
        self.conn = conn
        self.queue = queue
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
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
        conn.set_ssl([(host, port)])
        connection_params = ConnectionParams(conn, process_queue, host, port, user, password)
        conn.connect(user, password, wait=True)
    except Exception as e:
        logging.error(e)
        raise(e)
    return connection_params

def notify_ingest_status_process_message(queue=None):
    '''Creates a json message to notify the DIMS that the drs ingest has finished an ingest attempt'''
    logging.debug("************************ MQUTILS - CREATE_PROCESS_MESSAGE *******************************")
    message = "No message"
    try:
        #Add more details that will be needed from the load report.
        msg_json = {
            "package_id": "12345",
            "application_name": "Dataverse",
            "batch_ingest_status": "success",
            "message": "Some Notes"
        }
        if (queue is None):
            process_queue = os.getenv('PROCESS_QUEUE_PUBLISH_NAME')
        else:
            process_queue = queue
                
        logging.debug("msg json:")
        logging.debug(msg_json)
        message = json.dumps(msg_json)
        connection_params = get_process_mq_connection(process_queue)
        connection_params.conn.send(process_queue, message, headers = {"persistent": "true"})
        logging.debug("MESSAGE TO QUEUE create_initial_queue_message")
        logging.debug(message)
    except Exception as e:
        logging.error(e)
        raise(e)
    return message

        
def get_drs_mq_connection(queue=None):
    logging.debug("************************ MQUTILS - GET_DRS_MQ_CONNECTION *******************************")
    try:
        host = os.getenv('DRS_MQ_HOST')
        port = os.getenv('DRS_MQ_PORT')
        user = os.getenv('DRS_MQ_USER')
        password = os.getenv('DRS_MQ_PASSWORD')
        if (queue is None):
            drs_queue = os.getenv('DRS_TOPIC_NAME')
        else:
            drs_queue = queue
        logging.debug("************************ QUEUE: {} *******************************".format(drs_queue))
    
        conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
        conn.set_ssl([(host, port)])
        connection_params = ConnectionParams(conn, drs_queue, host, port, user, password)
        conn.connect(user, password, wait=True)
    except Exception as e:
        logging.error(e)
        raise(e)
    return connection_params

def notify_mock_drs_trigger_message(queue=None):
    '''Creates a mock message that indicates that the drs'''
    logging.debug("************************ MQUTILS - CREATE_PROCESS_MESSAGE *******************************")
    message = "No message"
    try:
        #Add more details that will be needed from the load report.
        msg_json = {
            "package_id": "12345",
            "application_name": "Dataverse",
            "batch_ingest_status": "success",
            "message": "Some Notes"
        }
        if (queue is None):
            drs_queue = os.getenv('DRS_QUEUE_PUBLISH_NAME')
        else:
            drs_queue = queue
                
        logging.debug("msg json:")
        logging.debug(msg_json)
        message = json.dumps(msg_json)
        connection_params = get_drs_mq_connection(drs_queue)
        connection_params.conn.send(drs_queue, message, headers = {"persistent": "true"})
        logging.debug("MESSAGE TO QUEUE create_initial_queue_message")
        logging.debug(message)
    except Exception as e:
        logging.error(e)
        raise(e)
    return message

