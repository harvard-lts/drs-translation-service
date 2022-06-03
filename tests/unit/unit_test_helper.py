import requests, sys, os, shutil
sys.path.append('app')
    
dropbox_path = os.getenv("DROPBOX_PATH")
sample_load_report="LOADREPORT_sample.txt"
load_report_path = os.getenv("LOADREPORT_PATH")

def deposit_sample_load_report():
    '''Creates a sample load report'''
    sourcepath = os.path.join("/home/appuser/tests/data/sampleloadreport/", sample_load_report)
    os.makedirs(os.path.join(load_report_path, "sample"), exist_ok=True)
    try:
        shutil.copyfile(sourcepath, os.path.join(load_report_path, "sample", sample_load_report))
    except OSError as e:
        print("Error during copy: %s : %s" % (os.path.join(load_report_path, "sample", sample_load_report), e.strerror))
        
def cleanup_sample_load_report():
    '''Removes the sample load report'''
    try:
        shutil.rmtree(os.path.join(load_report_path, "sample"))
    except OSError as e:
        print("Error during cleanup: %s : %s" % (os.path.join(load_report_path, "sample", sample_load_report), e.strerror))
        
def create_sample_failed_batch():
    '''Creates a sample failed batch'''
    failed_batch_file = os.path.join(dropbox_path, "sample", "batch.xml.failed")
    os.makedirs(os.path.join(dropbox_path, "sample"), exist_ok=True)
    open(failed_batch_file, 'a').close()

def cleanup_sample_failed_batch():
    '''Removes the newly failed batch'''
    try:
        shutil.rmtree(os.path.join(dropbox_path, "sample"))
    except OSError as e:
        print("Error during cleanup: %s : %s" % (os.path.join(dropbox_path, "sample/batch.xml.failed"), e.strerror))