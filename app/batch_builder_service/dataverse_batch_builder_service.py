from batch_builder_service.batch_builder_service import BatchBuilderService

class DataverseBatchBuilderService(BatchBuilderService):
    
    def _build_dirprop_override_command(self, object_name, supplemental_deposit_metadata):
        '''Builds the -dirprop command'''
        
        content_file_prop_overrides = self._build_dirprop_override_command_by_dir(object_name, "content", supplemental_deposit_metadata)
        doc_file_prop_overrides = self._build_dirprop_override_command_by_dir(object_name, "documentation", supplemental_deposit_metadata)
        command = ""
        hasoverrides = False
        if content_file_prop_overrides is not None:
            command += " -dirprop \"{}".format(content_file_prop_overrides)
            hasoverrides=True
                
        if doc_file_prop_overrides is not None:
            if content_file_prop_overrides is not None:
                    command += ";{}\"".format(doc_file_prop_overrides)
            else:
                command += " -dirprop \"{}\"".format(doc_file_prop_overrides)
        elif hasoverrides:
                command += "\""    
        return command