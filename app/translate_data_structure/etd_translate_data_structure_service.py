from translate_data_structure.translate_data_structure_service import TranslateDataStructureService
from content_model_mapping.content_model_mapping_builder import ContentModelMappingBuilder
from translation_service.translation_exceptions import TranslationException
from translate_data_structure.mets_extractor import MetsExtractor
from translate_data_structure.mapping_file_builder import MappingFileBuilder
import glob
import os
import os.path
import zipfile
import logging
import re


AMD_PRIMARY = "amd_primary"
AMD_SUP = "amd_supplemental"
AMD_LIC = "amd_license"
ROLE_THESIS = "THESIS"
ROLE_SUPPLEMENT = "THESIS_SUPPLEMENT"
ROLE_LICENSE = "LICENSE"
ROLE_DOCUMENTATION = "DOCUMENTATION"
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

        self.mets_extractor = self.__create_mets_extractor(filepath, extractedfiles)
        if self.mets_extractor is None:
            raise TranslationException("No mets.xml file was supplied. DRS Deposit will be haulted for {}".format(package_path), None)
    
        supplemental_deposit_data["dash_id"] = self.mets_extractor.get_identifier()
        
        for f in extractedfiles:
            if (os.path.isfile(os.path.join(filepath, f))):
                # Remove punctuation to give a default object name
                # The object name will be overwritten in the mapping.txt file
                # Use only alpha-numeric, period (.), underscore (_), or dash (-) for filenames
                modified_file_name = re.sub(r"[^\w\d\.\-]", "_", f)
                object_name = self.format_etd_osn(supplemental_deposit_data['school_dropbox_name'], f)
                object_dir = os.path.join(batch_dir, object_name)
                aux_object_dir = os.path.join(package_path, "_aux", batch_name, object_name)
                self.__handle_etd_content_model_mapping(os.path.join(filepath, f), 
                                                        modified_file_name, package_path, 
                                                        object_dir, aux_object_dir, supplemental_deposit_data)
                
        
        # Add mapping files
        return batch_dir

    def __handle_etd_content_model_mapping(self, fullfilename, modified_file_name, 
                                           package_path, object_dir, 
                                           aux_object_dir, supplemental_deposit_data):
        '''Handle the content model mapping'''
        #for filename in glob.glob(os.path.join(package_path, '*.*')):
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
    
    def __create_mets_extractor(self, filepath, extractedfiles):
        for f in extractedfiles:
            if f == "mets.xml":
                return MetsExtractor(os.path.join(filepath, f))
        return None

    def format_etd_osn(self, school_dropbox_name, filename, mets_file_path = None):
        '''Formats the OSN to use the format of 
        ETD_[OBJECT_ROLE]_[SCHOOL_CODE]_[DEGREE_DATE_VALUE]_PQ_[PROQUEST_IDENTIFIER_VALUE]'''
        if self.mets_extractor is None:
            if mets_file_path is not None:
                self.mets_extractor = MetsExtractor(mets_file_path)
            else:
                raise TranslationException("No mets.xml file was supplied. DRS Deposit will be haulted for {}-{}".
                                           format(school_dropbox_name, filename), None)
        amdid_mimetype = self.mets_extractor.get_amdid_and_mimetype(filename)
        if amdid_mimetype.amdid is None and filename != "mets.xml":
            raise TranslationException("Missing or incorrect fileSec info in mets.xml for {}".
                                           format(filename), None)

        degree_date = self.mets_extractor.get_degree_date()
        identifier = self.mets_extractor.get_identifier()
        role = self.__determine_role(amdid_mimetype.amdid, filename)
        osn = "ETD_{}_{}_{}_PQ_{}".format(role, school_dropbox_name, degree_date, identifier)
        return osn
    
    def __determine_role(self, amdid, filename):
        # mets.xml is the only one not in the mets.xml fileSec
        # so it will not have the amdid
        if amdid is None:
            if filename == "mets.xml":
                return ROLE_DOCUMENTATION
            else:
                return None

        if amdid.startswith(AMD_PRIMARY):
            return ROLE_THESIS
        elif amdid.startswith(AMD_SUP):
            return ROLE_SUPPLEMENT
        elif amdid.startswith(AMD_LIC):
            return ROLE_LICENSE
        return None
