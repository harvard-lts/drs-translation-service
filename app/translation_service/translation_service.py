import os, os.path, logging, shutil
import translation_service.translate_data_structure_service as translate_data_structure_service
from translation_service.batch_builder_assistant import BatchBuilderAssistant

logfile=os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel)

batch_builder_assistant = BatchBuilderAssistant()

def prepare_and_send_to_drs(package_dir, supplemental_deposit_data):
    #Set up directories
    batch_dir = translate_data_structure_service.translate_data_structure(package_dir)
    #Run BB
    batch_builder_assistant.process_batch(package_dir, os.path.basename(batch_dir), supplemental_deposit_data)
    
    #Move Batch to incoming
    batch_dir = __move_batch_to_incoming(batch_dir)
    
    #Remove old project dir
    __cleanup_project_dir(package_dir)
    
    #Add LOADING file to package directory
    __create_loading_file(batch_dir)

    #Update batch_dir permissions
    __update_permissions(batch_dir)
    
    return batch_dir

def __move_batch_to_incoming(batch_dir):
    dropbox_path = os.getenv("DROPBOX_PATH")
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
