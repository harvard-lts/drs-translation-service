import pytest, sys, os.path, shutil
sys.path.append('app')
import translation_service.translate_data_structure_service as translate_data_structure_service 

def test_translate_data_structure():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/doi-translation-service-test"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")
    
    batch_dir = translate_data_structure_service.translate_data_structure(loc)
    assert(expected_batch_dir == batch_dir)
    
    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir= os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))
    
    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    #Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "content", "test1.Bin"))
    assert os.path.exists(os.path.join(obj_dir, "content", "test2.Bin"))
    assert os.path.exists(os.path.join(obj_dir, "content", "test3.Bin"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "bag-info.txt"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "bagit.txt"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "manifest-md5.txt"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "datacite.xml"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "oai-ore.jsonld"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "pid-mapping.txt"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "doi-translation-service-test_datacite.v1.0.xml"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))
    
def cleanup_batch_dirs(batch_path, aux_dir, project_conf):
    '''Removes the newly created batch folders'''
    try:
        shutil.rmtree(batch_path)
        shutil.rmtree(aux_dir)
        os.remove(project_conf)
        shutil.rmtree(os.path.join(os.getenv("DROPBOX_PATH"), os.path.basename(batch_path)))
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))