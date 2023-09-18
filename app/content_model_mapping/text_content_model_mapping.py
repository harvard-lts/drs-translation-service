import os
import shutil
import glob
from content_model_mapping.content_model_mapping import ContentModelMapping

class TextContentModelMapping(ContentModelMapping):
    def handle_directory_mapping(self, package_path, object_dir, aux_object_dir):
        '''Moves the text into the text directory'''
        self.logger.debug("Formatting for text content model")
        text_dir = os.path.join(object_dir, "text")
        if not os.path.exists(text_dir):
            os.mkdir(text_dir)


        suffixes = ["txt", "xml", "csv", "java", "pl", "py", "rb", "sh", "c", "cpp", "h", "hpp", "js", "css", "html", "htm", "php", "json", "md", "r", "sql", "tsv", "yml"]

        self.logger.debug("globbing...")

        self.logger.debug("globbing...")
        for suffix in suffixes:
            for file in glob.glob(os.path.join(package_path, '*.' + suffix)):
                self.logger.debug("Found package: %s", file)
                filename = os.path.basename(file)
                if f".{suffix}" in filename:
                    shutil.copy2(file, os.path.join(text_dir, filename))

        project_conf = os.getenv("TEXT_PROJECT_CONF_TEMPLATE")        
        self._copy_project_conf(package_path, project_conf)
        object_xml_template = os.getenv("TEXT_OBJECT_XML_TEMPLATE")
        self._copy_object_xml_and_rename_object(aux_object_dir, object_xml_template)      