from translate_data_structure.translate_data_structure_service import TranslateDataStructureService
from content_model_mapping.audio_content_model_mapping import AudioContentModelMapping
from content_model_mapping.document_content_model_mapping import DocumentContentModelMapping
from content_model_mapping.stillimage_content_model_mapping import StillImageContentModelMapping
from content_model_mapping.text_content_model_mapping import TextContentModelMapping
from content_model_mapping.etd_opaque_content_model_mapping import ETDOpaqueContentModelMapping
from content_model_mapping.content_model_mapping_builder import ContentModelMappingBuilder
import glob
import os


class ETDTranslateDataStructureService(TranslateDataStructureService):

    def __init__(self):
        self.cmm_builder = ContentModelMappingBuilder()
        self.document_cmm = None
        self.still_image_cmm = None
        self.audio_cmm = None
        self.text_cmm = None
        self.opaque_cmm = None

    def _handle_content_model_mapping(self, package_path, object_dir, aux_object_dir):
        '''Handle the content model mapping'''

        for filename in glob.glob(os.path.join(package_path, '*.*')):
            content_model = self.cmm_builder.get_content_model_mapping(package_path, filename)
            if ((isinstance(content_model, DocumentContentModelMapping)) and (self.document_cmm is None)):
                self.document_cmm = content_model
                self.document_cmm.handle_directory_mapping(package_path, object_dir, aux_object_dir)
            elif ((isinstance(content_model, StillImageContentModelMapping)) and (self.still_image_cmm is None)):
                self.still_image_cmm = content_model
                self.still_image_cmm.handle_directory_mapping(package_path, object_dir, aux_object_dir)
            elif ((isinstance(content_model, AudioContentModelMapping)) and (self.audio_cmm is None)):
                self.audio_cmm = content_model
                self.audio_cmm.handle_directory_mapping(package_path, object_dir, aux_object_dir)
            elif ((isinstance(content_model, TextContentModelMapping)) and (self.text_cmm is None)):
                self.text_cmm = content_model
                self.text_cmm.handle_directory_mapping(package_path, object_dir, aux_object_dir)
            elif ((isinstance(content_model, ETDOpaqueContentModelMapping)) and (self.opaque_cmm is None)):
                self.opaque_cmm = content_model
                self.opaque_cmm.handle_directory_mapping(package_path, object_dir, aux_object_dir)
            else: # all content models have been created
                break


