import os
import shutil
import glob
from content_model_mapping.content_model_mapping import ContentModelMapping

class StillImageContentModelMapping(ContentModelMapping):
    def handle_directory_mapping(self, package_path, object_dir, aux_object_dir):
        '''Moves the container into the container directory'''
        self.logger.debug("Formatting for still image content model")
        container_dir = os.path.join(object_dir, "container")
        if not os.path.exists(container_dir):
            os.mkdir(container_dir)

        suffixes = ["jpg", "jp2", "gif", "tif", "tiff"]]

        self.logger.debug("globbing...")

        self.logger.debug("globbing...")
        for suffix in suffixes:
            for file in glob.glob(os.path.join(package_path, '*.' + suffix)):
                self.logger.debug("Found package: %s", file)
                filename = os.path.basename(file)
                if f".{suffix}" in filename:
                    shutil.copy2(file, os.path.join(container_dir, filename))

        project_conf = os.getenv("STILL_IMAGE_PROJECT_CONF_TEMPLATE")        
        self._copy_project_conf(package_path, project_conf)
        object_xml_template = os.getenv("STILL_IMAGE_OBJECT_XML_TEMPLATE")
        self._copy_object_xml_and_rename_object(aux_object_dir, object_xml_template)    