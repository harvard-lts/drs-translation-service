import pytest, sys, os.path, shutil, os
sys.path.append('app')
from load_report_service.dataverse_load_report_service import DataverseLoadReportService
from load_report_service.etd_load_report_service import ETDLoadReportService
from load_report_service.load_report_service_builder import LoadReportServiceBuilder
import unit_test_helper

nrs_prefix = os.getenv("NRS_PREFIX")

def test_handle_dvn_load_report():
    '''Tests that the obj urn is retrieved properly'''
    unit_test_helper.deposit_sample_dvn_load_report()
    load_report_service = DataverseLoadReportService()
    objects = load_report_service.handle_load_report(unit_test_helper.sample_load_report, True)
    assert len(objects) == 1
    assert objects[0].object_urn.startswith("URN-3")
    unit_test_helper.cleanup_sample_load_report()

def test_handle_etd_load_report():
    '''Tests that the obj urn is retrieved properly'''
    unit_test_helper.deposit_sample_etd_load_report()
    load_report_service = ETDLoadReportService()
    objects = load_report_service.handle_load_report(unit_test_helper.etd_sample_load_report, True)
    assert len(objects) == 3
    assert objects[0].object_urn.startswith("URN-3")
    unit_test_helper.cleanup_sample_etd_load_report()
            
def test_handle_dvn_failed_batch():
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

def test_builder_etd():
    '''Tests that None is returned for ePADD since ePADD doesn't
    use the load report service'''
    builder = LoadReportServiceBuilder()
    service = builder.get_load_report_service(os.getenv("ETD_DROPBOX_NAME"))
    assert isinstance(service, ETDLoadReportService)
            
