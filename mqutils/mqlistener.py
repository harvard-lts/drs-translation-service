import json, time, traceback, stomp, sys, os, logging
import mqutils
import mqexception

# Subscription id is unique to the subscription in this case there is only one subscription per connection
_sub_id = 1
_reconnect_attempts = 0
_max_attempts = 1000

logfile=os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel)

def subscribe_to_listener(connection_params):
    logging.debug("************************ MQUTILS MQLISTENER - CONNECT_AND_SUBSCRIBE *******************************")
    global _reconnect_attempts
    _reconnect_attempts = _reconnect_attempts + 1
    if _reconnect_attempts <= _max_attempts:
        # TODO: Retry timer with exponential backoff
        time.sleep(1)
        try:
            if not connection_params.conn.is_connected():
                connection_params.conn.connect(connection_params.user, connection_params.password, wait=True)
                logging.debug(f'subscribe_to_listener connecting {connection_params.queue} to with connection id 1 reconnect attempts: {_reconnect_attempts}')
            else:
                logging.debug(f'connect_and_subscibe already connected {connection_params.queue} to with connection id 1 reconnect attempts {_reconnect_attempts}')
        except Exception:
            logging.debug('Exception on disconnect. reconnecting...')
            logging.debug(traceback.format_exc())
            subscribe_to_listener(connection_params)
        else:
            if (connection_params.ack is not None):
                connection_params.conn.subscribe(destination=connection_params.queue, id=1, ack=connection_params.ack)
            else:
                connection_params.conn.subscribe(destination=connection_params.queue, id=1, ack='client-individual')
            _reconnect_attempts = 0
    else:
        logging.error('Maximum reconnect attempts reached for this connection. reconnect attempts: {}'.format(_reconnect_attempts))


class MqListener(stomp.ConnectionListener):
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.message_data = None
        self.message_id = None

    def on_error(self, frame):
        logging.debug('received an error "%s"' % frame.body)

    def on_message(self, frame):
        logging.debug("************************ MQUTILS MQLISTENER - ON_MESSAGE *******************************")
        headers, body = frame.headers, frame.body
        logging.debug('received a message headers "%s"' % headers)
        logging.debug('message body "%s"' % body)

        self.message_id = headers.get('message-id')
        try: 
            self.message_data = json.loads(body)
        except json.decoder.JSONDecodeError: 
            raise mqexception.MQException("Incorrect formatting of message detected.  Required JSON but received {} ".format(body))
        
        if self.connection_params.queue == os.getenv('PROCESS_QUEUE_CONSUME_NAME'):
            #Trigger the mock services to 'run the drs ingest'
            mqutils.notify_mock_drs_trigger_message(self.message_data["package_id"])
            #TODO This will call a method to handle prepping the batch for
            #distribution to the DRS
        #This is here to demo end to end testing
        elif self.connection_params.queue == os.getenv('DRS_QUEUE_CONSUME_NAME'):
            #Send ingest status message to process queue 
            #TODO - this will have to get pull the actual URN once it is available
            urn = "https://nrs-dev.lts.harvard.edu/URN-3:HUL.TEST:101113553"
            mqutils.notify_ingest_status_process_message(self.message_data["package_id"], self.message_data["batch_ingest_status"], urn)
        self.connection_params.conn.ack(self.message_id, 1)

        #TODO- Handle
        logging.debug(' message_data {}'.format(self.message_data))
        logging.debug(' message_id {}'.format(self.message_id))

    def on_disconnected(self):
        logging.debug('disconnected! reconnecting...')
        subscribe_to_listener(self.connection_params)
        
    def get_connection(self):
        return self.connection_params.conn
    
    def get_message_data(self):
        return self.message_data
    
    def get_message_id(self):
        return self.message_id

         

def initialize_drslistener():
    mqlistener = get_drsmqlistener()
    conn = mqlistener.get_connection()
    conn.set_listener('', mqlistener)
    subscribe_to_listener(mqlistener.connection_params)
    # http_clients://github.com/jasonrbriggs/stomp.py/issues/206
    while True:
        time.sleep(2)
        if not conn.is_connected():
            logging.debug('Disconnected in loop, reconnecting')
            subscribe_to_listener(mqlistener.connection_params)

def initialize_processlistener():
    mqlistener = get_processmqlistener()
    conn = mqlistener.get_connection()
    conn.set_listener('', mqlistener)
    subscribe_to_listener(mqlistener.connection_params)
    # http_clients://github.com/jasonrbriggs/stomp.py/issues/206
    while True:
         time.sleep(2)
         if not conn.is_connected():
             logging.debug('Disconnected in loop, reconnecting')
             subscribe_to_listener(mqlistener.connection_params)

def get_drsmqlistener(queue=None):
    connection_params = mqutils.get_drs_mq_connection(queue)
    mqlistener = MqListener(connection_params)
    return mqlistener

def get_processmqlistener(queue=None):
    connection_params = mqutils.get_process_mq_connection(queue)
    mqlistener = MqListener(connection_params)
    return mqlistener

    
if __name__ == "__main__":
    permitted_values = {"drs", "process"}
    args = sys.argv[1:]
    listener = "drs"
    if len(args) >= 1:
        listener = args[0]
     
    if (listener not in permitted_values):
        raise RuntimeError("Argument syntax requires either drs or process for parameters")
     
    if (listener == "drs"):    
        initialize_drslistener()   
    else:
        initialize_processlistener()