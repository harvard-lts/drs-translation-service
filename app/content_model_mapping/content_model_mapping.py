from abc import ABC, abstractmethod
import shutil
import os
import os.path
import logging

class ContentModelMapping(ABC):
    '''Abstract class that defines how to map the data for the 
    inheriting content models.  Inheriting classes will perform
    the actual mapping'''
    
    def __init__(self):
        self.logger = logging.getLogger('dts')
    
    @abstractmethod
    def handle_directory_mapping(self, package_path, object_dir, aux_object_dir):
        pass

    def handle_single_file_directory_mapping(self, filename_path, package_path, object_dir, aux_object_dir):
        pass

    def _handle_project_conf_and_object_xml(self, package_path, aux_object_dir, project_conf_template, object_xml_template):
        self._copy_project_conf(package_path, project_conf_template)
        self._copy_object_xml_and_rename_object(aux_object_dir, object_xml_template)
                                
    def _move_files(self, root_dir, source, dest_dir):
        '''This method actually copies the files from source to destination rather than
        moves them to preserve the original structure and to aid in error handling'''
        if (os.path.isfile(source)):
            self.logger.debug("Moving {} to {}".format(os.path.join(root_dir, source), os.path.join(dest_dir, source)))
            shutil.copy2(os.path.join(root_dir, source), os.path.join(dest_dir, os.path.basename(source)))
        else:
            for root, subdirs, files in os.walk(source):
                for subdir in subdirs:
                    self._move_files(os.path.join(root, subdir), os.path.join(root, subdir), dest_dir)
                for filename in files:
                    shutil.copy2(os.path.join(root, filename), os.path.join(dest_dir, filename))
    
    def _copy_project_conf(self, project_dir, project_conf):
        '''Copies the project conf to the project directory'''
        shutil.copy2(project_conf, os.path.join(project_dir, "project.conf"))
    
    def _copy_object_xml_and_rename_object(self, aux_object_dir, object_xml_template):
        '''Copies the project conf to the proper location and renames OBJECT_NAME
        to the new object name'''
        object_xml = os.path.join(aux_object_dir, "object.xml")
        object_name = os.path.basename(aux_object_dir)
    
        # Read in the template file
        with open(object_xml_template, 'r') as file:
            filedata = file.read()
    
        # Replace the object name
        filedata = filedata.replace('OBJECT_NAME', object_name)
    
        # Write the object.xml file out in the aux directory
        with open(object_xml, 'w') as file:
            file.write(filedata)
    
    
    