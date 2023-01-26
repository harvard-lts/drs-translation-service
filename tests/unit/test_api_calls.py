import requests, sys, os, json, shutil
sys.path.append('app')
import unit_test_helper

base_dropbox_dir = os.getenv("BASE_DROPBOX_PATH")
base_load_report_dir = os.getenv("BASE_LOADREPORT_PATH")


def test_valid_loadreport_call():
    unit_test_helper.deposit_sample_load_report()
    response = requests.get("https://localhost:8443/loadreport?filename={}&dryrun=True".format(unit_test_helper.sample_load_report), verify=False)
    assert response.status_code == 200
    unit_test_helper.cleanup_sample_load_report()
    
def test_invalid_loadreport_call():
    response = requests.get("https://localhost:8443/loadreport", verify=False)
    assert response.status_code == 400
    
def test_invalid_loadreport_no_such_filename_call():
    response = requests.get("https://localhost:8443/loadreport?filename=abc", verify=False)
    assert response.status_code == 400

def test_valid_batchfailed_call():
    response = requests.get("https://localhost:8443/failedBatch?batchName=sample&dryrun=True", verify=False)
    assert response.status_code == 200
    
def test_invalid_batchfailed_call():
    response = requests.get("https://localhost:8443/failedBatch", verify=False)
    assert response.status_code == 400

def test_invalid_batchfailed_no_such_batch_call():
    response = requests.get("https://localhost:8443/failedBatch?batchName=abc", verify=False)
    # This will work because we are not deleting the dir, when we attempt to delete the dir this will
    # need to be changed back to 400
    assert response.status_code == 200
    
def test_valid_reprocess_call():
    dropbox_name_for_testing=os.getenv("TEST_DROPBOX_NAME", "")
    #Real dropboxes us the 'incoming' directory
    if dropbox_name_for_testing != "":
        dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
    admin_metadata_json = json.dumps({"dropbox_name": dropbox_name_for_testing})
    payload = {"unprocessed_data_path": "/home/appuser/tests/data/doi-translation-service-test", "application_name": "Dataverse", "admin_metadata": admin_metadata_json, "testing": True}
        
    response = requests.get("https://localhost:8443/reprocess_batch", params=payload, verify=False)
    print(response.text)
    cleanup_batch()
    cleanup_batch_builder_files()
    cleanup_mock_loadreport()
    assert response.status_code == 200
    
    
def cleanup_batch():
    '''Removes the batch from the test data'''
    try:
        shutil.rmtree("/home/appuser/tests/data/doi-translation-service-test-batch")
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))

def cleanup_batch_builder_files():
    '''Removes the batch builder files from the project'''
    try:
        shutil.rmtree("/home/appuser/tests/data/doi-translation-service-test/_aux")
        os.remove("/home/appuser/tests/data/doi-translation-service-test/project.conf")
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))

def cleanup_mock_loadreport():
    '''Removes the batch from the dropbox'''
    try:
        mock_lr_dir = os.path.join(base_load_report_dir, "doi-translation-service-test-batch")
        shutil.rmtree(mock_lr_dir)
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))
        