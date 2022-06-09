import os, os.path, logging
from translation_service.translation_exceptions import BatchBuilderException

'''
The assistant processes the batches using 
the Batch Builder client
'''
class BatchBuilderAssistant:
    
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
    
               
    def process_batch(self, project_path, batch_name, supplemental_deposit_metadata):
        '''Builds the batch.xml and descriptor.xml for the prepared batch'''
        bb_client_path = os.getenv("BB_CLIENT_PATH")

        if os.path.isdir(project_path):
            command = "cd {} && ".format(bb_client_path)
            command += self.build_command(project_path, batch_name, supplemental_deposit_metadata)

            logging.info("batch builder command: " + command)
            os.system(command)
                        
            expected_batch_file = os.path.join(project_path, batch_name, "batch.xml")
            if not os.path.isfile(expected_batch_file):
                logging.error("Failed to create batch, no batch.xml found: " + command)
                raise BatchBuilderException("Failed to create batch, no batch.xml found: " + command)  
                        
            if not self.__validate_descriptors_exist(os.path.join(project_path, batch_name)):
                logging.error("Failed to create batch, no descriptor found: " + command)
                raise BatchBuilderException("Failed to create batch, no descriptor found: " + command)  
                        

    def build_command(self, project_path, batch_name, supplemental_deposit_metadata):
            bb_script_name = os.getenv("BB_SCRIPT_NAME")
            command = "sh " + bb_script_name + " -a build -p " + project_path + " -b " + batch_name
            object_name = os.path.basename(project_path)
            hasoverrides = False
            
            batch_prop_overrides = self.__build_batchprop_override_command(supplemental_deposit_metadata)
            if batch_prop_overrides is not None:
                command += batch_prop_overrides
                hasoverrides=True

            object_prop_overrides = self.__build_objprop_override_command(object_name, supplemental_deposit_metadata)
            if object_prop_overrides is not None:
                command += object_prop_overrides
                hasoverrides=True

            content_file_prop_overrides = self.__build_fileprop_override_command(object_name, "content", supplemental_deposit_metadata)
            if content_file_prop_overrides is not None:
                command += " -dirprop \"{}".format(content_file_prop_overrides)
                hasoverrides=True
                
            doc_file_prop_overrides = self.__build_fileprop_override_command(object_name, "documentation", supplemental_deposit_metadata)
            if doc_file_prop_overrides is not None:
                if content_file_prop_overrides is not None:
                    command += ";{}\"".format(doc_file_prop_overrides)
                else:
                    command += " -dirprop \"{}\"".format(doc_file_prop_overrides)
            elif hasoverrides:
                command += "\""    
            return command
        
    def __validate_descriptors_exist(self, batch_path): 
        for root, dirs, files in os.walk(batch_path):
            if "descriptor.xml" in files:
                return True
        return False 
    
    def __build_batchprop_override_command(self, supplemental_deposit_metadata): 
        '''Syntax -batchprop property=value,property=value,property=value;'''
        overrides = ""   
        delimiter = ""
        if "successEmail" in supplemental_deposit_metadata:
            overrides += "successEmail={}".format(supplemental_deposit_metadata["successEmail"])
        if "failureEmail" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}failureEmail={}".format(delimiter,supplemental_deposit_metadata["failureEmail"])
        if "successMethod" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}successMethod={}".format(delimiter,supplemental_deposit_metadata["successMethod"])
        if "depositAgent" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}depositAgent={}".format(delimiter,supplemental_deposit_metadata["depositAgent"])
        if "depositAgentEmail" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}depositAgentEmail={}".format(delimiter,supplemental_deposit_metadata["depositAgentEmail"])
        command = None
        if overrides:
            command = " -batchprop \"{}\"".format(overrides);
            
        return command                           


    def __build_objprop_override_command(self, object_name, supplemental_deposit_metadata):  
        '''-objectprop object_name::property=value,property=value;'''  
        overrides = ""  
        delimiter = "" 
        if "ownerCode" in supplemental_deposit_metadata:
            overrides += "ownerCode={}".format(supplemental_deposit_metadata["ownerCode"])
        if "billingCode" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}billingCode={}".format(delimiter,supplemental_deposit_metadata["billingCode"])
        if "resourceNamePattern" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}resourceNamePattern={}".format(delimiter,supplemental_deposit_metadata["resourceNamePattern"])
        if "urnAuthorityPath" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}urnAuthorityPath={}".format(delimiter,supplemental_deposit_metadata["urnAuthorityPath"])
        if "accessFlag" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}accessFlag={}".format(delimiter,supplemental_deposit_metadata["accessFlag"])
        if "adminCategory" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}adminCategory={}".format(delimiter,supplemental_deposit_metadata["adminCategory"])
        if "objectRole" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            objectRole = supplemental_deposit_metadata["objectRole"]
            objectRole = objectRole.replace(":", "_")
            overrides += "{}role={};".format(delimiter,objectRole)
        command = None
        if overrides:
            command = " -objectprop \"{}::{}\"".format(object_name, overrides);
            
        return command 

    def __build_fileprop_override_command(self, object_name, directory_name, supplemental_deposit_metadata):  
        '''Syntax object_name::directory_path::property=value,property=value;'''  
        overrides = ""  
        delimiter = ""  
        if "firstGenerationInDrs" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "isFirstGenerationInDrs={}".format(supplemental_deposit_metadata["firstGenerationInDrs"])
        if "usageClass" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}usageClass={}".format(delimiter,supplemental_deposit_metadata["usageClass"])
        if "storageClass" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}fileStorageClass={}".format(delimiter,supplemental_deposit_metadata["storageClass"])
        command = None
        if overrides:
            command = "{}::{}::{}".format(object_name, directory_name, overrides);
            
        return command  