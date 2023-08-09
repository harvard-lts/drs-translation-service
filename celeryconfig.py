import os
from kombu import Exchange, Queue

broker_url = os.getenv('BROKER_URL')
broker_connection_retry_on_startup=True
task_serializer = 'json'
accept_content = ['application/json']
result_serializer = 'json'
timezone = 'US/Eastern'
enable_utc = True
worker_enable_remote_control = False

#DLQ Routing
dead_letter_queue_option = {
    'x-dead-letter-exchange': os.getenv("DLQ_EXCHANGE_NAME"),
    'x-dead-letter-routing-key': os.getenv("DLQ_QUEUE_NAME"),
    'x-message-ttl': int(os.getenv('MESSAGE_EXPIRATION_MS', 3600000))
}

# Set the default exchange to the same as the queue name
default_exchange = Exchange(os.getenv("PROCESS_CONSUME_QUEUE_NAME"), type='direct')

# Create the Queue and pass the DLQ options to it
# This will route any failed messages to the DLQ
default_queue = Queue(
    os.getenv("PROCESS_CONSUME_QUEUE_NAME"),
    default_exchange,
    routing_key=os.getenv("PROCESS_CONSUME_QUEUE_NAME"),
    queue_arguments=dead_letter_queue_option)
 
task_queues = [default_queue]
task_routes = {
    'dts.tasks.prepare_and_send_to_drs':
        {'queue': os.getenv("PROCESS_CONSUME_QUEUE_NAME")}
}
