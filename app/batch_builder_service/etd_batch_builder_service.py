from batch_builder_service.batch_builder_service import BatchBuilderService

class ETDBatchBuilderService(BatchBuilderService):
    
    def _build_dirprop_override_command(self, object_name, supplemental_deposit_metadata):
        '''Builds the -dirprop command'''
        
        command = ""
        if "contentModel" in supplemental_deposit_metadata:
            file_prop_overrides = self._build_dirprop_override_command_by_dir(object_name, supplemental_deposit_metadata["contentModel"], supplemental_deposit_metadata)
            if file_prop_overrides is not None:
                command = " -dirprop \"{}\"".format(file_prop_overrides)
        return command