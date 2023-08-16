from batch_builder_service.batch_builder_service import BatchBuilderService
from translation_service.epadd_mods_mapping_handler import EpaddModsMappingHandler

class EpaddBatchBuilderService(BatchBuilderService):
    
    def _build_additional_objprop_overrides(self, project_path, object_name, supplemental_deposit_metadata):
        '''Builds the ePadd specific objprop overrides'''
        epadd_mods_mapping_handler = EpaddModsMappingHandler()
        embargoBasis = None
        if "embargoBasis" in supplemental_deposit_metadata and supplemental_deposit_metadata["embargoBasis"]:
            embargoBasis = supplemental_deposit_metadata["embargoBasis"]
        emailaddress = None
        if "failureEmail" in supplemental_deposit_metadata and supplemental_deposit_metadata["failureEmail"]:
            emailaddress = supplemental_deposit_metadata["failureEmail"]
        return epadd_mods_mapping_handler.build_object_overrides(project_path, object_name, embargoBasis, emailaddress)
    
    def _build_dirprop_override_command(self, object_name, supplemental_deposit_metadata):
        '''Builds the -dirprop command'''
        
        overrides = self._build_dirprop_override_command_by_dir(object_name, "container", supplemental_deposit_metadata)
        command = ""
        if overrides is not None:
            command += " -dirprop \"{}\"".format(overrides)
                
        return command
        