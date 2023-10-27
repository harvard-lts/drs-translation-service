import os
import shutil
import glob
from content_model_mapping.content_model_mapping import ContentModelMapping

class OpaqueContentModelMapping(ContentModelMapping):
    
    def __init__(self, is_extraced_package):
        self.is_extracted_package = is_extraced_package.lower()
        super().__init__()
        
    def handle_directory_mapping(self, package_path, object_dir, aux_object_dir):
        self.logger.debug("Formatting for opaque content model")
        parent_directory_path = package_path
        if (self.is_extracted_package == "true"):
            # Make batch dir and object dir
            os.makedirs(object_dir, exist_ok=True)
            # /package_path/extracted
            extracted_files_dir = os.path.join(package_path, "extracted")
            # /package_path/extracted/unzippeddir
            extracted_files = os.listdir(extracted_files_dir)
            if (len(extracted_files) != 1):
                raise Exception(
                    "{} directory expected 1 item but found {}".format(extracted_files_dir, len(extracted_files)))
    
            parent_directory_path = os.path.join(extracted_files_dir, extracted_files[0])
    
        hascontent = self.__handle_content_files(object_dir, parent_directory_path)
    
        project_conf = os.getenv("OPAQUE_PROJECT_CONF_TEMPLATE")
        self._copy_project_conf(package_path, project_conf)
        if not hascontent:
            object_xml_template = os.getenv("OBJECT_XML_DOC_ONLY_TEMPLATE")
        else:
            object_xml_template = os.getenv("OPAQUE_OBJECT_XML_TEMPLATE")
        self._copy_object_xml_and_rename_object(aux_object_dir, object_xml_template)
    
        self.__handle_documentation_files(object_dir, parent_directory_path)
        
    def __handle_content_files(self, object_dir, extracted_path):
        '''Moves any content related files to the content directory'''
        content_list_string = os.getenv("CONTENT_FILES_AND_DIRS", "")
        content_list = content_list_string.split(",")
    
        hascontent = False
        for item in content_list:
            item = item.strip()
            item_path = os.path.join(extracted_path, item)
            content_path = os.path.join(object_dir, "content")
    
            # If there is a wildcard, then move all under that item
            if ("*" in item):
                for file in glob.glob(r'{}'.format(item_path)):
                    shutil.copy2(file, os.path.join(content_path, file))
            elif os.path.exists(item_path):
                self.logger.debug("Moving content for {}".format(item_path))
                if not os.path.exists(content_path):
                    os.mkdir(content_path)
                # If it is a path to a file, move the file
                if (os.path.isfile(item_path)):
                    self.logger.debug("Moving {} to {}".format(item_path, os.path.basename(item_path)))
                    shutil.copy2(item_path, os.path.join(content_path, os.path.basename(item_path)))
                # If it is a directory, use the recursive call
                else:
                    self._move_files(item_path, item_path, content_path)
                hascontent = hascontent or True
            else:
                hascontent = hascontent or False
    
        return hascontent
    
    def __handle_documentation_files(self, object_dir, extracted_path):
        documentation_list_string = os.getenv("DOCUMENTATION_FILES_AND_DIRS", "")
        documentation_list = documentation_list_string.split(",")
    
        doc_path = os.path.join(object_dir, "documentation")
        for item in documentation_list:
            item = item.strip()
            item_path = os.path.join(extracted_path, item)
            # If there is a wildcard, then move all under that item
            if ("*" in item):
                for file in glob.glob('{}'.format(item_path)):
                    shutil.copy2(os.path.join(item_path, file), os.path.join(doc_path, file))
            elif os.path.exists(item_path):
                if not os.path.exists(doc_path):
                    os.mkdir(doc_path)
    
                # If it is a path to a file, move the file
                if (os.path.isfile(item_path)):
                    self.logger.debug("Moving {} to {}".format(item_path, os.path.basename(item_path)))
                    shutil.copy2(item_path, os.path.join(doc_path, os.path.basename(item_path)))
                # If it is a directory, use the recursive call
                else:
                    self._move_files(item_path, item_path, doc_path)
    
    def get_file_directory_name(self):
        return "content"