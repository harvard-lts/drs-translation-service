import requests, sys, os, shutil
sys.path.append('app')
    
sample_load_report="LOADREPORT_sample.txt"
base_dropbox_dir = os.getenv("BASE_DROPBOX_PATH")
base_load_report_dir = os.getenv("BASE_LOADREPORT_PATH")
test_dropbox_name=os.getenv("TEST_DROPBOX_NAME", "")

def deposit_sample_load_report():
    '''Creates a sample load report'''
    sourcepath = os.path.join("/home/appuser/tests/data/sampleloadreport/", sample_load_report)
    os.makedirs(os.path.join(base_load_report_dir, test_dropbox_name, "sample"), exist_ok=True)
    try:
        shutil.copyfile(sourcepath, os.path.join(base_load_report_dir, test_dropbox_name, "sample", sample_load_report))
    except OSError as e:
        print("Error during copy: %s : %s" % (os.path.join(base_load_report_dir, test_dropbox_name, "sample", sample_load_report), e.strerror))
        
def cleanup_sample_load_report():
    '''Removes the sample load report'''
    try:
        shutil.rmtree(os.path.join(base_load_report_dir, test_dropbox_name, "sample"))
    except OSError as e:
        print("Error during cleanup: %s : %s" % (os.path.join(base_load_report_dir, test_dropbox_name, "sample", sample_load_report), e.strerror))
        
def create_sample_failed_batch():
    '''Creates a sample failed batch'''
    failed_batch_file = os.path.join(base_dropbox_dir, test_dropbox_name, "sample", "batch.xml.failed")
    os.makedirs(os.path.join(base_dropbox_dir, test_dropbox_name, "sample"), exist_ok=True)
    open(failed_batch_file, 'a').close()

def cleanup_sample_failed_batch():
    '''Removes the newly failed batch'''
    try:
        shutil.rmtree(os.path.join(base_dropbox_dir, test_dropbox_name, "sample"))
    except OSError as e:
        print("Error during cleanup: %s : %s" % (os.path.join(base_dropbox_dir, test_dropbox_name, "sample/batch.xml.failed"), e.strerror))