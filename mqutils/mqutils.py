import os, json, time, datetime, stomp


_host = os.getenv('PROCESS_MQ_HOST')
_port = os.getenv('PROCESS_MQ_PORT')
_user = os.getenv('PROCESS_MQ_USER')
_password = os.getenv('PROCESS_MQ_PASSWORD')
_queue = os.getenv('PROCESS_QUEUE_NAME')

def get_mq_connection():
    print("************************ MQUTILS - GET_MQ_CONNECTION *******************************")
    try:
        conn = stomp.Connection([(_host, _port)], heartbeats=(40000, 40000), keepalive=True)
        conn.set_ssl([(_host, _port)])
        conn.connect(_user, _password, wait=True)
    except Exception as e:
        print(e)
        raise(e)
    return conn

def notify_process_message():
    '''Creates a queue json message to notify the queue that the drs ingest has finished an ingest attempt'''
    print("************************ MQUTILS - CREATE_PROCESS_MESSAGE *******************************")
    try:
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat()
       
       #Add more details that will be needed from the load report.
        msg_json = {
            "drs_id": 12345,
            "timestamp": timestamp,
            "status": "success",
        }
        
        
        print("msg json:")
        print(msg_json)
        message = json.dumps(msg_json)
        conn = get_mq_connection()
        conn.send(_queue, message, headers = {"persistent": "true"})
        print("MESSAGE TO QUEUE create_initial_queue_message")
        print(message)
    except Exception as e:
        print(e)
        raise(e)
    return message


