import os, os.path, logging, shutil
from load_report_service.load_report import LoadReport
from load_report_service.load_report_exception import LoadReportException
import mqresources.mqutils as mqutils

logfile=os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel, format="%(asctime)s:%(levelname)s:%(message)s")

load_report_dir = os.getenv("LOADREPORT_PATH")
dropbox_dir = os.getenv("DROPBOX_PATH")

def handle_load_report(load_report_name, dry_run = False):
    #Strip off the LOADREPORT_ to get the batch name
    if (not load_report_name.startswith("LOADREPORT_")):
        raise LoadReportException("ERROR Expected load report name, {}, to begin with LOADREPORT_".format(load_report_name))
    
    batch_name = load_report_name[11:-4]
    load_report_path = os.path.join(load_report_dir, batch_name, load_report_name)
   
    # Parse the LRs (attempt even if none were brought from the dropbox)
    obj_osn = _parse_load_report(load_report_path)
    # if not dry_run:
    #     #Delete the LR from the dropbox
    #     _delete_load_report_from_dropbox(os.path.join(load_report_dir, batch_name))
    #     #Delete the batch
    #     _delete_batch_from_dropbox(os.path.join(dropbox_dir, batch_name))
        
    if (obj_osn is None):
        raise LoadReportException("ERROR Object OSN could not be found in load report, {}.".format(load_report_path))
    
    nrs_prefix = os.getenv("NRS_PREFIX")    
    urn = os.path.join(nrs_prefix, obj_osn)
    mqutils.notify_ingest_status_process_message(batch_name, "success", urn)
    return urn
    

def handle_failed_batch(batch_name, dry_run = False):
    #Send failed notification
    mqutils.notify_ingest_status_process_message(batch_name, "failed")
    #Delete batch from dropbox
    if not dry_run:
        _delete_batch_from_dropbox(os.path.join(dropbox_dir, batch_name)) 
    return batch_name
    
def _delete_load_report_from_dropbox(load_report_path):
    '''
    Deletes the load report from the dropbox.
    If an error occurs in the deletion, the error is written to the log but no exception is thrown
    since it will try again next time
    '''
    try:
        shutil.rmtree(load_report_path)
    except Exception:
        logging.exception("Error in deleting load report {} from the dropbox.".format(load_report_path))
        raise LoadReportException("ERROR Deleting Load Report from dropbox", "Error in deleting load report {} from the dropbox.".format(load_report_path)) 

def _delete_batch_from_dropbox(batch_path):
    '''
    Deletes the batch from the dropbox.
    If an error occurs in the deletion, the error is written to the log but no exception is thrown
    '''
    try:
        shutil.rmtree(batch_path)
    except Exception:
        logging.exception("Error in deleting batch {} from the dropbox".format(batch_path))
        raise LoadReportException("ERROR Deleting Batch from Dropbox", "Error in deleting batch {} from the dropbox".format(batch_path)) 
      

    
def _parse_load_report(local_load_report_path):
    '''
    Reads and parses the values of the load report and returns the obj_urn. 
    '''
    load_report = LoadReport(local_load_report_path)
    return load_report.get_obj_urn()
                    
    
    