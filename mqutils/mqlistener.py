import datetime, json, time, traceback, stomp, sys
import mqutils
import mqexception

# Subscription id is unique to the subscription in this case there is only one subscription per connection
_sub_id = 1
_reconnect_attempts = 0
_max_attempts = 1000

def subscribe_to_listener(connection_params):
    print("************************ MQUTILS MQLISTENER - CONNECT_AND_SUBSCRIBE *******************************")
    global _reconnect_attempts
    _reconnect_attempts = _reconnect_attempts + 1
    if _reconnect_attempts <= _max_attempts:
        # TODO: Retry timer with exponential backoff
        time.sleep(1)
        try:
            if not connection_params.conn.is_connected():
                connection_params.conn.connect(connection_params.user, connection_params.password, wait=True)
                print(f'subscribe_to_listener connecting {connection_params.queue} to with connection id 1 reconnect attempts: {_reconnect_attempts}', flush=True)
            else:
                print(f'connect_and_subscibe already connected {connection_params.queue} to with connection id 1 reconnect attempts {_reconnect_attempts}', flush=True)
        except Exception as e:
            print('Exception on disconnect. reconnecting...')
            print(traceback.format_exc())
            subscribe_to_listener(connection_params)
        else:
            connection_params.conn.subscribe(destination=connection_params.queue, id=1, ack='client-individual')
            _reconnect_attempts = 0
    else:
        print('Maximum reconnect attempts reached for this connection. reconnect attempts: {}'.format(_reconnect_attempts), flush=True)


class MqListener(stomp.ConnectionListener):
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.message_data = None
        self.message_id = None
        print('MqListener init')

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print("************************ MQUTILS MQLISTENER - ON_MESSAGE *******************************")
        headers, body = frame.headers, frame.body
        print('received a message headers "%s"' % headers)
        print('message body "%s"' % body)

        self.message_id = headers.get('message-id')
        try: 
            self.message_data = json.loads(body)
        except json.decoder.JSONDecodeError: 
            raise mqexception.MQException("Incorrect formatting of message detected.  Required JSON but received {} ".format(body))
        
        self.connection_params.conn.ack(self.message_id, 1)

        #TODO- Handle
        print(' message_data {}'.format(self.message_data))
        print(' message_id {}'.format(self.message_id))

    def on_disconnected(self):
        print('disconnected! reconnecting...')
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
            print('Disconnected in loop, reconnecting')
            subscribe_to_listener(mqlistener.connection_params)

def initialize_processlistener():
    mqlistener = get_processmqlistener()
    conn = mqlistener.get_connection()
    conn.set_listener('', mqlistener)
    subscribe_to_listener(mqlistener.connection_params)
    # http_clients://github.com/jasonrbriggs/stomp.py/issues/206
    while True:
         time.sleep(2)
         counter = counter+2
         if not conn.is_connected():
             print('Disconnected in loop, reconnecting')
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
        raise RuntimeException("Argument syntax requires either drs or process for parameters")
     
    if (listener == "drs"):    
        initialize_drslistener()   
    else:
        initialize_processlistener()