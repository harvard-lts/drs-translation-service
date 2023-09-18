from translation_service.translation_service import TranslationService
from translate_data_structure.etd_translate_data_structure_service import ETDTranslateDataStructureService


class ETDTranslationService(TranslationService):

    DROPBOX_NAME = "etd"

    # add an instance of the DataverseTranslateDataStructureService
    # to the class
    def _get_translate_data_structure_service(self):
        return ETDTranslateDataStructureService()

    # add an instance of the ETDBatchBuilderService
    # to the class
    # def _get_batch_builder_service(self):
    #   return ETDDBatchBuilderService()

    def get_admin_metadata(self, drs_config_path):
        '''Returns the admin metadata'''
        admin_metadata = {"dropbox_name": self.DROPBOX_NAME}

        return admin_metadata