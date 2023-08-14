import os
import os.path
from abc import abstractmethod, ABC

class TranslateDataStructureService(ABC):
           
    def translate_data_structure(self, package_path):
        batch_name = os.path.basename(package_path) + "-batch"
        batch_dir = os.path.join(package_path, batch_name)
        # Object name is the same as the package name
        object_name = os.path.basename(package_path)
        object_dir = os.path.join(batch_dir, object_name)
    
        aux_object_dir = os.path.join(package_path, "_aux", batch_name, object_name)
        os.makedirs(aux_object_dir, exist_ok=True)
        os.makedirs(object_dir, exist_ok=True)
        self._handle_content_model_mapping(package_path, object_dir, aux_object_dir)
        
        return batch_dir

    @abstractmethod
    def _handle_content_model_mapping(self, package_path, object_dir, aux_object_dir):
        pass