import pytest, sys, os.path, shutil
sys.path.append('app')
import translation_service.translation_service as translation_service 

dropbox = os.getenv("DROPBOX_PATH")
load_report_dir = os.getenv("LOADREPORT_PATH")
   
def test_prepare_and_send_to_drs():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/doi-translation-service-test"
    package_dir = os.path.join(dropbox, os.path.basename(loc))
    
    #Copy the data from the loc to the dropbox
    shutil.copytree(loc, package_dir)
    
    #Run prepare
    batch_dir = translation_service.prepare_and_send_to_drs(package_dir, {})
    
    #Check that the loading file exists
    assert os.path.exists(os.path.join(batch_dir, "LOADING"))
    
    #Remove the files
    cleanup_batch(batch_dir)

def test_prepare_and_create_mock_lr():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/doi-translation-service-test"
    package_dir = os.path.join(dropbox, os.path.basename(loc))
    
    #Copy the data from the loc to the dropbox
    shutil.copytree(loc, package_dir)
    
    #Run prepare
    batch_dir = translation_service.prepare_and_send_to_drs(package_dir, {}, True)
    
    mock_lr_name = "LOADREPORT_{}.txt".format(os.path.basename(batch_dir))
    mock_lr = os.path.join(load_report_dir, os.path.basename(batch_dir), mock_lr_name)
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