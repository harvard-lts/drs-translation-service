import requests, sys, os
sys.path.append('app')

dts_endpoint = os.getenv("DTS_ENDPOINT")

def test_valid_loadreport_call():
    response = requests.get( dts_endpoint + "/loadreport?filename=abc", verify=False)
    assert response.status_code == 200
    
def test_invalid_loadreport_call():
    response = requests.get(dts_endpoint + "/loadreport", verify=False)
    assert response.status_code == 400

def test_valid_batchfailed_call():
    response = requests.get(dts_endpoint + "/failedBatch?batchName=abc", verify=False)
    assert response.status_code == 200
    
def test_invalid_batchfailed_call():
    response = requests.get(dts_endpoint + "/failedBatch", verify=False)
    assert response.status_code == 400