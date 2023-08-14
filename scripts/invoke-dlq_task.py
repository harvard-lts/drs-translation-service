from celery import Celery
import os

app1 = Celery('tasks')
app1.config_from_object('celeryconfig')

transfer_task = os.getenv('PROCESS_TASK_NAME', 'dts.tasks.prepare_and_send_to_drs')

arguments = {
            'dlq_testing': "true",
            }

res = app1.send_task(transfer_task,
                     args=[arguments], kwargs={},
                     queue=os.getenv("PROCESS_CONSUME_QUEUE_NAME"))
