from translate_data_structure.translate_data_structure_service import TranslateDataStructureService
from content_model_mapping.content_model_mapping_builder import ContentModelMappingBuilder
from translation_service.translation_exceptions import TranslationException
from translate_data_structure.mapping_file_builder import MappingFileBuilder
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
        self.mets_extractor = None
    
    def translate_data_structure(self, package_path, supplemental_deposit_data=None):
        batch_name = os.path.basename(package_path) + "-batch"
        batch_dir = os.path.join(package_path, batch_name)
            
        filepath = package_path
        files = os.listdir(package_path)
        extractedfiles = []
        if len(files) == 1:
            # If it is a zip file, extract it
            if os.path.isfile(os.path.join(package_path, files[0])) and files[0].endswith(".zip"):
                extractedfiles = self.__unzip_submission_file(os.path.join(package_path, files[0]))
                filepath = os.path.join(package_path, "extracted")
            elif os.path.isfile(os.path.join(package_path, files[0])):
                extractedfiles = files
        elif len(files) > 1:
            extractedfiles = files

        if "file_info" not in supplemental_deposit_data:
            raise TranslationException("file_info was not provided in the supplemental_deposit_data for {}. Data: {}".
                                       format(package_path, supplemental_deposit_data), None)
    
        thesis = None
        for f in extractedfiles:
            if (os.path.isfile(os.path.join(filepath, f))):
                file_info_dict = supplemental_deposit_data['file_info']
                if f not in file_info_dict:
                    raise TranslationException("File infor for {} was not provided in the supplemental_deposit_data. Data: {}".
                                       format(f, supplemental_deposit_data), None)
                file_info = file_info_dict[f]
                object_osn = file_info['object_osn']
                modified_file_name = file_info['modified_file_name']
                if file_info['object_role'] == "THESIS":
                    thesis = ThesisData(object_osn, modified_file_name, f)
                else:
                    object_dir = os.path.join(batch_dir, object_osn)
                    aux_object_dir = os.path.join(package_path, "_aux", batch_name, object_osn)
                    self.__handle_etd_content_model_mapping(os.path.join(filepath, f), 
                                                            modified_file_name, package_path, 
                                                            object_dir, aux_object_dir, supplemental_deposit_data)
                
        # Do the thesis last so the correct project conf gets copied
        # and the object mapping file is placed for the thesis
        if thesis is None:
            raise TranslationException("No thesis supplied for {}".format(package_path), None)
        object_dir = os.path.join(batch_dir, thesis.object_name)
        aux_object_dir = os.path.join(package_path, "_aux", batch_name, thesis.object_name)
        self.__handle_etd_content_model_mapping(os.path.join(filepath, thesis.original_file_name), 
                                                            thesis.file_name, package_path, 
                                                            object_dir, aux_object_dir, supplemental_deposit_data)

        return batch_dir

    def __handle_etd_content_model_mapping(self, fullfilename, modified_file_name, 
                                           package_path, object_dir, 
                                           aux_object_dir, supplemental_deposit_data):
        '''Handle the content model mapping'''
        content_model = self.cmm_builder.get_content_model_mapping(os.path.dirname(fullfilename), os.path.basename(fullfilename))
        os.makedirs(aux_object_dir, exist_ok=True)
        os.makedirs(object_dir, exist_ok=True)
        content_model.handle_single_file_directory_mapping(fullfilename, modified_file_name, package_path, object_dir, aux_object_dir)
        # Add the mapping files
        mapping_file_builder = MappingFileBuilder()
        relative_dir = os.path.join(content_model.get_file_directory_name(), modified_file_name)
        mapping_file_builder.build_mapping_file(os.path.basename(object_dir), relative_dir, supplemental_deposit_data, aux_object_dir)
        object_mapping_dest = os.path.join(package_path, "_aux", "template")
        os.makedirs(object_mapping_dest, exist_ok=True)
        mapping_file_builder.build_object_mapping_file(os.path.basename(object_dir), 
                                                       supplemental_deposit_data, object_mapping_dest)

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

class ThesisData:
    def __init__(self, object_name, file_name, original_file_name):
        self.object_name = object_name
        self.file_name = file_name
        self.original_file_name = original_file_name