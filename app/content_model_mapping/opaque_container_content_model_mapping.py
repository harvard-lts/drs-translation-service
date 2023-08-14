import os
import shutil
from content_model_mapping.content_model_mapping import ContentModelMapping
from pathlib import Path

class OpqaueContainerContentModelMapping(ContentModelMapping):
        
    def handle_directory_mapping(self, package_path, object_dir, aux_object_dir):
        '''Moves the container into the container directory'''
        self.logger.debug("Formatting for opaque container content model")
        hascontent = False
        container_dir = os.path.join(object_dir, "container")
        if not os.path.exists(container_dir):
            os.mkdir(container_dir)

        # Copy zip/gz/7z
        self.logger.debug("globbing...")
    
        for file in Path(package_path).glob('*.zip'):
            self.logger.debug("Found package: %s", file)
            filename = os.path.basename(file)
            if ".zip" in filename:
                shutil.copy2(file, os.path.join(container_dir, filename))
                hascontent = True
    
        for file in Path(package_path).glob('*.7z'):
            self.logger.debug("Found package: %s", file)
            filename = os.path.basename(file)
            if ".7z" in filename:
                shutil.copy2(file, os.path.join(container_dir, filename))
                hascontent = True
                
        for file in Path(package_path).glob('*.gz'):
            self.logger.debug("Found package: %s", file)
            filename = os.path.basename(file)
            if ".gz" in filename:
                shutil.copy2(file, os.path.join(container_dir, filename))
                hascontent = True
                
        project_conf = os.getenv("OPAQUE_CONTAINER_PROJECT_CONF_TEMPLATE")        
        self._copy_project_conf(package_path, project_conf)
        object_xml_template = os.getenv("OPAQUE_CONTAINER_OBJECT_XML_TEMPLATE")
        self._copy_object_xml_and_rename_object(aux_object_dir, object_xml_template)
