import logging
from translation_service.dataverse_translation_service import DataverseTranslationService
from translation_service.epadd_translation_service import EpaddTranslationService


class TranslationServiceBuilder():

    EPADD_APPLICATION_NAME = "ePADD"
    DVN_APPLICATION_NAME = "Dataverse"

    def __init__(self):
        self.logger = logging.getLogger("dts")

    def get_translation_service(self, depositing_application):
        '''Get the load report name based on the depositing application'''
        self.logger.debug("Getting translation service for {}".format(depositing_application))

        if depositing_application == self.EPADD_APPLICATION_NAME:
            return DataverseTranslationService()
        elif depositing_application == self.DVN_APPLICATION_NAME:
            return EpaddTranslationService()
        return None
    
    def get_translation_service_from_dropbox(self, dropbox_name):
        '''Get the load report name based on the depositing application'''
        self.logger.debug("Getting translation service for {}".format(depositing_application))

        if "epadd" in dropbox_name:
            return DataverseTranslationService()
        elif "dvn" in dropbox_name:
            return EpaddTranslationService()
        return None