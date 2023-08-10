from abc import ABC, abstractmethod

class ContentModelMapping(ABC):
    '''Abstract class that defines how to map the data for the 
    inheriting content models.  Inheriting classes will perform
    the actual mapping'''
        
    @abstractmethod
    def handle_directory_mapping(self):
        pass
    
    def _move_files(self):
        '''Moves files to their proper content model directories
        '''
        pass
    
    def _copy_project_conf(self):
        '''Copies the project conf to the project directory'''
        pass
    
    def _copy_object_xml_and_rename_object(self):
        '''Copies the project conf to the proper location and renames OBJECT_NAME
        to the new object name'''
        pass
    
    
    