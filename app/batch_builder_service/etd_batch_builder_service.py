from batch_builder_service.batch_builder_service import BatchBuilderService

class ETDBatchBuilderService(BatchBuilderService):
    
    def _build_dirprop_override_command(self, object_name, supplemental_deposit_metadata):
        '''Builds the -dirprop command'''
        
        return False