from load_report_service.dataverse_load_report_service import DataverseLoadReportService
from load_report_service.etd_load_report_service import ETDLoadReportService
import os
import logging

class LoadReportServiceBuilder():
    
    def __init__(self):
        self.logger = logging.getLogger("dts")
    
    def get_load_report_service(self, dropbox_name):
        '''Get the load report name based on the dropbox name'''
        self.logger.debug("Getting load report service for {}".format(dropbox_name))
        dvn_dropbox_name = os.getenv("DVN_DROPBOX_NAME", "dvndev")
        etd_dropbox_name = os.getenv("ETD_DROPBOX_NAME", "etd")
        if dropbox_name == dvn_dropbox_name:
            return DataverseLoadReportService()
        elif dropbox_name == etd_dropbox_name:
            return ETDLoadReportService()
        return None