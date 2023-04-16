import json
import logging
import os
import sys
import time
from collections import OrderedDict
from unittest.mock import patch

sys.path.append('app/dts_mqresources')
sys.path.append('app/translation_service')
import mqutils
from listener.process_ready_queue_listener import ProcessReadyQueueListener

logging.basicConfig(format='%(message)s')

_process_queue = "/queue/dims-data-ready-testing"


@patch("listener.process_ready_queue_listener.ProcessReadyQueueListener._handle_received_message")
@patch("listener.process_ready_queue_listener.ProcessReadyQueueListener._get_queue_name")
def test_process_listener(get_queue_name_mock, handle_received_message_mock):
    '''Tests to see if the listener picks up a message from the process queue'''
    get_queue_name_mock.return_value = _process_queue
    mq_listener_object = ProcessReadyQueueListener()

    message_json = notify_data_ready_process_message()

    counter = 0
    # Try for 30 seconds then fail
    while not handle_received_message_mock.call_count:
        time.sleep(2)
        counter = counter + 2
        if counter >= 10:
            assert False, "test_listener: could not find anything on the {} after 30 seconds".format(_process_queue)

    args, kwargs = handle_received_message_mock.call_args
    assert type(args[0]) is dict
    assert OrderedDict(args[0]) == OrderedDict(message_json)

    # cleanup the queue and disconnect the listener
    mq_listener_object._acknowledge_message(args[1], args[2])
    mq_listener_object.disconnect()


def notify_data_ready_process_message():
    '''Creates a dummy queue json message to notify the queue that the 
    DVN data is ready to process.  This is normally placed on the queue by
    the DRS Import Management Service'''
    try:
        # Add more details that will be needed from the load report.
        message_json = {
            "package_id": "12345",
            "application_name": "Dataverse",
            "dropbox_path": "/path/to/object",
            "message": "Message"
        }

        # Default to one hour from now
        now_in_ms = int(time.time()) * 1000
        expiration = int(os.getenv('MESSAGE_EXPIRATION_MS', 36000000)) + now_in_ms

        print("msg json:")
        print(message_json)
        message = json.dumps(message_json)
        connection_params = mqutils.get_process_mq_connection(_process_queue)
        connection_params.conn.send(_process_queue, message, headers={"persistent": "true", "expires": expiration})
        print("MESSAGE TO QUEUE notify_data_ready_process_message")
        print(message)
    except Exception as e:
        print(e)
        raise e
    return message_json


if __name__ == "__main__":
    notify_data_ready_process_message()
