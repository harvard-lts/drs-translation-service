from translate_data_structure.translate_data_structure_service import TranslateDataStructureService
from content_model_mapping.opaque_container_content_model_mapping import OpaqueContainerContentModelMapping

class EpaddTranslateDataStructureService(TranslateDataStructureService):
    
    def __init__(self):
        self.opaque_container_cmm = OpaqueContainerContentModelMapping()
        
    def _handle_content_model_mapping(self, package_path, object_dir, aux_object_dir):
        self.opaque_container_cmm.handle_directory_mapping(package_path, object_dir, aux_object_dir)
    