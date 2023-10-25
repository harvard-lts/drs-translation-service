import os
import shutil
import glob
from content_model_mapping.content_model_mapping import ContentModelMapping

class DocumentContentModelMapping(ContentModelMapping):
    def handle_directory_mapping(self, package_path, object_dir, aux_object_dir):
        '''Moves the document into the document directory'''
        self.logger.debug("Formatting for document content model")
        document_dir = os.path.join(object_dir, "document")
        if not os.path.exists(document_dir):
            os.mkdir(document_dir)

        suffixes = ["pdf", "doc", "docx", "wp", "wpd", "epub", "rtf"]

        self.logger.debug("globbing...")

        self.logger.debug("globbing...")
        for suffix in suffixes:
            for file in glob.glob(os.path.join(package_path, '*.' + suffix)):
                self.logger.debug("Found package: %s", file)
                filename = os.path.basename(file)
                if f".{suffix}" in filename:
                    shutil.copy2(file, os.path.join(document_dir, filename))

        project_conf = os.getenv("DOCUMENT_PROJECT_CONF_TEMPLATE")        
        object_xml_template = os.getenv("DOCUMENT_OBJECT_XML_TEMPLATE")
        self._handle_project_conf_and_object_xml(package_path, aux_object_dir, project_conf, object_xml_template)

    def handle_single_file_directory_mapping(self, filename_path, target_filename, package_path, object_dir, aux_object_dir):
        content_dir = os.path.join(object_dir, "document")
        if not os.path.exists(content_dir):
            os.mkdir(content_dir)
        shutil.copy2(filename_path, os.path.join(content_dir, os.path.basename(target_filename)))

        project_conf = os.getenv("DOCUMENT_PROJECT_CONF_TEMPLATE")        
        object_xml_template = os.getenv("DOCUMENT_OBJECT_XML_TEMPLATE")
        self._handle_project_conf_and_object_xml(package_path, aux_object_dir, project_conf, object_xml_template)