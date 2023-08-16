from load_report_service.dataverse_load_report_service import DataverseLoadReportService

class LoadReportServiceBuilder():
    
    def get_load_report_service(self, dropbox_name):
        '''Get the load report name based on the dropbox name'''
        dvn_dropbox_name = os.getenv("DVN_DROPBOX_NAME", "dvndev")
        if dropbox_name == dvn_dropbox_name:
            return "Dataverse"
        return None