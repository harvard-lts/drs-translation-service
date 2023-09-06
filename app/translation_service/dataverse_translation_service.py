from translation_service.translation_service import TranslationService
from translate_data_structure.dataverse_translate_data_structure_service import DataverseTranslateDataStructureService


class DataverseTranslationService(TranslationService):

    # add an instance of the DataverseTranslateDataStructureService
    # to the class
    def _get_translate_data_structure_service(self):
        return DataverseTranslateDataStructureService()

    # add an instance of the DataverseBatchBuilderService
    # to the class
    def _get_batch_builder_service(self):
        return DataverseBatchBuilderService()

    def get_admin_metadata(self, drs_config_path):
        '''Returns the admin metadata'''
        admin_metadata = {}
        try:
            # This will throw an error if the
            # file is missing which is handled in the try-except
            with open(drs_config_path, 'r', encoding='UTF-8') as file:
                metadata = file.read().splitlines()
                metadata_dict = {}
                for val in metadata:
                    if len(val) > 0:
                        split_val = val.split('=')
                        metadata_dict[split_val[0]] = split_val[1]

                try:
                    # This will throw an error if any key is missing
                    # and is handled in the try-except
                    admin_metadata = {
                        "accessFlag": metadata_dict["accessFlag"],
                        "contentModel": metadata_dict["contentModel"],
                        "depositingSystem": metadata_dict["depositingSystem"],
                        "firstGenerationInDrs":
                        metadata_dict["firstGenerationInDrs"],
                        "objectRole": metadata_dict["objectRole"],
                        "usageClass": metadata_dict["usageClass"],
                        "storageClass": metadata_dict["storageClass"],
                        "ownerCode": metadata_dict["ownerCode"],
                        "billingCode": metadata_dict["billingCode"],
                        "resourceNamePattern":
                        metadata_dict["resourceNamePattern"],
                        "urnAuthorityPath": metadata_dict["urnAuthorityPath"],
                        "depositAgent": metadata_dict["depositAgent"],
                        "depositAgentEmail":
                        metadata_dict["depositAgentEmail"],
                        "successEmail": metadata_dict["successEmail"],
                        "failureEmail": metadata_dict["failureEmail"],
                        "successMethod": metadata_dict["successMethod"],
                        "adminCategory": metadata_dict.get("adminCategory"),
                        "embargoBasis": metadata_dict.get("embargoBasis")
                    }
                except KeyError as err:
                    self.logger.error("Missing a key in " + drs_config_path +
                                      " file: " + str(err))

        except FileNotFoundError:
            self.logger.error("drsConfig.txt does not exist for path: " +
                              drs_config_path)

        return admin_metadata
