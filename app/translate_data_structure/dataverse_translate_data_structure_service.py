from translate_data_structure.translate_data_structure_service import TranslateDataStructureService
from content_model_mapping.opaque_content_model_mapping import OpaqueContentModelMapping
import os

class DataverseTranslateDataStructureService(TranslateDataStructureService):
    
    def __init__(self):
        self.opaque_cmm = OpaqueContentModelMapping(os.getenv("EXTRACTED_PACKAGE_DVN", True))
        
    def _handle_content_model_mapping(self, package_path, object_dir, aux_object_dir):
        self.opaque_cmm.handle_directory_mapping(package_path, object_dir, aux_object_dir)
    