from translate_data_structure.translate_data_structure_service import TranslateDataStructureService
from content_model_mapping.content_model_mapping_builder import ContentModelMappingBuilder
import glob
import os


class ETDTranslateDataStructureService(TranslateDataStructureService):

    def __init__(self):
        self.cmm_builder = ContentModelMappingBuilder()

    def _handle_content_model_mapping(self, package_path, object_dir, aux_object_dir):
        '''Handle the content model mapping'''

        for filename in glob.glob(os.path.join(package_path, '*.*')):
            content_model = self.cmm_builder.get_content_model_mapping(package_path, filename)
            content_model.handle_directory_mapping(package_path, object_dir, aux_object_dir)
