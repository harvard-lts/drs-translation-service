import os, os.path, logging, shutil
from content_model_mapping.opaque_content_model_mapping import OpqaueContentModelMapping
from content_model_mapping.opaque_container_content_model_mapping import OpqaueContainerContentModelMapping
from translation_service.batch_builder_assistant import BatchBuilderAssistant

logger = logging.getLogger('dts')
base_load_report_dir = os.getenv("BASE_LOADREPORT_PATH")
sample_load_report="/home/appuser/tests/data/sampleloadreport/LOADREPORT_sample.txt"

batch_builder_assistant = BatchBuilderAssistant()

def prepare_and_send_to_drs(package_dir, supplemental_deposit_data, depositing_application, testing = False):
    #Set up directories
    batch_name = os.path.basename(package_dir) + "-batch"
    batch_dir = os.path.join(package_dir, batch_name)
    
    #This if-else is used for content model mapping for now.
    if depositing_application == "Dataverse":
        cmmapping = OpqaueContentModelMapping(os.getenv("EXTRACTED_PACKAGE_DVN", "True"))
    else:
        cmmapping = OpqaueContainerContentModelMapping()
    object_name = os.path.basename(package_dir)
    object_dir = os.path.join(batch_dir, object_name)
    aux_object_dir = os.path.join(package_dir, "_aux", batch_name, object_name)
    os.makedirs(aux_object_dir, exist_ok=True)
    os.makedirs(object_dir, exist_ok=True)
    
    cmmapping.handle_directory_mapping(package_dir, object_dir, aux_object_dir)
    #Run BB
    batch_builder_assistant.process_batch(package_dir, batch_name, supplemental_deposit_data, depositing_application)
    
    #Move Batch to incoming
    batch_dir = __move_batch_to_incoming(package_dir, batch_dir)
    
    if not testing:
    #Remove old project dir
        __cleanup_project_dir(package_dir)
    
    #Update batch_dir permissions
    __update_permissions(batch_dir)
    
    #Add LOADING file to package directory if we are not testing
    if not testing:
        __create_loading_file(batch_dir)
    #If testing, place a mock load report to allow for the flow to continue
    else:
        if ('dropbox_name' not in supplemental_deposit_data):
            raise Exception("When testing, dropbox_name must be supplied in the supplemental deposit data")
        __place_mock_load_report(os.path.basename(batch_dir), supplemental_deposit_data["dropbox_name"])
    
    return batch_dir

def parse_drsconfig_metadata(drs_config_path):
    admin_metadata = {}
    try:
        #This will throw an error if the file is missing which is handled in the try-except
        with open(drs_config_path, 'r', encoding='UTF-8') as file:
            metadata = file.read().splitlines()
            metadata_dict = {}
            for val in metadata:
                if len(val) > 0:
                    split_val = val.split('=')
                    metadata_dict[split_val[0]] = split_val[1]
            
            try:
                #This will throw an error if any key is missing and is handled in the try-except
                admin_metadata = {        
                    "accessFlag": metadata_dict["accessFlag"],
                    "contentModel": metadata_dict["contentModel"],
                    "depositingSystem": metadata_dict["depositingSystem"],
                    "firstGenerationInDrs": metadata_dict["firstGenerationInDrs"],
                    "objectRole": metadata_dict["objectRole"],
                    "usageClass": metadata_dict["usageClass"],
                    "storageClass": metadata_dict["storageClass"],
                    "ownerCode": metadata_dict["ownerCode"],
                    "billingCode": metadata_dict["billingCode"],
                    "resourceNamePattern": metadata_dict["resourceNamePattern"],
                    "urnAuthorityPath": metadata_dict["urnAuthorityPath"],
                    "depositAgent": metadata_dict["depositAgent"],
                    "depositAgentEmail": metadata_dict["depositAgentEmail"],
                    "successEmail": metadata_dict["successEmail"],
                    "failureEmail": metadata_dict["failureEmail"],
                    "successMethod": metadata_dict["successMethod"],
                    "adminCategory": metadata_dict.get("adminCategory"),
                    "embargoBasis": metadata_dict.get("embargoBasis")
                }
            except KeyError as err:
                logger.error("Missing a key in " + drs_config_path +" file: " + str(err))

    except FileNotFoundError:
        logger.error("drsConfig.txt does not exist for path: "+ drs_config_path)
    
    return admin_metadata

def __move_batch_to_incoming(project_dir, batch_dir):
    #dropbox is the path above the project
    dropbox_path = os.path.dirname(project_dir)
    shutil.move(batch_dir, dropbox_path)
    return os.path.join(dropbox_path, os.path.basename(batch_dir))   


def __cleanup_project_dir(project_dir):
    '''Remove project directory'''
    shutil.rmtree(project_dir) 

def __create_loading_file(batch_dir):
    '''Creates a LOADING file for DRS'''
    loading_file = os.path.join(batch_dir, "LOADING")
    open(loading_file, 'a').close()

def __update_permissions(batch_dir):
    '''
    Sets group and r/w permission for DRS as follows:
        Directory - batch_dir
        User - hdc3aadm (55020)
        Group - guestftp (4000)
    '''
    for root, dirs, files in os.walk(batch_dir):
        for dir in dirs:
            os.chown(os.path.join(root, dir), 55020, 4000)
            os.chmod(os.path.join(root, dir), 0o775)
        for file in files:
            os.chown(os.path.join(root, file), 55020, 4000)
            os.chmod(os.path.join(root, file), 0o775)
    os.chown(batch_dir, 55020, 4000)
    os.chmod(batch_dir, 0o775)
    
    
def __place_mock_load_report(batch_name, dropbox_name):
    #Make sure to append incoming if it is a real dropbox
    if dropbox_name != "":
        dropbox_name = os.path.join(dropbox_name, "incoming")
    batch_load_report_dir = os.path.join(base_load_report_dir, dropbox_name, batch_name)
    #Create dir in LR dir
    os.mkdir(batch_load_report_dir)
    
    mock_load_report_name = "LOADREPORT_{}.txt".format(batch_name)
    mock_load_report_dest = os.path.join(batch_load_report_dir, mock_load_report_name)
    shutil.copy(sample_load_report, mock_load_report_dest)
