from translation_service.translation_service import TranslationService
from translate_data_structure.dataverse_translate_data_structure_service import DataverseTranslateDataStructureService
from batch_builder_service.dataverse_batch_builder_service import DataverseBatchBuilderService


class DataverseTranslationService(TranslationService):

    # add an instance of the DataverseTranslateDataStructureService
    # to the class
    def _get_translate_data_structure_service(self):
        return DataverseTranslateDataStructureService()

    # add an instance of the DataverseBatchBuilderService
    # to the class
    def _get_batch_builder_service(self):
        return DataverseBatchBuilderService()

    def get_admin_metadata(self, dropbox_name):
        '''Returns the admin metadata'''
        admin_metadata = {"dropbox_name": dropbox_name}

        return admin_metadata
