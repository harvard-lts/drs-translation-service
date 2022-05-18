import requests, sys, os
sys.path.append('app')

dts_endpoint = os.getenv("DTS_ENDPOINT")

def test_valid_loadreport_call():
    response = requests.get("https://localhost:8443/loadreport?filename=abc", verify=False)
    assert response.status_code == 200
    
def test_invalid_loadreport_call():
    response = requests.get("https://localhost:8443/loadreport", verify=False)
    assert response.status_code == 400

def test_valid_batchfailed_call():
    response = requests.get("https://localhost:8443/failedBatch?batchName=abc", verify=False)
    assert response.status_code == 200
    
def test_invalid_batchfailed_call():
    response = requests.get("https://localhost:8443/failedBatch", verify=False)
    assert response.status_code == 400