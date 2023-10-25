from translate_data_structure.translate_data_structure_service import TranslateDataStructureService
from content_model_mapping.content_model_mapping_builder import ContentModelMappingBuilder
from translation_service.translation_exceptions import TranslationException
import glob
import os
import os.path
import zipfile
import logging
import re


logger = logging.getLogger('dts')
class ETDTranslateDataStructureService(TranslateDataStructureService):

    def __init__(self):
        self.cmm_builder = ContentModelMappingBuilder()

    def translate_data_structure(self, package_path):
        batch_name = os.path.basename(package_path) + "-batch"
        batch_dir = os.path.join(package_path, batch_name)
            
        filepath = package_path
        files = os.listdir(package_path)
        extractedfiles = []
        if len(files) == 1:
            # If it is a zip file, extract it
            if os.path.isfile(os.path.join(package_path, files[0])) and files[0].endswith(".zip"):
                extractedfiles = self.__unzip_submission_file(os.path.join(package_path, f))
                filepath = os.path.join(package_path, "extracted")
            elif os.path.isfile(os.path.join(package_path, files[0])):
                extractedfiles = files
        elif len(files) > 1:
            extractedfiles = files

        for f in extractedfiles:
            if (os.path.isfile(os.path.join(filepath, f))):
                # Remove punctuation to give a default object name
                # The object name will be overwritten in the mapping.txt file
                object_name = re.sub(r"[()]\s", "_", f)
                object_dir = os.path.join(batch_dir, object_name)
                aux_object_dir = os.path.join(package_path, "_aux", batch_name, object_name)
                self.__handle_etd_content_model_mapping(os.path.join(filepath, f), package_path, object_dir, aux_object_dir)
            
        return batch_dir

    def __handle_etd_content_model_mapping(self, fullfilename, package_path, object_dir, aux_object_dir):
        '''Handle the content model mapping'''

        #for filename in glob.glob(os.path.join(package_path, '*.*')):
        content_model = self.cmm_builder.get_content_model_mapping(os.path.dirname(fullfilename), os.path.basename(fullfilename))
        os.makedirs(aux_object_dir, exist_ok=True)
        os.makedirs(object_dir, exist_ok=True)
        content_model.handle_single_file_directory_mapping(fullfilename, package_path, object_dir, aux_object_dir)

    def __unzip_submission_file(self, submission_file_path):

        zipextractionpath = os.path.join(os.path.dirname(submission_file_path), "extracted")
        #Unzip the zipfile
        with zipfile.ZipFile(submission_file_path, 'r') as zip_ref:
            zip_ref.extractall(zipextractionpath) 
    
        extracteditems = os.listdir(zipextractionpath)
        if (len(extracteditems) < 2):
            raise TranslationException("{} directory expected more than 1 item but found {}".format(
                zipextractionpath, len(extracteditems)), None)    
        
        # Remove the submission file
        return extracteditems