import datetime, json, os, time, traceback, stomp, sys

# Subscription id is unique to the subscription in this case there is only one subscription per connection
_sub_id = 1
_reconnect_attempts = 0
_max_attempts = 1000

def connect_and_subscribe(connection_params):
    print("************************ MQUTILS MQLISTENER - CONNECT_AND_SUBSCRIBE *******************************")
    global _reconnect_attempts
    _reconnect_attempts = _reconnect_attempts + 1
    if _reconnect_attempts <= _max_attempts:
        # TODO: Retry timer with exponential backoff
        time.sleep(1)
        try:
            connection_params.conn.set_ssl([(connection_params.host, connection_params.port)])
            if not connection_params.conn.is_connected():
                connection_params.conn.connect(connection_params.user, connection_params.password, wait=True)
                print(f'connect_and_subscribe connecting {connection_params.queue} to with connection id 1 reconnect attempts: {_reconnect_attempts}', flush=True)
            else:
                print(f'connect_and_subscibe already connected {connection_params.queue} to with connection id 1 reconnect attempts {_reconnect_attempts}', flush=True)
        except Exception as e:
            print('Exception on disconnect. reconnecting...')
            print(traceback.format_exc())
            connect_and_subscribe(connection_params)
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
        self.message_data = json.loads(body)
        

        #TODO- Handle
        print(' message_data {}'.format(self.message_data))
        print(' message_id {}'.format(self.message_id))

    def on_disconnected(self):
        print('disconnected! reconnecting...')
        connect_and_subscribe(self.connection_params)
        
    def get_connection(self):
        return self.connection_params.conn
    
    def get_message_data(self):
        return self.message_data
    
    def get_message_id(self):
        return self.message_id

class ConnectionParams:
    def __init__(self, conn, queue, host, port, user, password):
        self.conn = conn
        self.queue = queue
        self.host = host
        self.port = port
        self.user = user
        self.password = password
         

def initialize_drslistener():
    mqlistener = get_drsmqlistener()
    conn = mqlistener.get_connection()
    conn.set_listener('', mqlistener)
    connect_and_subscribe(mqlistener.connection_params)
    # http_clients://github.com/jasonrbriggs/stomp.py/issues/206
    while True:
        time.sleep(2)
        if not conn.is_connected():
            print('Disconnected in loop, reconnecting')
            connect_and_subscribe(mqlistener.connection_params)

def initialize_processlistener():
    mqlistener = get_processmqlistener()
    conn = mqlistener.get_connection()
    conn.set_listener('', mqlistener)
    connect_and_subscribe(mqlistener.connection_params)
    # http_clients://github.com/jasonrbriggs/stomp.py/issues/206
    while True:
        time.sleep(2)
        if not conn.is_connected():
            print('Disconnected in loop, reconnecting')
            connect_and_subscribe(mqlistener.connection_params)

def get_drsmqlistener():
    host = os.getenv('DRS_MQ_HOST')
    port = os.getenv('DRS_MQ_PORT')
    user = os.getenv('DRS_MQ_USER')
    password = os.getenv('DRS_MQ_PASSWORD')
    drs_queue = os.getenv('DRS_QUEUE_NAME')
    conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
    connection_params = ConnectionParams(conn, drs_queue, host, port, user, password)
    mqlistener = MqListener(connection_params)
    return mqlistener

def get_processmqlistener():
    host = os.getenv('PROCESS_MQ_HOST')
    port = os.getenv('PROCESS_MQ_PORT')
    user = os.getenv('PROCESS_MQ_USER')
    password = os.getenv('PROCESS_MQ_PASSWORD')
    process_queue = os.getenv('PROCESS_QUEUE_NAME')
    conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
    connection_params = ConnectionParams(conn, process_queue, host, port, user, password)
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