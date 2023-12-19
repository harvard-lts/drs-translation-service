import requests, sys, os, shutil
sys.path.append('app')
    
sample_load_report="LOADREPORT_sample.txt"
etd_sample_load_report="LOADREPORT_sample_etd.txt"
base_dropbox_dir = os.getenv("BASE_DROPBOX_PATH")
base_load_report_dir = os.getenv("BASE_LOADREPORT_PATH")


def deposit_sample_dvn_load_report():
    '''Creates a sample load report'''
    sourcepath = os.path.join("/home/appuser/tests/data/sampleloadreport/", sample_load_report)
    #Real dropboxes us the 'incoming' directory
    dropbox_name_for_testing = os.getenv("TEST_DROPBOX_NAME", "")
    if dropbox_name_for_testing != "":
        dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
    os.makedirs(os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample"), exist_ok=True)
    try:
        shutil.copyfile(sourcepath, os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample", sample_load_report))
    except OSError as e:
        print("Error during copy: %s : %s" % (os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample", sample_load_report), e.strerror))

def deposit_sample_etd_load_report():
    '''Creates a sample load report'''
    sourcepath = os.path.join("/home/appuser/tests/data/sampleloadreport/", etd_sample_load_report)
    #Real dropboxes us the 'incoming' directory
    dropbox_name_for_testing = os.getenv("TEST_DROPBOX_NAME", "")
    if dropbox_name_for_testing != "":
        dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
    os.makedirs(os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample_etd"), exist_ok=True)
    try:
        shutil.copyfile(sourcepath, os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample_etd", etd_sample_load_report))
    except OSError as e:
        print("Error during copy: %s : %s" % (os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample_etd", etd_sample_load_report), e.strerror))
       
def cleanup_sample_load_report():
    '''Removes the sample load report'''
    try:
        dropbox_name_for_testing = os.getenv("TEST_DROPBOX_NAME", "")
        #Real dropboxes us the 'incoming' directory
        if dropbox_name_for_testing != "":
            dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
        shutil.rmtree(os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample"))
    except OSError as e:
        print("Error during cleanup: %s : %s" % (os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample", sample_load_report), e.strerror))
        
def cleanup_sample_etd_load_report():
    '''Removes the sample load report'''
    try:
        dropbox_name_for_testing = os.getenv("TEST_DROPBOX_NAME", "")
        #Real dropboxes us the 'incoming' directory
        if dropbox_name_for_testing != "":
            dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
        shutil.rmtree(os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample_etd"))
    except OSError as e:
        print("Error during cleanup: %s : %s" % (os.path.join(base_load_report_dir, dropbox_name_for_testing, "sample_etd", etd_sample_load_report), e.strerror))
        
def create_sample_failed_batch():
    '''Creates a sample failed batch'''
    dropbox_name_for_testing = os.getenv("TEST_DROPBOX_NAME", "")
    #Real dropboxes us the 'incoming' directory
    if dropbox_name_for_testing != "":
        dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
    failed_batch_file = os.path.join(base_dropbox_dir, dropbox_name_for_testing, "sample", "batch.xml.failed")
    os.makedirs(os.path.join(base_dropbox_dir, dropbox_name_for_testing, "sample"), exist_ok=True)
    open(failed_batch_file, 'a').close()

def cleanup_sample_failed_batch():
    '''Removes the newly failed batch'''
    try:
        dropbox_name_for_testing = os.getenv("TEST_DROPBOX_NAME", "")
        #Real dropboxes us the 'incoming' directory
        if dropbox_name_for_testing != "":
            dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
        shutil.rmtree(os.path.join(base_dropbox_dir, dropbox_name_for_testing, "sample"))
    except OSError as e:
        print("Error during cleanup: %s : %s" % (os.path.join(base_dropbox_dir, dropbox_name_for_testing, "sample/batch.xml.failed"), e.strerror))