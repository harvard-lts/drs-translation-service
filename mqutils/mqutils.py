import os, json, time, datetime, stomp

_queue = os.getenv('PROCESS_QUEUE_NAME')

def get_process_mq_connection():
    print("************************ MQUTILS - GET_PROCESS_MQ_CONNECTION *******************************")
    try:
        host = os.getenv('PROCESS_MQ_HOST')
        port = os.getenv('PROCESS_MQ_PORT')
        user = os.getenv('PROCESS_MQ_USER')
        password = os.getenv('PROCESS_MQ_PASSWORD')

        conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
        conn.set_ssl([(host, port)])
        conn.connect(user, password, wait=True)
    except Exception as e:
        print(e)
        raise(e)
    return conn

def notify_process_message(queue=_queue):
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

        
        print("msg json:")
        print(msg_json)
        message = json.dumps(msg_json)
        conn = get_process_mq_connection()
        conn.send(queue, message, headers = {"persistent": "true"})
        print("MESSAGE TO QUEUE create_initial_queue_message")
        print(message)
    except Exception as e:
        print(e)
        raise(e)
    return message

def get_drs_mq_connection():
    print("************************ MQUTILS - GET_DRS_MQ_CONNECTION *******************************")
    try:
        host = os.getenv('DRS_MQ_HOST')
        port = os.getenv('DRS_MQ_PORT')
        user = os.getenv('DRS_MQ_USER')
        password = os.getenv('DRS_MQ_PASSWORD')

        conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
        conn.set_ssl([(host, port)])
        conn.connect(user, password, wait=True)
    except Exception as e:
        print(e)
        raise(e)
    return conn

