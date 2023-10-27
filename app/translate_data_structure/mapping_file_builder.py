import logging
import os.path


logger = logging.getLogger('dts')

class MappingFileBuilder:
    
    def build_mapping_file(self, object_osn, relative_file_path, supplemental_metadata, mapping_file_dest):
        mapping_file = MappingFile(object_osn, relative_file_path)
        mapping_file.dash_id = supplemental_metadata.get("dash_id")
        mapping_file.alma_id = supplemental_metadata.get("alma_id")
        mapping_file.pq_id = supplemental_metadata.get("pq_id")
        self.__write_mapping_file(mapping_file, os.path.join(mapping_file_dest, "mapping.txt"))

    def build_object_mapping_file(self, object_osn, supplemental_metadata, mapping_file_dest):
        mapping_file = ObjectMappingFile(object_osn, supplemental_metadata.get("alma_id", ""))
        self.__write_mapping_file(mapping_file, os.path.join(mapping_file_dest, "object_mapping.txt"))

    def __write_mapping_file(self, mapping_file, mapping_file_dest):
        f = open(mapping_file_dest, "w")
        f.write(mapping_file.get_mapping_string())
        f.close()

class MappingFile:
    def __init__(self, object_osn, relative_file_path):
        self.file_osn = object_osn + "_1"
        self.relative_file_path = relative_file_path
        print(self.file_osn)
        print(self.relative_file_path)
        self.dash_id = None
        self.alma_id = None
        self.pq_id = None

    def get_mapping_string(self):
        return "{},{},,,,{},".format(self.relative_file_path, self.file_osn, self.__create_hml_string())
    
    def __create_hml_string(self):
        hml_string = ""
        dash_string = self.__create_dash_string()
        alma_string = self.__create_alma_string()
        pq_string = self.__create_pq_string()
        if dash_string is not None:
            hml_string = dash_string
        if alma_string is not None:
            hml_string += alma_string
        if pq_string is not None:
            hml_string += pq_string
        return hml_string

    def __create_dash_string(self):
        if self.dash_id is not None:
            return "DASH|{}|Dash|".format(self.dash_id)
        return None
    
    def __create_alma_string(self):
        if self.alma_id is not None:
            return "Alma|{}|Alma|".format(self.alma_id)
        return None
    
    def __create_pq_string(self):
        if self.pq_id is not None:
            if not self.pq_id.startswith("PQ"):
                self.pq_id = "PQ-" + self.pq_id
            return "Local|{}|ProQuestID|".format(self.pq_id)
        return None


class ObjectMappingFile:
    def __init__(self, obj_dir_name, alma_id):
        self.obj_dir_name = obj_dir_name
        self.alma_id = alma_id

    def get_mapping_string(self):
        return "{},{},".format(self.obj_dir_name, self.alma_id)
