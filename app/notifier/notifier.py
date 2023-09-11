from celery import Celery
import os
import logging

app1 = Celery()
app1.config_from_object('celeryconfig')


def send_error_notification(subject, body, recipients=None):
    logging.getLogger('dts').error(body)
    queue = os.getenv("EMAIL_NOTIFIER_QUEUE_NAME")
    subject = "DTS: " + subject
    default_email_recipient = os.getenv("DEFAULT_EMAIL_RECIPIENT")
    if recipients is None:
        recipients = default_email_recipient
    else:
        recipients += "," + default_email_recipient
    arguments = {"subject": subject, "body": body,
                 "recipients": recipients}
    NOTIFIER_TASK_NAME = os.getenv("EMAIL_NOTIFIER_TASK_NAME",
                                   "rabbitmq-email-notifier." +
                                   "tasks.notify_email_message")
    return app1.send_task(NOTIFIER_TASK_NAME, args=[arguments], kwargs={},
                          queue=queue)
