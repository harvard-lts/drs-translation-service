import sys, os, pytest, logging, stomp, time, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import mqutils as mqutils
import mqlistener as mqlistener

logging.basicConfig(format='%(message)s')

def test_get_mq_connection():
    mq_conn = None
    mq_conn = mqutils.get_mq_connection()
    assert mq_conn is not None

def test_notification():
    '''Sends a status message to the process queue and verifies that it made it'''
    #Send the message
    message = mqutils.notify_process_message()
    assert type(message) is str
    messagedict = json.loads(message)
    
    mqlistenerobject = get_mqlistener()
    
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
    #dequeue the message
    conn.ack(mqlistenerobject.get_message_id(), 1)    
    assert mqlistenerobject.get_message_data() is not None
    assert type(mqlistenerobject.get_message_data()) is dict
    assert mqlistenerobject.get_message_data() == messagedict
    

def get_mqlistener():
    '''Sets up a listener to make sure that the process message made it onto the queue'''
    host = os.getenv('PROCESS_MQ_HOST')
    port = os.getenv('PROCESS_MQ_PORT')
    user = os.getenv('PROCESS_MQ_USER')
    password = os.getenv('PROCESS_MQ_PASSWORD')
    test_queue = os.getenv('PROCESS_QUEUE_NAME')
    conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
    connection_params = mqlistener.ConnectionParams(conn, test_queue, host, port, user, password)
    mqlistenerobject = mqlistener.MqListener(connection_params)
    return mqlistenerobject