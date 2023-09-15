from translate_data_structure.translate_data_structure_service import TranslateDataStructureService
from content_model_mapping.audio_content_model_mapping import AudioContentModelMapping
from content_model_mapping.document_content_model_mapping import DocumentContentModelMapping
from content_model_mapping.stillimage_content_model_mapping import StillImageContentModelMapping
from content_model_mapping.text_content_model_mapping import TextContentModelMapping
from content_model_mapping.opaque_content_model_mapping import OpaqueContentModelMapping
from content_model_mapping.content_model_mapping_builder import ContentModelMappingBuilder


class ETDTranslateDataStructureService(TranslateDataStructureService):

    def __init__(self):
        self.cmm_builder = ContentModelMappingBuilder()

    def _handle_content_model_mapping(self, package_path, object_dir, aux_object_dir):
        self.cmm_builder.get_content_model_mapping(package_path,
                                                   object_dir).handle_directory_mapping(package_path, object_dir, aux_object_dir)
