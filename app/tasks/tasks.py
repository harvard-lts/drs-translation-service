from celery import Celery
from kombu import Queue
import os
import traceback
import logging
import translation_service.translation_service as translation_service
from translation_service.translation_exceptions import TranslationException
import notifier.notifier as notifier

app = Celery()
app.config_from_object('celeryconfig')

process_task = os.getenv('PROCESS_TASK_NAME', 'dts.tasks.prepare_and_send_to_drs')
process_status_task = os.getenv('PROCESS_STATUS_TASK_NAME', 'dims.tasks.handle_process_status')
retries = int(os.getenv('MESSAGE_MAX_RETRIES', 3))

logger = logging.getLogger('dts')

@app.task(bind=True, serializer='json', name=process_task, max_retries=retries, acks_late=True, autoretry_for=(Exception,))
def prepare_and_send_to_drs(self, message):
    logger.debug("retries {}".format(self.request.retries))
    try:
        testing = False
        if "testing" in message:
            testing = True
        # This calls a method to handle prepping the batch for distribution to the DRS
        translation_service.prepare_and_send_to_drs(
            os.path.join(
                message["destination_path"],
                message["package_id"]
            ),
            message['admin_metadata'],
            message['application_name'],
            testing
        )
    except TranslationException as te:
        emails = message["admin_metadata"].get("failureEmail")
        if te.emailaddress:
            if emails is not None:
                emails += "," + te.emailaddress
            else:
                emails = te.emailaddress
        exception_msg = traceback.format_exc()
        send_error_notifications(message, te, exception_msg, emails, self.request.retries)
    except Exception as e:
        failureEmail = message["admin_metadata"].get("failureEmail")
        exception_msg = traceback.format_exc()
        send_error_notifications(message, e, exception_msg, failureEmail, self.request.retries)   
    

def send_error_notifications(message_body, exception, exception_msg, emails, num_retries):
    package_id = message_body.get("package_id")
    if "doi" in package_id:
        application_name = "Dataverse"
    else:
        application_name = "ePADD"

    msg_json = {
        "package_id": package_id,
        "application_name": application_name,
        "batch_ingest_status": "failed",
        "admin_metadata": {
            "original_queue": os.getenv("PROCESS_PUBLISH_QUEUE_NAME"),
            "task_name": process_status_task,
            "retry_count": 0
        }
    }
    publish_queue = Queue(
        os.getenv("PROCESS_PUBLISH_QUEUE_NAME"), no_declare=True)
    app.send_task(process_status_task, args=[msg_json], kwargs={},
            queue=publish_queue)
    
    msg = "Could not process export for DRSIngest for {}.  Error {}.".format(message_body.get("package_id"), str(exception))
    body = msg + "\n" + exception_msg
    notifier.send_error_notification(str(exception), body, emails)
    
    #If too many retries happened
    if num_retries == retries: 
        send_max_retry_notifications(message_body)

def send_max_retry_notifications(message_body):
    subject = "Maximum resubmitting retries reached for message with id {}.".format(message_body.get("package_id"))
    body = "Maximum resubmitting retries reached for message with id {}.\n\n" \
        "The message has been consumed and will not be resubmitted again.".format(message_body.get("package_id"))
    notifier.send_error_notification(subject, body)