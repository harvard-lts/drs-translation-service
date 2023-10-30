from abc import ABC, abstractmethod
import os
import os.path
import logging
import shutil


class TranslationService(ABC):
    '''Abstract class that defines how to translate the data for the 
    inheriting classes.  Inheriting classes will perform
    the actual translation'''
    
    def __init__(self):
        self.logger = logging.getLogger('dts')
        self.base_load_report_dir = os.getenv("BASE_LOADREPORT_PATH")
        self.sample_load_report="/home/appuser/tests/data/sampleloadreport/LOADREPORT_sample.txt"

    @abstractmethod
    def get_admin_metadata(self, drs_config_path):
        pass

    @abstractmethod
    def _get_batch_builder_service(self):
        pass

    @abstractmethod
    def _get_translate_data_structure_service(self):
        pass

    def prepare_and_send_to_drs(self, package_dir, supplemental_deposit_data, testing=False):
        # Set up directories
        batch_name = os.path.basename(package_dir) + "-batch"
        batch_dir = os.path.join(package_dir, batch_name)
        
        translate_service = self._get_translate_data_structure_service()
        
        batch_builder_service = self._get_batch_builder_service()
        
        translate_service.translate_data_structure(package_dir, supplemental_deposit_data)
        # Run BB
        batch_builder_service.process_batch(package_dir, batch_name, supplemental_deposit_data)
        
        # Move Batch to incoming
        batch_dir = self.__move_batch_to_incoming(package_dir, batch_dir)
        
        if not testing:
            # Remove old project dir
            self.__cleanup_project_dir(package_dir)
        
        # Update batch_dir permissions
        self.__update_permissions(batch_dir)
        
        # Add LOADING file to package directory if we are not testing
        if not testing:
            self.__create_loading_file(batch_dir)
        # If testing, place a mock load report to allow for the flow to continue
        else:
            if ('dropbox_name' not in supplemental_deposit_data):
                raise Exception("When testing, dropbox_name must be supplied in the supplemental deposit data")
            self.__place_mock_load_report(os.path.basename(batch_dir), supplemental_deposit_data["dropbox_name"])
        
        return batch_dir

    def __move_batch_to_incoming(self, project_dir, batch_dir):
        # dropbox is the path above the project
        dropbox_path = os.path.dirname(project_dir)
        shutil.move(batch_dir, dropbox_path)
        return os.path.join(dropbox_path, os.path.basename(batch_dir))   

    def __cleanup_project_dir(self, project_dir):
        '''Remove project directory'''
        shutil.rmtree(project_dir) 

    def __create_loading_file(self, batch_dir):
        '''Creates a LOADING file for DRS'''
        loading_file = os.path.join(batch_dir, "LOADING")
        open(loading_file, 'a').close()

    def __update_permissions(self, batch_dir):
        '''
        Sets group and r/w permission for DRS as follows:
            Directory - batch_dir
            User - hdc3aadm (55020)
            Group - guestftp (4000)
        '''
        for root, dirs, files in os.walk(batch_dir):
            for dir in dirs:
                os.chown(os.path.join(root, dir), 55020, 4000)
                os.chmod(os.path.join(root, dir), 0o775)
            for file in files:
                os.chown(os.path.join(root, file), 55020, 4000)
                os.chmod(os.path.join(root, file), 0o775)
        os.chown(batch_dir, 55020, 4000)
        os.chmod(batch_dir, 0o775)

    def __place_mock_load_report(self, batch_name, dropbox_name):
        # Make sure to append incoming if it is a real dropbox
        if dropbox_name != "":
            dropbox_name = os.path.join(dropbox_name, "incoming")
        batch_load_report_dir = os.path.join(self.base_load_report_dir, dropbox_name, batch_name)
        # Create dir in LR dir
        os.mkdir(batch_load_report_dir)
        
        mock_load_report_name = "LOADREPORT_{}.txt".format(batch_name)
        mock_load_report_dest = os.path.join(batch_load_report_dir, mock_load_report_name)
        shutil.copy(self.sample_load_report, mock_load_report_dest)
        