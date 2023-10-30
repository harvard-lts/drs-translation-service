from translation_service.translation_service import TranslationService
from translate_data_structure.etd_translate_data_structure_service import ETDTranslateDataStructureService
from batch_builder_service.etd_batch_builder_service import ETDBatchBuilderService
from translation_service.translation_exceptions import TranslationException


class ETDTranslationService(TranslationService):

    DROPBOX_NAME = "etd"

    # add an instance of the DataverseTranslateDataStructureService
    # to the class
    def _get_translate_data_structure_service(self):
        return ETDTranslateDataStructureService()

    def get_admin_metadata(self, batch_path, drs_config_path):
        '''Returns the admin metadata'''
        raise TranslationException("Cannot reprocess ETDs.  This will have to be manually built and sent to the DRS: {}".format(batch_path))
    
    # add an instance of the EpaddBatchBuilderService
    # to the class
    def _get_batch_builder_service(self):
        return ETDBatchBuilderService()