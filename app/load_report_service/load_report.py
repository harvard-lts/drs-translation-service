#!/usr/bin/env python3

from load_report_service.load_report_exception import LoadReportException


'''
Parses a load report and manipulates some of the contents
'''
class LoadReport:

    class Object:
        object_id = None
        object_deliverable_uri = None
        object_urn = None
        depositor_name = None
        object_owner_supplied_name = None
        billing = None
        owner = None
        object_type = None
        object_roles = None
        file_id = None
        file_urn = None
        file_format = None
        file_size = None
        file_owner_supplied_name = None
        file_original_path = None
    
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
        self.objects = self.__parse_load_report(self.load_report_path)

    def __parse_load_report(self, load_report_path):
            """
            Parses the load report file and returns a list of objects extracted from the file.

            Args:
                load_report_path (str): The path to the load report file.

            Returns:
                list: A list of objects extracted from the load report file.

            Raises:
                LoadReportException: If there is an error opening or parsing the load report file.
            """
            
            try: 
                file = open(load_report_path, "r")
            except FileNotFoundError:
                raise LoadReportException("ERROR OPENING LOAD REPORT", 'Load Report Filepath does not exist: {}'.format(self.load_report_path), None)

            if file is not None:
                
                lines = file.readlines()
                in_file_section = False

                objects = []
                for line in lines:
                    if in_file_section:
                        object = self.Object()
                        fields = line.rstrip('\n').split("\t")
                        if len(fields) == 15 and fields[self.DRS_FILE_OWNER_SUPPLIED_NAME_INDEX] != 'null':
                            try:
                                object.object_id = fields[self.DRS_OBJECT_ID_INDEX]
                                object.object_deliverable_uri = fields[self.DRS_OBJ_DELIVERABLE_URI_INDEX]
                                object.object_urn = fields[self.DRS_OBJECT_URN_INDEX]
                                object.depositor_name = fields[self.DRS_DEPOSITOR_NAME_INDEX]
                                object.object_owner_supplied_name = fields[self.DRS_OBJECT_OWNER_SUPPLIED_NAME_INDEX]
                                object.billing = fields[self.DRS_BILLING_INDEX]
                                object.owner = fields[self.DRS_OWNER_INDEX]
                                object.object_type = fields[self.DRS_OBJECT_TYPE_INDEX]
                                object.object_roles = fields[self.DRS_OBJECT_ROLES_INDEX]
                                object.file_id = fields[self.DRS_FILE_ID_INDEX]
                                object.file_urn = fields[self.DRS_FILE_URN_INDEX]
                                object.file_format = fields[self.DRS_FILE_FORMAT_INDEX]
                                object.file_size = fields[self.DRS_FILE_SIZE_INDEX]
                                object.file_owner_supplied_name = fields[self.DRS_FILE_OWNER_SUPPLIED_NAME_INDEX]
                                object.file_original_path = fields[self.DRS_FILE_ORIGINAL_PATH_INDEX]
                                objects.append(object)
                            except Exception as why:
                                raise LoadReportException("Error in Load Report Parsing", "An unexpected error occurred while parsing the load report "+self.load_report_path + "\n" + str(why))
                    elif line.startswith(self.DRS_FILELIST_SECTION_LINE_PREFIX):
                        in_file_section = True
                file.close()
            else:
                raise LoadReportException("Error in Load Report Parsing", "Could not open load report: " + self.load_report_path) 

            return objects

    def get_objects(self):
        return self.objects
