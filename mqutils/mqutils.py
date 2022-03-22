import os, json, time, datetime, stomp

class ConnectionParams:
    def __init__(self, conn, queue, host, port, user, password):
        self.conn = conn
        self.queue = queue
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
def get_process_mq_connection(queue=None):
    print("************************ MQUTILS - GET_PROCESS_MQ_CONNECTION *******************************")
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
        print(e)
        raise(e)
    return connection_params

def notify_process_message(queue=None):
    '''Creates a queue json message to notify the queue that the drs ingest has finished an ingest attempt'''
    print("************************ MQUTILS - CREATE_PROCESS_MESSAGE *******************************")
    message = "No message"
    try:
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat()
       
        #Add more details that will be needed from the load report.
        msg_json = {
            "package_id": "12345",
            "application_name": "DVN",
            "status": "success",
            "notes": "Some Notes",
            "timestamp": timestamp, 
        }
        if (queue is None):
            process_queue = os.getenv('PROCESS_QUEUE_CONSUME_NAME')
        else:
            process_queue = queue
                
        print("msg json:")
        print(msg_json)
        message = json.dumps(msg_json)
        connection_params = get_process_mq_connection(process_queue)
        connection_params.conn.send(queue, message, headers = {"persistent": "true"})
        print("MESSAGE TO QUEUE create_initial_queue_message")
        print(message)
    except Exception as e:
        print(e)
        raise(e)
    return message

        
def get_drs_mq_connection(queue=None):
    print("************************ MQUTILS - GET_DRS_MQ_CONNECTION *******************************")
    try:
        host = os.getenv('DRS_MQ_HOST')
        port = os.getenv('DRS_MQ_PORT')
        user = os.getenv('DRS_MQ_USER')
        password = os.getenv('DRS_MQ_PASSWORD')
        if (queue is None):
            drs_queue = os.getenv('DRS_QUEUE_NAME')
        else:
            drs_queue = queue
        print("************************ QUEUE: {} *******************************".format(drs_queue))
    
        conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
        conn.set_ssl([(host, port)])
        connection_params = ConnectionParams(conn, drs_queue, host, port, user, password)
        conn.connect(user, password, wait=True)
    except Exception as e:
        print(e)
        raise(e)
    return connection_params

