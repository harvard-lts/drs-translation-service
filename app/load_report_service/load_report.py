#!/usr/bin/env python3

import logging
from load_report_service.load_report_exception import LoadReportException

'''
Parses a load report and manipulates some of the contents
'''
class LoadReport:
    
    #Constants
    BATCH_NAME_LINE_PREFIX = "Batch name: ";
    BATCH_DIRECTORY_LINE_PREFIX = "Batch directory name: ";
    DRS_FILELIST_SECTION_LINE_PREFIX = "OBJ-ID"
        
    #The column location of the fields in the report (drs_).
    DRS_OBJECT_ID_INDEX = 0
    DRS_OBJ_DELIVERABLE_URI_INDEX = 1
    DRS_OBJECT_URN_INDEX = 2
    DRS_DEPOSITOR_NAME_INDEX = 3
    DRS_OBJECT_OWNER_SUPPLIED_NAME_INDEX = 4
    DRS_BILLING_INDEX = 5
    DRS_OWNER_INDEX = 6
    DRS_OBJECT_TYPE_INDEX = 7
    DRS_OBJECT_ROLES_INDEX = 8
    DRS_FILE_ID_INDEX = 9
    DRS_FILE_URN_INDEX= 10
    DRS_FILE_FORMAT_INDEX = 11
    DRS_FILE_SIZE_INDEX = 12
    DRS_FILE_OWNER_SUPPLIED_NAME_INDEX = 13
    DRS_FILE_ORIGINAL_PATH_INDEX = 14
    
    """ Initiator function """
    def __init__(self, load_report_path):   
        self.load_report_path = load_report_path
    
    
    #Parse the report and extract the OSN URN
    # and file information.
    # 
    #There are 3 different sections in the loader report:
    # 1. batch summary
    # 2. file list
    # 3. relationship list
    # 
    #This method relies on knowing which of the 3 sections it is in.
    # 
    def get_obj_urn(self):

        file = None
        
        try: 
            file = open(self.load_report_path, "r")
        except FileNotFoundError:
            logging.warning('Load Report Filepath does not exist: {}'.format(self.load_report_path))
            raise LoadReportException("ERROR OPENING LOAD REPORT", 'Load Report Filepath does not exist: {}'.format(self.load_report_path))

        if file is not None:
            
            lines = file.readlines()
            in_file_section = False
            
            for line in lines:
                if in_file_section:
                    fields = line.rstrip('\n').split("\t")
                    if len(fields) == 15 and fields[self.DRS_FILE_OWNER_SUPPLIED_NAME_INDEX] != 'null':
                        #Update the database
                        try:
                            #All files will have the same object urn
                            obj_urn = fields[self.DRS_OBJECT_URN_INDEX]
                            return obj_urn
                        except Exception as why:
                            raise LoadReportException("Error in Load Report Parsing", "An unexpected error occurred while parsing the load report "+self.load_report_path + "\n" + str(why))
                elif line.startswith(self.DRS_FILELIST_SECTION_LINE_PREFIX):
                    in_file_section = True
                
            
            file.close()
        else:
            raise LoadReportException("Error in Load Report Parsing", "Could not open load report: " + self.load_report_path) 

        return None
