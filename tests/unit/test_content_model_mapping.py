import pytest, sys, os.path, shutil, os
sys.path.append('app')
import translation_service.translate_data_structure_service as translate_data_structure_service 
from content_model_mapping.opaque_content_model_mapping import OpqaueContentModelMapping

def test_opaque_cm_mapping():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/doi-translation-service-test"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")
    
    batch_name = os.path.basename(loc) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    object_dir = os.path.join(batch_dir, object_name)

    aux_object_dir = os.path.join(package_path, "_aux", batch_name, object_name)
    os.makedirs(aux_object_dir, exist_ok=True)
    os.makedirs(object_dir, exist_ok=True)
    opaque_cmm = OpqaueContentModelMapping(os.getenv("EXTRACTED_PACKAGE_DVN", "True"))
    batch_dir = opaque_cmm.handle_directory_mapping(loc)
    assert(expected_batch_dir == batch_dir)
    
    obj_dir = os.path.join(batch_dir, os.path.basename(loc, object_dir, aux_object_dir))
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
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))

def test_opaque_cm_doc_only():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/doi-translation-service-test-doc-only"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")
    
    opaque_cmm = OpqaueContentModelMapping(os.getenv("EXTRACTED_PACKAGE_DVN", "True"))
    batch_dir = opaque_cmm.handle_directory_mapping(loc)
    assert(expected_batch_dir == batch_dir)
    
    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir= os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))
    
    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    #Check that all files are where they are expected to be
    assert not os.path.exists(os.path.join(obj_dir, "content"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "bag-info.txt"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "bagit.txt"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "manifest-md5.txt"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "datacite.xml"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "oai-ore.jsonld"))
    assert os.path.exists(os.path.join(obj_dir, "documentation", "pid-mapping.txt"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))

         
def cleanup_batch_dirs(batch_path, aux_dir, project_conf):
    '''Removes the newly created batch folders'''
    try:
        shutil.rmtree(batch_path)
        shutil.rmtree(aux_dir)
        os.remove(project_conf)
        base_dropbox_dir = os.getenv("BASE_DROPBOX_PATH")
        dropbox_name_for_testing=os.getenv("TEST_DROPBOX_NAME", "")
        #Real dropboxes us the 'incoming' directory
        if dropbox_name_for_testing != "":
            dropbox_name_for_testing = os.path.join(dropbox_name_for_testing, "incoming")
    
        shutil.rmtree(os.path.join(base_dropbox_dir, dropbox_name_for_testing, os.path.basename(batch_path)))
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))