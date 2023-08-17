import pytest, sys, os.path, shutil, os
sys.path.append('app')
from load_report_service.dataverse_load_report_service import DataverseLoadReportService
from load_report_service.load_report_service_builder import LoadReportServiceBuilder
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
    
def test_builder_dvn():
    '''Tests that the service is the DVN service'''
    builder = LoadReportServiceBuilder()
    service = builder.get_load_report_service(os.getenv("DVN_DROPBOX_NAME"))
    assert isinstance(service, DataverseLoadReportService)
    
def test_builder_epadd():
    '''Tests that None is returned for ePADD since ePADD doesn't
    use the load report service'''
    builder = LoadReportServiceBuilder()
    service = builder.get_load_report_service(os.getenv("EPADD_DROPBOX_NAME"))
    assert service is None
            
