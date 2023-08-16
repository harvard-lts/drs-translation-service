import pytest, sys, os.path, shutil
sys.path.append('app')
from load_report_service.dataverse_load_report_service import DataverseLoadReportService
import unit_test_helper

nrs_prefix = os.getenv("NRS_PREFIX")

def test_handle_load_report():
    '''Tests that the obj urn is retrieved properly'''
    unit_test_helper.deposit_sample_load_report()
    load_report_service = DataverseLoadReportService()
    obj_urn = load_report_service.handle_load_report(unit_test_helper.sample_load_report, True)
    assert obj_urn.startswith(os.path.join(nrs_prefix, "URN-3"))
    unit_test_helper.cleanup_sample_load_report()
            
def test_handle_failed_batch():
    '''Tests that the failed batch marker exists'''
    unit_test_helper.create_sample_failed_batch()
    load_report_service = DataverseLoadReportService()
    batch_name = load_report_service.handle_failed_batch("sample", True)
    assert batch_name == "sample"
    unit_test_helper.cleanup_sample_failed_batch()
            
