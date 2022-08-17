import pytest, sys, os.path, shutil
sys.path.append('app')
import translation_service.translation_service as translation_service 

base_dropbox_dir = os.getenv("BASE_DROPBOX_PATH")
base_load_report_dir = os.getenv("BASE_LOADREPORT_PATH")
test_dropbox_name=os.getenv("TEST_DROPBOX_NAME", "")
   
def test_prepare_and_create_mock_lr():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/doi-translation-service-test"
    
    package_dir = os.path.join(base_dropbox_dir, test_dropbox_name, os.path.basename(loc))
    
    #Copy the data from the loc to the dropbox
    shutil.copytree(loc, package_dir)
    
    #Run prepare
    batch_dir = translation_service.prepare_and_send_to_drs(package_dir, {"application_name": "Dataverse", "dropbox_name": test_dropbox_name}, True)

    mock_lr_name = "LOADREPORT_{}.txt".format(os.path.basename(batch_dir))
    mock_lr = os.path.join(base_load_report_dir, test_dropbox_name, os.path.basename(batch_dir), mock_lr_name)
    #Check that the loading file exists
    assert os.path.exists(mock_lr)
    
    #Remove the files
    cleanup_batch(batch_dir)
    #Remove the files
    cleanup_mock_loadreport(mock_lr)


def cleanup_batch(batch_dir):
    '''Removes the batch from the dropbox'''
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