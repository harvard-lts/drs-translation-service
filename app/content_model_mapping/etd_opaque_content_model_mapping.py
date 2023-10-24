import os
import shutil
import glob
from content_model_mapping.content_model_mapping import ContentModelMapping

class ETDOpaqueContentModelMapping(ContentModelMapping):
    
    def __init__(self):
        super().__init__()
        
    def handle_directory_mapping(self, package_path, object_dir, aux_object_dir):
        self.logger.debug("Formatting for opaque content model")
        content_dir = os.path.join(object_dir, "content")
        if not os.path.exists(content_dir):
            os.mkdir(content_dir)
        # Required directory even if not used
        documentation_dir = os.path.join(object_dir, "documentation")
        if not os.path.exists(documentation_dir):
            os.mkdir(documentation_dir)
        
        document_suffixes = ["pdf", "doc", "docx", "wp", "wpd", "epub", "rtf"]
        stillimage_suffixes = ["jpg", "jp2", "gif", "tif", "tiff"]
        audio_suffixes = ["wav", "mp3", "mp4", "aifc", "m2a"]
        text_suffixes = ["txt", "xml", "csv", "java", "pl", "py", "rb", "sh", "c", "cpp", "h", "hpp", "js", "css", "html", "htm", "php", "json", "md", "r", "sql", "tsv", "yml"]
        excluded_suffixes = document_suffixes + stillimage_suffixes + audio_suffixes + text_suffixes

        self.logger.debug("globbing...")

        for file in glob.glob(os.path.join(package_path, '*.*')):
            self.logger.debug("Found package: %s", file)
            filename = os.path.basename(file)
            suffix = filename.split(".")[-1]
            if suffix not in excluded_suffixes:
                shutil.copy2(file, os.path.join(content_dir, filename))

        project_conf = os.getenv("OPAQUE_PROJECT_CONF_TEMPLATE")
        self._copy_project_conf(package_path, project_conf)
        object_xml_template = os.getenv("OPAQUE_OBJECT_XML_TEMPLATE")
        self._copy_object_xml_and_rename_object(aux_object_dir, object_xml_template)

    
   