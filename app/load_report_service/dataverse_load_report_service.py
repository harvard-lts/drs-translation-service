from load_report_service.load_report_service import LoadReportService

class DataverseLoadReportService(LoadReportService):
    
    def _get_application_name(self):
        '''Returns the application name'''
        
        return "Dataverse"
        