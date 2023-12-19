from load_report_service.load_report_service import LoadReportService
from load_report_service.load_report_exception import LoadReportException
from celery import Celery
import os
import logging

app = Celery(os.getenv("ETD_BROKER"))
app.config_from_object('etdtestceleryconfig')

etd_holding_task = os.getenv('ETD_HOLDING_TASK_NAME', 'etd-alma-drs-holding-service.tasks.add_holdings')

logger = logging.getLogger('dts')

class ETDLoadReportService(LoadReportService):
    
    def _get_application_name(self):
        '''Returns the application name'''
        
        return "ETD"
    
    def _process_load_report(self, objects, batch_name, load_report_path, dry_run = False):
        """
        Process the load report.

        Args:
            objects (list): List of objects.
            batch_name (str): Name of the batch.
            load_report_path (str): Path to the load report.

        Raises:
            LoadReportException: If object URN could not be found in the load report.
        """
        pqid = ""
        object_id = ""
        for object in objects:

            obj_osn = object.object_owner_supplied_name
            if (obj_osn is None):
                raise LoadReportException("ERROR Object OSN could not be found in load report, {}.".format(load_report_path))
            if (obj_osn.startswith("ETD_THESIS")):
                pqid = self.get_pqid_from_osn(obj_osn)
                object_id = object.object_id

        # remove trailing "-batch"
        package_id = batch_name[0:-6]
        
        application_name = self._get_application_name()
        
        msg_json = {
            "package_id": package_id,
            "application_name": application_name,
            "drs_object_id": object_id,
            "pqid": pqid,
            "admin_metadata": {
                "original_queue": os.getenv("ETD_HOLDING_QUEUE_NAME"),
                "task_name": etd_holding_task,
                "retry_count": 0
            }
        }
        if not dry_run:
            app.send_task(etd_holding_task, args=[msg_json], kwargs={},
                          queue=os.getenv("ETD_HOLDING_QUEUE_NAME"))
        
    def get_pqid_from_osn(self, obj_osn):
        # Format is ETD_THESIS_<school>_<degreedate>_PQ_<pqid>_<timestamp>
        # Split by "PQ_"
        osn_split = obj_osn.split("PQ_")
        if (len(osn_split) != 2):
            raise LoadReportException("ERROR Object OSN is not in expected format, {}.".format(obj_osn))
        # Split by "_"
        osn_split = osn_split[1].split("_")
        if (len(osn_split) != 2):
            raise LoadReportException("ERROR Object OSN is not in expected format, {}.".format(obj_osn))
        return osn_split[0]
        