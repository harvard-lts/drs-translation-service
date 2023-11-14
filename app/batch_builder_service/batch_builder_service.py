from abc import ABC, abstractmethod
import logging
import os
import os.path
from translation_service.translation_exceptions import BatchBuilderException

class BatchBuilderService(ABC):
    '''
    The service processes the batches using 
    the Batch Builder client
    '''
    
    def __init__(self):
        self.logger = logging.getLogger('dts')
    
    @abstractmethod
    def _build_dirprop_override_command(self, object_name, supplemental_deposit_metadata):
        '''Subclasses build the -dirprop command'''
        pass
        
    def process_batch(self, project_path, batch_name, supplemental_deposit_metadata):
        '''Builds the batch.xml and descriptor.xml for the prepared batch'''
        bb_client_path = os.getenv("BB_CLIENT_PATH")

        if os.path.isdir(project_path):
            command = "cd {} && ".format(bb_client_path)
            command += self.build_command(project_path, batch_name, supplemental_deposit_metadata)

            self.logger.info("batch builder command: " + command)
            os.system(command)
                        
            expected_batch_file = os.path.join(project_path, batch_name, "batch.xml")
            if not os.path.isfile(expected_batch_file):
                emailaddress = None
                if "failureEmail" in supplemental_deposit_metadata and supplemental_deposit_metadata["failureEmail"]:
                    emailaddress = supplemental_deposit_metadata["failureEmail"]
                raise BatchBuilderException("Failed to create batch, no batch.xml found: " + command, emailaddress)
                        
            if not self.__validate_descriptors_exist(os.path.join(project_path, batch_name)):
                emailaddress = None
                if "failureEmail" in supplemental_deposit_metadata and supplemental_deposit_metadata["failureEmail"]:
                    emailaddress = supplemental_deposit_metadata["failureEmail"]
                raise BatchBuilderException("Failed to create batch, no descriptor found: " + command, emailaddress) 
        return command
            
    def build_command(self, project_path, batch_name, supplemental_deposit_metadata):
        bb_script_name = os.getenv("BB_SCRIPT_NAME")
        command = "sh " + bb_script_name + " -a build -p " + project_path + " -b " + batch_name
        object_name = os.path.basename(project_path)
            
        batch_prop_overrides = self._build_batchprop_override_command(supplemental_deposit_metadata)
        if batch_prop_overrides is not None:
            command += batch_prop_overrides
            
        object_prop_overrides = self.__build_objprop_override_command(project_path, object_name, supplemental_deposit_metadata)
        if object_prop_overrides is not None:
            command += object_prop_overrides
            
        dir_prop_overrids = self._build_dirprop_override_command(object_name, supplemental_deposit_metadata)   
        if dir_prop_overrids:
            command += dir_prop_overrids
        return command
    
    def _build_additional_file_prop_command(self, object_name, supplemental_deposit_metadata):
        '''Override in the subclass if there are additional overrides'''
        return None
            
    def __validate_descriptors_exist(self, batch_path): 
        for root, dirs, files in os.walk(batch_path):
            if "descriptor.xml" in files:
                return True
        return False 
    
    def _build_batchprop_override_command(self, supplemental_deposit_metadata): 
        '''Syntax -batchprop property=value,property=value,property=value;'''
        overrides = ""   
        delimiter = ""
        if "successEmail" in supplemental_deposit_metadata:
            overrides += "successEmail={}".format(supplemental_deposit_metadata["successEmail"].rstrip())
        if "failureEmail" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}failureEmail={}".format(delimiter,supplemental_deposit_metadata["failureEmail"].rstrip())
        if "successMethod" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}successMethod={}".format(delimiter,supplemental_deposit_metadata["successMethod"].rstrip())
        if "depositAgent" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}depositAgent={}".format(delimiter,supplemental_deposit_metadata["depositAgent"].rstrip())
        if "depositAgentEmail" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}depositAgentEmail={}".format(delimiter,supplemental_deposit_metadata["depositAgentEmail"].rstrip())
        command = None
        if overrides:
            command = " -batchprop \"{}\"".format(overrides);
            
        return command                           


    def __build_objprop_override_command(self, project_path, object_name, supplemental_deposit_metadata):  
        '''-objectprop object_name::property=value,property=value;'''  
        overrides = ""  
        delimiter = "" 
        if "ownerCode" in supplemental_deposit_metadata:
            overrides += "ownerCode={}".format(supplemental_deposit_metadata["ownerCode"].rstrip())
        if "billingCode" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}billingCode={}".format(delimiter,supplemental_deposit_metadata["billingCode"].rstrip())
        if "resourceNamePattern" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}resourceNamePattern={}".format(delimiter,supplemental_deposit_metadata["resourceNamePattern"].rstrip())
        if "urnAuthorityPath" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}urnAuthorityPath={}".format(delimiter,supplemental_deposit_metadata["urnAuthorityPath"].rstrip())
        if "accessFlag" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}accessFlag={}".format(delimiter,supplemental_deposit_metadata["accessFlag"].rstrip())
        if "adminCategory" in supplemental_deposit_metadata and supplemental_deposit_metadata["adminCategory"].rstrip():
            if overrides:
                delimiter = ","
            overrides += "{}adminCategory={}".format(delimiter,supplemental_deposit_metadata["adminCategory"].rstrip())
        if "objectRole" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            objectRole = supplemental_deposit_metadata["objectRole"].rstrip()
            objectRole = objectRole.replace(":", "_")
            overrides += "{}role={}".format(delimiter,objectRole)
        
        additional_overrides = self._build_additional_objprop_overrides(project_path, object_name, supplemental_deposit_metadata) 
        if additional_overrides:
            overrides += delimiter + additional_overrides 
    
        command = None
        if overrides:
            command = " -objectprop \"{}::{};\"".format(object_name, overrides);
            
        return command 
    
    def _build_additional_objprop_overrides(self, project_path, object_name, supplemental_deposit_metadata):
        '''Implemented by subclasses if they have more objprop overrides'''
        return None
    
    def _build_dirprop_override_command_by_dir(self, object_name, directory_name, supplemental_deposit_metadata):  
        '''Syntax object_name::directory_path::property=value,property=value;
        NOTE: This is called by _build_dirprop_override_command which appends
        the -dirprop command'''
        
        overrides = ""  
        delimiter = ""  
        if "firstGenerationInDrs" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "isFirstGenerationInDrs={}".format(supplemental_deposit_metadata["firstGenerationInDrs"].rstrip())
        if "usageClass" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}usageClass={}".format(delimiter,supplemental_deposit_metadata["usageClass"].rstrip())
        if "storageClass" in supplemental_deposit_metadata:
            if overrides:
                delimiter = ","
            overrides += "{}fileStorageClass={}".format(delimiter,supplemental_deposit_metadata["storageClass"].rstrip())
        command = None
        if overrides:
            command = "{}::{}::{}".format(object_name, directory_name, overrides)
        
        return command