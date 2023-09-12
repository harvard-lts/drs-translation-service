import pytest, sys, os.path, shutil, os
sys.path.append('app')
from content_model_mapping.opaque_content_model_mapping import OpqaueContentModelMapping
from content_model_mapping.opaque_container_content_model_mapping import OpqaueContainerContentModelMapping
from content_model_mapping.text_content_model_mapping import TextContentModelMapping
from content_model_mapping.audio_content_model_mapping import AudioContentModelMapping
from content_model_mapping.document_content_model_mapping import DocumentContentModelMapping
from content_model_mapping.still_image_content_model_mapping import StillImageContentModelMapping

def test_map_opaque_cm_mapping():
    '''Formats the directory and verifies that all files ended up where they should be'''
    package_path = "/home/appuser/tests/data/doi-translation-service-test"
    expected_batch_dir = os.path.join(package_path, os.path.basename(package_path) + "-batch")
    
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    obj_dir = os.path.join(batch_dir, object_name)
    obj_aux_dir = os.path.join(package_path, "_aux", batch_name, object_name)
    os.makedirs(obj_aux_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    opaque_cmm = OpqaueContentModelMapping(os.getenv("EXTRACTED_PACKAGE_DVN", "True"))
    opaque_cmm.handle_directory_mapping(package_path, obj_dir, obj_aux_dir)
    
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
    cleanup_batch_dirs(batch_dir, os.path.join(package_path, "_aux"), os.path.join(package_path, "project.conf"))

def test_map_opaque_cm_doc_only():
    '''Formats the directory and verifies that all files ended up where they should be'''
    package_path = "/home/appuser/tests/data/doi-translation-service-test-doc-only"
    expected_batch_dir = os.path.join(package_path, os.path.basename(package_path) + "-batch")
    
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    obj_dir = os.path.join(batch_dir, os.path.basename(package_path))
    obj_aux_dir= os.path.join(package_path, "_aux", os.path.basename(package_path) + "-batch", os.path.basename(package_path))
    os.makedirs(obj_aux_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    opaque_cmm = OpqaueContentModelMapping(os.getenv("EXTRACTED_PACKAGE_DVN", "True")) 
    opaque_cmm.handle_directory_mapping(package_path, obj_dir, obj_aux_dir)
    
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
    cleanup_batch_dirs(batch_dir, os.path.join(package_path, "_aux"), os.path.join(package_path, "project.conf"))

def test_map_opaque_container_cm_zip():
    '''Formats the directory and verifies that all files ended up where they should be'''
    package_path = "/home/appuser/tests/data/epadd-export-test-zip"
    
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    obj_dir = os.path.join(batch_dir, os.path.basename(package_path))
    obj_aux_dir= os.path.join(package_path, "_aux", os.path.basename(package_path) + "-batch", os.path.basename(package_path))
    os.makedirs(obj_aux_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    opaque_container_cmm = OpqaueContainerContentModelMapping() 
    opaque_container_cmm.handle_directory_mapping(package_path, obj_dir, obj_aux_dir)

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "container", "test_export.zip"))
    cleanup_batch_dirs(batch_dir, os.path.join(package_path, "_aux"), os.path.join(package_path, "project.conf"))
    
def test_map_opaque_container_cm_7z():
    '''Formats the directory and verifies that all files ended up where they should be'''
    package_path = "/home/appuser/tests/data/epadd-export-test-7z"
    
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    obj_dir = os.path.join(batch_dir, os.path.basename(package_path))
    obj_aux_dir= os.path.join(package_path, "_aux", os.path.basename(package_path) + "-batch", os.path.basename(package_path))
    os.makedirs(obj_aux_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    opaque_container_cmm = OpqaueContainerContentModelMapping() 
    opaque_container_cmm.handle_directory_mapping(package_path, obj_dir, obj_aux_dir)

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "container", "test.7z"))
    cleanup_batch_dirs(batch_dir, os.path.join(package_path, "_aux"), os.path.join(package_path, "project.conf"))
    
def test_map_opaque_container_cm_gz():
    '''Formats the directory and verifies that all files ended up where they should be'''
    package_path = "/home/appuser/tests/data/epadd-export-test-gz"
    
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    obj_dir = os.path.join(batch_dir, os.path.basename(package_path))
    obj_aux_dir= os.path.join(package_path, "_aux", os.path.basename(package_path) + "-batch", os.path.basename(package_path))
    os.makedirs(obj_aux_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    opaque_container_cmm = OpqaueContainerContentModelMapping() 
    opaque_container_cmm.handle_directory_mapping(package_path, obj_dir, obj_aux_dir)
    
    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "container", "test.gz"))
    cleanup_batch_dirs(batch_dir, os.path.join(package_path, "_aux"), os.path.join(package_path, "project.conf"))

def test_map_document_cm_mapping():
    package_path = "/home/appuser/tests/data/document_cm"
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    obj_dir = os.path.join(batch_dir, os.path.basename(package_path))
    obj_aux_dir= os.path.join(package_path, "_aux", os.path.basename(package_path) + "-batch", os.path.basename(package_path))
    os.makedirs(obj_aux_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    document_cmm = DocumentContentModelMapping()
    document_cmm.handle_directory_mapping(package_path, obj_dir, obj_aux_dir)
    
    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "document", "test.pdf"))
    cleanup_batch_dirs(batch_dir, os.path.join(package_path, "_aux"), os.path.join(package_path, "project.conf"))

def test_map_text_cm_mapping():
    package_path = "/home/appuser/tests/data/text_cm"
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    obj_dir = os.path.join(batch_dir, os.path.basename(package_path))
    obj_aux_dir= os.path.join(package_path, "_aux", os.path.basename(package_path) + "-batch", os.path.basename(package_path))
    os.makedirs(obj_aux_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    text_cmm = TextContentModelMapping()
    text_cmm.handle_directory_mapping(package_path, obj_dir, obj_aux_dir)
    
    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "text", "test.csv"))
    cleanup_batch_dirs(batch_dir, os.path.join(package_path, "_aux"), os.path.join(package_path, "project.conf"))
 
def test_map_audio_cm_mapping():
    package_path = "/home/appuser/tests/data/audio_cm"
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    obj_dir = os.path.join(batch_dir, os.path.basename(package_path))
    obj_aux_dir= os.path.join(package_path, "_aux", os.path.basename(package_path) + "-batch", os.path.basename(package_path))
    os.makedirs(obj_aux_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    audio_cmm = AudioContentModelMapping()
    audio_cmm.handle_directory_mapping(package_path, obj_dir, obj_aux_dir)
    
    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "audio", "test.mp4"))
    cleanup_batch_dirs(batch_dir, os.path.join(package_path, "_aux"), os.path.join(package_path, "project.conf"))
 
def test_map_still_image_cm_mapping():
    package_path = "/home/appuser/tests/data/still_image_cm"
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    obj_dir = os.path.join(batch_dir, os.path.basename(package_path))
    obj_aux_dir= os.path.join(package_path, "_aux", os.path.basename(package_path) + "-batch", os.path.basename(package_path))
    os.makedirs(obj_aux_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    still_image_cmm = StillImageContentModelMapping()
    still_image_cmm.handle_directory_mapping(package_path, obj_dir, obj_aux_dir)
    
    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "still_image", "test.gif"))
    assert os.path.exists(os.path.join(obj_dir, "still_image", "test2.gif"))
    cleanup_batch_dirs(batch_dir, os.path.join(package_path, "_aux"), os.path.join(package_path, "project.conf"))
         
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