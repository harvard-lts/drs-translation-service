import sys, os, logging, time, datetime, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import mqutils as mqutils
import mqlistener as mqlistener

logging.basicConfig(format='%(message)s')

_process_queue = "/queue/dvn-data-ready-testing"
_drs_queue = "/topic/dvn-dev-DRS_OBJECT_UPDATED"

def test_drs_listener():
    '''Tests to see if the listener picks up a topic from the queue'''
    mqlistenerobject = mqlistener.get_drsmqlistener(_drs_queue)
    
    conn = mqlistenerobject.get_connection()
    conn.set_listener('', mqlistenerobject)
    mqlistener.subscribe_to_listener(mqlistenerobject.connection_params)
    
    message = notify_drs_message()
    messagedict = json.loads(message)
    
    counter = 0
    #Try for 30 seconds then fail
    while mqlistenerobject.get_message_data() is None:
        time.sleep(2)
        counter = counter+2
        if not conn.is_connected():
            mqlistener.subscribe_to_listener(mqlistenerobject.connection_params)
        if counter >= 30:
            assert False, "test_drs_listener: could not find anything on the queue after 30 seconds"
        
    assert mqlistenerobject.get_message_data() is not None
    assert type(mqlistenerobject.get_message_data()) is dict
    assert mqlistenerobject.get_message_data() == messagedict
    
def test_process_listener():
    message = notify_data_ready_process_message()
    messagedict = json.loads(message)
    
    '''Tests to see if the listener picks up a message from the process queue'''
    mqlistenerobject = mqlistener.get_processmqlistener(_process_queue)
    
    conn = mqlistenerobject.get_connection()
    conn.set_listener('', mqlistenerobject)
    mqlistener.subscribe_to_listener(mqlistenerobject.connection_params)
    
    counter = 0
    #Try for 30 seconds then fail
    while mqlistenerobject.get_message_data() is None:
        time.sleep(2)
        counter = counter+2
        if not conn.is_connected():
            mqlistener.subscribe_to_listener(mqlistenerobject.connection_params)
        if counter >= 30:
            assert False, "test_process_listener: could not find anything on the queue after 30 seconds"
    
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

        #Add more details that will be needed from the load report.
        msg_json = {
            "package_id": "12345",
            "application_name": "DVN",
            "dropbox_path": "/path/to/object",
            "notes": "Some Notes",
            "timestamp": timestamp, 
        }

        print("msg json:")
        print(msg_json)
        message = json.dumps(msg_json)
        connection_params = mqutils.get_process_mq_connection(_process_queue)
        connection_params.conn.send(_process_queue, message, headers = {"persistent": "true"})
        print("MESSAGE TO QUEUE notify_data_ready_process_message")
        print(message)
    except Exception as e:
        print(e)
        raise(e)
    return message

def notify_drs_message():
    '''Creates a dummy queue drs json message This is normally placed on the topic by
    the DRS Ingest'''
    message = "No message"
    try:
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat()
       
        #Sample DRS Ingest message.
        msg_json = {"data":
                    {"objectId":123,
                     "contentModel":"CMID-5.0",
                     "accessFlag":"N",
                     "isFile":"false",
                     "ocflObjectKey":"12345678",
                     "ocflObjectPath":"/8765/4321/12345678",
                     "primaryUrn":"URN-3.HUL.ARCH:123456",
                     "status":"current"}
                    }

        print("msg json:")
        print(msg_json)
        message = json.dumps(msg_json)
        connection_params = mqutils.get_drs_mq_connection(_drs_queue)
        connection_params.conn.send(_drs_queue, message, headers = {"persistent": "true"})
        print("MESSAGE TO QUEUE notify_drs_message")
        print(message)
    except Exception as e:
        print(e)
        raise(e)
    return message

if __name__ == "__main__":
    notify_data_ready_process_message()
