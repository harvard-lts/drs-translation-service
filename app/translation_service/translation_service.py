import os, os.path, logging, shutil
import translate_data_structure_service 

logfile=os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel)

def prepare_and_send_to_drs(package_dir):
    #Set up directories
    translate_data_structure_service.translate_data_structure(package_dir)
    #Run BB
    
    #Add LOADING file to package directory
    
    