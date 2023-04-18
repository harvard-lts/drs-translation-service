import mqresources.mqutils as mqutils
import os, logging

def send_error_notification(subject, body, recipients=None):
    logging.getLogger('dts').error(body)
    queue = os.getenv("EMAIL_QUEUE_NAME")
    subject = "DTS: " + subject   
    default_email_recipient = os.getenv("DEFAULT_EMAIL_RECIPIENT")
    if recipients is None:
        recipients = default_email_recipient
    else:
        recipients += "," + default_email_recipient
    return mqutils.notify_email_message(subject, body, recipients, queue)