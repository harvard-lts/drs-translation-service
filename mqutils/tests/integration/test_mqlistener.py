import sys, os, pytest, logging, stomp, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
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