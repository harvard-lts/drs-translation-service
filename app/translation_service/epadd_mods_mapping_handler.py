import os, os.path, logging
from translation_service.translation_exceptions import EpaddModsHandlingException

'''
Parses and assigns values using the associated mapping file
'''
class EpaddModsMappingHandler:
        
    def __init__(self):
        
        log_file = os.getenv("LOGFILE_PATH")
        loglevel=os.getenv('LOGLEVEL', 'WARNING')
        
        # Configure logging module
        logging.basicConfig(
          filename=log_file,
          level=loglevel,
          format="%(asctime)s:%(levelname)s:%(message)s",
          filemode='a'
        )
        
    def parse_mapping_file(self):
        pass