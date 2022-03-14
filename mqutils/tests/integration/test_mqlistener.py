import sys, os, pytest, logging, stomp, time, datetime, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import mqutils as mqutils
import mqlistener as mqlistener

logging.basicConfig(format='%(message)s')

def test_drs_listener():
    '''Tests to see if the listener picks up a topic from the queue'''
    mqlistenerobject = mqlistener.get_drsmqlistener()
    
    conn = mqlistenerobject.get_connection()
    conn.set_listener('', mqlistenerobject)
    mqlistener.connect_and_subscribe(mqlistenerobject.connection_params)
    
    counter = 0
    #Try for 30 seconds then fail
    while mqlistenerobject.get_message_data() is None:
        time.sleep(2)
        counter = counter+2
        if not conn.is_connected():
            mqlistener.connect_and_subscribe(mqlistenerobject.connection_params)
        if counter >= 30:
            assert False, "Could not find anything on the queue after 30 seconds"
        
    assert mqlistenerobject.get_message_data() is not None
    assert type(mqlistenerobject.get_message_data()) is dict
    
def test_process_listener():
    message = notify_data_ready_process_message()
    messagedict = json.loads(message)
    
    '''Tests to see if the listener picks up a message from the process queue'''
    mqlistenerobject = mqlistener.get_processmqlistener()
    
    conn = mqlistenerobject.get_connection()
    conn.set_listener('', mqlistenerobject)
    mqlistener.connect_and_subscribe(mqlistenerobject.connection_params)
    
    counter = 0
    #Try for 30 seconds then fail
    while mqlistenerobject.get_message_data() is None:
        time.sleep(2)
        counter = counter+2
        if not conn.is_connected():
            mqlistener.connect_and_subscribe(mqlistenerobject.connection_params)
        if counter >= 30:
            assert False, "Could not find anything on the queue after 30 seconds"
    
    conn.ack(mqlistenerobject.get_message_id(), 1)    
    assert mqlistenerobject.get_message_data() is not None
    assert type(mqlistenerobject.get_message_data()) is dict
    assert mqlistenerobject.get_message_data() == messagedict
    
def notify_data_ready_process_message():
    '''Creates a dummy queue json message to notify the queue that the 
    DVN data is ready to process.  This is normally placed on the queue by
    the DRS Import Management Service'''
    message = "No message"
    try:
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat()
       
        #Add more details that will be needed from the load report.
        msg_json = {
            "package_id": "12345",
            "application_name": "DVN",
            "dropbox_path": "/path/to/object",
            "notes": "Some Notes",
            "timestamp": timestamp, 
        }

        queue = os.getenv('PROCESS_QUEUE_NAME')
        print("msg json:")
        print(msg_json)
        message = json.dumps(msg_json)
        conn = mqutils.get_mq_connection()
        conn.send(queue, message, headers = {"persistent": "true"})
        print("MESSAGE TO QUEUE create_initial_queue_message")
        print(message)
    except Exception as e:
        print(e)
        raise(e)
    return message