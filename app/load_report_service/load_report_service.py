import os, os.path, shutil
from load_report_service.load_report import LoadReport
from load_report_service.load_report_exception import LoadReportException
from celery import Celery
from kombu import Queue

base_load_report_dir = os.getenv("BASE_LOADREPORT_PATH")
base_dropbox_dir = os.getenv("BASE_DROPBOX_PATH")

app = Celery()
app.config_from_object('celeryconfig')

process_status_task = os.getenv('PROCESS_STATUS_TASK_NAME', 'dims.tasks.handle_process_status')

def handle_load_report(load_report_name, dry_run = False):
    #Strip off the LOADREPORT_ to get the batch name
    if (not load_report_name.startswith("LOADREPORT_")):
        raise LoadReportException("ERROR Expected load report name, {}, to begin with LOADREPORT_".format(load_report_name))
    
    batch_name = load_report_name[11:-4]
    
    load_report_path = None
    dropbox_name = None
    
    dropbox_names = os.getenv("DROPBOX_NAMES", "")
    if dropbox_names != "":
        dropbox_names_list = dropbox_names.split(",")
        #Loop through the dropboxes to determine where the load report lives
        for dropbox_name in dropbox_names_list:
            dropbox_name = dropbox_name.strip()
            batch_path = os.path.join(base_load_report_dir, dropbox_name, "incoming", batch_name)
            if (os.path.exists(batch_path)):
                load_report_path = os.path.join(batch_path, load_report_name)
                break
    else:
        load_report_path = os.path.join(base_load_report_dir, batch_name, load_report_name)
        dropbox_name = ""
        
    if load_report_path is None:
        raise LoadReportException("Could not fine load report {} in any of these dropboxes {}.".format(load_report_name, dropbox_names))
        
    # Parse the LRs (attempt even if none were brought from the dropbox)
    obj_osn = _parse_load_report(load_report_path)
    # TODO: Fix delete
    # Not deleting for now, the loadreport is written with appadmin permissions
    # and will have to be updated on the DRS side
    if not dry_run:
    #     #Delete the LR from the dropbox
    #     _delete_load_report_from_dropbox(os.path.dirname(load_report_path))
    #     #Delete the batch
        if dropbox_name != "":
            dropbox_name = os.path.join(dropbox_name, "incoming")
            _delete_batch_from_dropbox(os.path.join(base_dropbox_dir, dropbox_name, batch_name))
        
    if (obj_osn is None):
        raise LoadReportException("ERROR Object OSN could not be found in load report, {}.".format(load_report_path))
    
    nrs_prefix = os.getenv("NRS_PREFIX")    
    urn = os.path.join(nrs_prefix, obj_osn)
    # remove trailing "-batch"
    package_id = batch_name[0:-6]
    
    if "doi" in package_id:
        application_name = "Dataverse"
    else:
        application_name = "ePADD"

    msg_json = {
        "package_id": package_id,
        "application_name": application_name,
        "batch_ingest_status": "success",
        "drs_url": urn,
        "admin_metadata": {
            "original_queue": os.getenv("PROCESS_PUBLISH_QUEUE_NAME"),
            "task_name": process_status_task,
            "retry_count": 0
        }
    }
    publish_queue = Queue(
        os.getenv("PROCESS_PUBLISH_QUEUE_NAME"), no_declare=True)
    app.send_task(process_status_task, args=[msg_json], kwargs={},
                  queue=publish_queue)
    return urn
    

def handle_failed_batch(batch_name, dry_run = False):
    #Send failed notification
    # remove trailing "-batch"
    package_id = batch_name[0:-6]
    if "doi" in package_id:
        application_name = "Dataverse"
    else:
        application_name = "ePADD"

    msg_json = {
        "package_id": package_id,
        "application_name": application_name,
        "batch_ingest_status": "failed",
        "admin_metadata": {
            "original_queue": os.getenv("PROCESS_PUBLISH_QUEUE_NAME"),
            "task_name": process_status_task,
            "retry_count": 0
        }
    }
    publish_queue = Queue(
        os.getenv("PROCESS_PUBLISH_QUEUE_NAME"), no_declare=True)
    app.send_task(process_status_task, args=[msg_json], kwargs={},
                  queue=publish_queue)

    #Delete batch from dropbox
    # TODO: Fix delete
    # Not deleting for now, the loadreport is written with appadmin permissions
    # and will have to be updated on the DRS side
    # if not dry_run:
#         dropbox_path = None
#         dropbox_names = os.getenv("DROPBOX_NAMES", "")
#         if dropbox_names != "":
#             dropbox_names_list = dropbox_names.split(",")
#             #Loop through the dropboxes to determine where the batch
#             for dropbox_name in dropbox_names_list:
#                 dropbox_name = dropbox_name.strip()
#                 dropbox_path = os.path.join(base_dropbox_dir, dropbox_name, "incoming", batch_name)
#                 if (os.path.exists(dropbox_path)):
#                     break
#         else:
#             dropbox_path = os.path.join(base_dropbox_dir, batch_name)
    #     _delete_batch_from_dropbox(dropbox_path)
    return batch_name
    
def _delete_load_report_from_dropbox(load_report_batch_path):
    '''
    Deletes the load report from the dropbox.
    If an error occurs in the deletion, the error is written to the log but no exception is thrown
    since it will try again next time
    '''
    try:
        shutil.rmtree(load_report_batch_path)
    except Exception:
        raise LoadReportException("ERROR Deleting Load Report from dropbox", "Error in deleting load report {} from the dropbox.".format(load_report_batch_path)) 

def _delete_batch_from_dropbox(batch_path):
    '''
    Deletes the batch from the dropbox.
    If an error occurs in the deletion, the error is written to the log but no exception is thrown
    '''
    try:
        shutil.rmtree(batch_path)
    except Exception:
        raise LoadReportException("ERROR Deleting Batch from Dropbox", "Error in deleting batch {} from the dropbox".format(batch_path)) 
      

    
def _parse_load_report(local_load_report_path):
    '''
    Reads and parses the values of the load report and returns the obj_urn. 
    '''
    load_report = LoadReport(local_load_report_path)
    return load_report.get_obj_urn()
                    
    
    