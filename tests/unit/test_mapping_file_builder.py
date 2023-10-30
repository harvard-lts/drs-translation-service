import sys
import os.path
import os
sys.path.append('app')
from translate_data_structure.mapping_file_builder import MappingFileBuilder


def test_mapping_file():
    dest_dir = "/home/appuser/tests/data/mapping-file-tests"
    builder = MappingFileBuilder()
    builder.build_mapping_file("TEST_OSN", 
                                "document/somedoc.pdf", 
                                {"dash_id": "DASH1234", "alma_id": "Alma1234", "pq_id": "PQ-1234"}, 
                                dest_dir)

    expected_string = "document/somedoc.pdf,TEST_OSN_1,,,,DASH|DASH1234|Dash||Alma|Alma1234|Alma||Local|PQ-1234|ProQuestID|,"
    full_dest_dir = os.path.join(dest_dir, "mapping.txt")
    assert os.path.exists(full_dest_dir)
    f = open(full_dest_dir, "r")
    text = f.read()
    assert expected_string == text
    os.remove(full_dest_dir)

def test_object_mapping_file():
    dest_dir = "/home/appuser/tests/data/mapping-file-tests"
    builder = MappingFileBuilder()
    builder.build_object_mapping_file("TEST_OSN", 
                                {"dash_id": "DASH1234", "alma_id": "Alma1234", "pq_id": "PQ-1234"}, 
                                dest_dir)

    expected_string = "TEST_OSN,Alma1234,"
    full_dest_dir = os.path.join(dest_dir, "object_mapping.txt")
    assert os.path.exists(full_dest_dir)
    f = open(full_dest_dir, "r")
    text = f.read()
    assert expected_string == text
    os.remove(full_dest_dir)