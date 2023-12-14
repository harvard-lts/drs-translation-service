from celery import Celery
import os
import shutil
import os.path
import time
from celery import Task

app1 = Celery('tasks')
app1.config_from_object('celeryconfig')

class WatchForTask(Task):
    name = os.getenv("ETD_HOLDING_TASK_NAME")
    def run(self):
        dropbox_name_for_testing=os.getenv("TEST_DROPBOX_NAME", "")
        # Real dropboxes us the 'incoming' directory
        if dropbox_name_for_testing != "":
            dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")

        batch_dir = os.path.join(base_dropbox_dir, dropbox_name_for_testing, "test-etd-holding-task-batch")
        mock_lr_name = "LOADREPORT_{}.txt".format(os.path.basename(batch_dir))
        mock_lr = os.path.join(base_load_report_dir, dropbox_name_for_testing, os.path.basename(batch_dir), mock_lr_name)
        f = open(mock_lr, "w")
        f.write("Load report data")
        f.close()

app2 = Celery('tasks')
app2.config_from_object('etdceleryconfig')
app2.tasks.register(WatchForTask())

base_dropbox_dir = os.getenv("BASE_DROPBOX_PATH")
base_load_report_dir = os.getenv("BASE_LOADREPORT_PATH")

# @app2.task(bind=True, serializer='json', name=os.getenv("ETD_HOLDING_TASK_NAME"), max_retries=3, acks_late=True, autoretry_for=(Exception,))
# def watch_for_task(self, message):
#     dropbox_name_for_testing=os.getenv("TEST_DROPBOX_NAME", "")
#     # Real dropboxes us the 'incoming' directory
#     if dropbox_name_for_testing != "":
#         dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")

#     batch_dir = os.path.join(base_dropbox_dir, dropbox_name_for_testing, "test-etd-holding-task-batch")
#     mock_lr_name = "LOADREPORT_{}.txt".format(os.path.basename(batch_dir))
#     mock_lr = os.path.join(base_load_report_dir, dropbox_name_for_testing, os.path.basename(batch_dir), mock_lr_name)
#     f = open(mock_lr, "w")
#     f.write("Load report data")
#     f.close()

def test_send_to_drs_task():
    loc = "/home/appuser/tests/data/doi-translation-service-test"
    dropbox_name_for_testing=os.getenv("TEST_DROPBOX_NAME", "")
    # Real dropboxes us the 'incoming' directory
    if dropbox_name_for_testing != "":
        dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
        
    package_dir = os.path.join(base_dropbox_dir, dropbox_name_for_testing, os.path.basename(loc))
        
    # Copy the data from the loc to the dropbox
    shutil.copytree(loc, package_dir)
    
    process_task = os.getenv('PROCESS_TASK_NAME', 'dts.tasks.prepare_and_send_to_drs')

    arguments = {"package_id": "doi-translation-service-test",
                 "application_name": "Dataverse",
                 "destination_path": base_dropbox_dir,
                 "admin_metadata":
                    {"dropbox_name": "", 
                     "original_queue": "myqueue",
                     "task_name": process_task,
                     "retry_count":0,
                     'failureEmail': os.getenv("DEFAULT_EMAIL_RECIPIENT")},
                 "testing":"yes"}    
        
    res = app1.send_task(process_task,
                         args=[arguments], kwargs={},
                         queue=os.getenv("PROCESS_CONSUME_QUEUE_NAME"))
    
    batch_dir = os.path.join(base_dropbox_dir, dropbox_name_for_testing, os.path.basename(loc)+"-batch")
    mock_lr_name = "LOADREPORT_{}.txt".format(os.path.basename(batch_dir))
    mock_lr = os.path.join(base_load_report_dir, dropbox_name_for_testing, os.path.basename(batch_dir), mock_lr_name)
    
    counter = 0
    # Try for 60 seconds then fail
    while not os.path.exists(mock_lr):
        time.sleep(2)
        counter = counter + 2
        if counter >= 60:
            #Remove the files
            cleanup_dropbox(batch_dir)
            #Remove the files
            cleanup_dropbox(package_dir)
            #Remove the files
            cleanup_mock_loadreport(mock_lr)
            assert False, "test_notification: could not find anything on the {} after 30 seconds".format(os.getenv("PROCESS_CONSUME_QUEUE_NAME"))
    
    #Check that the loading file exists and the batch exists
    assert os.path.exists(batch_dir)
    assert os.path.exists(mock_lr)
    #Remove the files
    cleanup_dropbox(batch_dir)
    #Remove the files
    cleanup_dropbox(package_dir)
    #Remove the files
    cleanup_mock_loadreport(mock_lr)

def test_etd_holding_task():
    '''Test that writing to the queue works'''
    dropbox_name_for_testing=os.getenv("TEST_DROPBOX_NAME", "")
    # Real dropboxes us the 'incoming' directory
    if dropbox_name_for_testing != "":
        dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")

    etd_holding_task = os.getenv("ETD_HOLDING_TASK_NAME")

    arguments = {"package_id": "etd-holding-test",
                 "application_name": "ETD",
                 "destination_path": base_dropbox_dir,
                 "object_id": "etd-holding-test-object-id",
                 "pqid": "etd-holding-test-pqid",
                 "testing":"yes"}    
    
    app2.control.add_consumer(os.getenv("ETD_HOLDING_QUEUE_NAME"), reply=True)   
    res = app2.send_task(etd_holding_task,
                         args=[arguments], kwargs={},
                         queue=os.getenv("ETD_HOLDING_QUEUE_NAME"))
    
    batch_dir = os.path.join(base_dropbox_dir, dropbox_name_for_testing, "test-etd-holding-task-batch")
    mock_lr_name = "LOADREPORT_{}.txt".format(os.path.basename(batch_dir))
    mock_lr = os.path.join(base_load_report_dir, dropbox_name_for_testing, os.path.basename(batch_dir), mock_lr_name)
    
    counter = 0
    # Try for 60 seconds then fail
    while not os.path.exists(mock_lr):
        time.sleep(2)
        counter = counter + 2
        if counter >= 60:
            #Remove the files
            cleanup_dropbox(batch_dir)
            #Remove the files
            cleanup_mock_loadreport(mock_lr)
            assert False, "test_notification: could not find anything on the {} after 30 seconds".format(os.getenv("ETD_HOLDING_QUEUE_NAME"))
    
    #Check that the loading file exists and the batch exists
    assert os.path.exists(batch_dir)
    assert os.path.exists(mock_lr)
    #Remove the files
    cleanup_dropbox(batch_dir)
    #Remove the files
    cleanup_mock_loadreport(mock_lr)
    
def cleanup_dropbox(batch_dir):
    '''Removes the batch or package from the dropbox'''
    try:
        shutil.rmtree(batch_dir)
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))
        
def cleanup_mock_loadreport(mock_lr):
    '''Removes the batch from the dropbox'''
    try:
        os.remove(mock_lr)
        os.rmdir(os.path.dirname(mock_lr))
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))
