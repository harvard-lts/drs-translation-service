import os, os.path, logging
from mqresources import mqutils

logfile=os.getenv('LOGFILE_PATH', 'hdc3a_transfer_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel)

def translation_data_structure():
    return True


    
        
        
