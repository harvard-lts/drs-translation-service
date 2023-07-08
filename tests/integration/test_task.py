from celery import Celery
import os
import shutil
import os.path
import time

app1 = Celery('tasks')
app1.config_from_object('celeryconfig')

base_dropbox_dir = os.getenv("BASE_DROPBOX_PATH")
base_load_report_dir = os.getenv("BASE_LOADREPORT_PATH")

def test_send_to_drs_task():
    loc = "/home/appuser/tests/data/doi-translation-service-test"
    dropbox_name_for_testing=os.getenv("TEST_DROPBOX_NAME", "")
    # Real dropboxes us the 'incoming' directory
    if dropbox_name_for_testing != "":
        dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
        
    package_dir = os.path.join(base_dropbox_dir, dropbox_name_for_testing, os.path.basename(loc))
        
    # Copy the data from the loc to the dropbox
    shutil.copytree(loc, package_dir)
    
    arguments = {"package_id": "doi-translation-service-test",
                 "application_name": "Dataverse",
                 "destination_path": base_dropbox_dir,
                 "admin_metadata":
                 {"dropbox_name": "", "original_queue": "myqueue", "retry_count":0},
                 "testing":"yes"}    
        
    res = app1.send_task('dts.tasks.prepare_and_send_to_drs',
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
            assert False, "test_notification: could not find anything on the {} after 30 seconds".format(drs_queue)
    
    #Check that the loading file exists and the batch exists
    assert os.path.exists(batch_dir)
    assert os.path.exists(mock_lr)
    #Remove the files
    cleanup_dropbox(batch_dir)
    #Remove the files
    cleanup_dropbox(package_dir)
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