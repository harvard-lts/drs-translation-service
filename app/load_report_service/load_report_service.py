import os, os.path, logging, shutil

logfile=os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel)

def handle_load_report(package_name):
    #TODO
    pass
    
    