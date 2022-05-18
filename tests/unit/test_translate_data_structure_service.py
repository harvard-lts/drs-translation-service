import pytest, sys, os.path, shutil
sys.path.append('app')
import translation_service.translate_data_structure_service as translate_data_structure_service 

def test_translate_data_structure():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/doi-translation-service-test"
    assert translate_data_structure_service.translate_data_structure(loc)
    #Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(loc, "content", "test1.Bin"))
    assert os.path.exists(os.path.join(loc, "content", "test2.Bin"))
    assert os.path.exists(os.path.join(loc, "content", "test3.Bin"))
    assert os.path.exists(os.path.join(loc, "documentation", "bag-info.txt"))
    assert os.path.exists(os.path.join(loc, "documentation", "bagit.txt"))
    assert os.path.exists(os.path.join(loc, "documentation", "manifest-md5.txt"))
    assert os.path.exists(os.path.join(loc, "documentation", "datacite.xml"))
    assert os.path.exists(os.path.join(loc, "documentation", "oai-ore.jsonld"))
    assert os.path.exists(os.path.join(loc, "documentation", "pid-mapping.txt"))
    assert os.path.exists(os.path.join(loc, "documentation", "doi-translation-service-test_datacite.v1.0.xml"))
    cleanup_content_and_documentation(loc)
    
def cleanup_content_and_documentation(dir_path):
    '''Removes the newly created content and documentation folders'''
    try:
        shutil.rmtree(os.path.join(dir_path, "content"))
        shutil.rmtree(os.path.join(dir_path, "documentation"))
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))