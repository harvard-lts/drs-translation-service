import pytest, sys, os.path, shutil
sys.path.append('app')
import translation_service.translation_service as translation_service 

dropbox = os.getenv("DROPBOX_PATH")
    
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


def cleanup_batch(batch_dir):
    '''Removes the batch from the dropbox'''
    try:
        shutil.rmtree(batch_dir)
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))