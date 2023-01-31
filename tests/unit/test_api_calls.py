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
    
    unprocessed = ["/home/appuser/tests/data/unprocessed"]
    exports = json.dumps(unprocessed)
    payload = {"unprocessed_exports": exports, "dryrun": True}
        
    response = requests.get("https://localhost:8443/reprocess_batches", params=payload, verify=False)
    assert response.status_code == 200
    
    
        