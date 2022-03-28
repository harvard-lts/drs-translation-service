import sys, os, logging, time, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import mqutils as mqutils
import mqlistener as mqlistener

logging.basicConfig(format='%(message)s')

def test_get_process_mq_connection():
    connection_params = mqutils.get_process_mq_connection()
    assert connection_params.conn is not None

def test_notification():
    '''Sends a status message to the process queue and verifies that it made it'''
    #Send the message
    message = mqutils.notify_process_message("/queue/drs-ingest-status-testing")
    assert type(message) is str
    messagedict = json.loads(message)
    
    mqlistenerobject = mqlistener.get_processmqlistener("/queue/drs-ingest-status-testing")
    
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
            assert False, "test_notification: could not find anything on the queue after 30 seconds"
    #dequeue the message
    conn.ack(mqlistenerobject.get_message_id(), 1)    
    assert mqlistenerobject.get_message_data() is not None
    assert type(mqlistenerobject.get_message_data()) is dict
    assert mqlistenerobject.get_message_data() == messagedict
