import sys, os, logging, stomp, time, datetime, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import mqutils as mqutils
import mqlistener as mqlistener
from mqexception import MQException

logging.basicConfig(filename='/home/appuser/logs/endtoend.log', level=logging.DEBUG)
    
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
            "message": "Message"
        }

        logging.debug("********SENDING SAMPLE MESSAGE TO PROCESS QUEUE*******")
        logging.debug(msg_json)
        logging.debug("**********************************")
        message = json.dumps(msg_json)
        connection_params = mqutils.get_process_mq_connection()
        connection_params.conn.send(os.getenv('PROCESS_QUEUE_CONSUME_NAME'), message, headers = {"persistent": "true"})
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

        logging.debug("********SENDING DRS INGEST MESSAGE TO DRS TOPIC*******")
        logging.debug(msg_json)
        logging.debug("**********************************")
        message = json.dumps(msg_json)
        message = json.dumps(msg_json)
        connection_params = mqutils.get_drs_mq_connection()
        connection_params.conn.send(os.getenv('DRS_QUEUE_NAME'), message, headers = {"persistent": "true"})
    except Exception as e:
        print(e)
        raise(e)
    return message

def notify_ingest_status_process_message():
    '''Creates a dummy queue json message to notify the dims of the 
    final ingest status.  '''
    message = "No message"
    try:
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat()
       
        #Add more details that will be needed from the load report.
        msg_json = {
            "package_id": "12345",
            "application_name": "DVN",
            "batch_ingest_status": "success",
            "message": "Success"
        }

        logging.debug("********DRS INGEST STATUS MESSAGE TO PROCESS QUEUE*******")
        logging.debug(msg_json)
        logging.debug("**********************************")
        message = json.dumps(msg_json)
        connection_params = mqutils.get_process_mq_connection()
        connection_params.conn.send(os.getenv('PROCESS_QUEUE_PUBLISH_NAME'), message, headers = {"persistent": "true"})
        print("MESSAGE TO QUEUE notify_ingest_status_process_message")
        print(message)
    except Exception as e:
        print(e)
        raise(e)
    return message


if __name__ == "__main__":
    notify_data_ready_process_message()