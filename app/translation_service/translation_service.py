import os, os.path, logging
import translate_data_structure_service 
from batch_builder_assistant import BatchBuilderAssistant

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
    __move_batch_to_incoming(batch_dir)
    
    #Remove old project dir
    __cleanup_project_dir(package_dir)
    
    #Add LOADING file to package directory
    __create_loading_file(batch_dir)

def __move_batch_to_incoming(batch_dir):
    dropbox_path = os.getenv("DROPBOX_PATH")
    shutil.move(batch_dir, dropbox_path)
    pass   


def __cleanup_project_dir(project_dir):
    '''Remove project directory'''
    pass 

def __create_loading_file(batch_dir):
    '''Creates a sample failed batch'''
    loading_file = os.path.join(batch_dir, "LOADING")
    open(loading_file, 'a').close()