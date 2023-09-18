import pytest, sys, os.path, shutil, os
sys.path.append('app')
from translate_data_structure.dataverse_translate_data_structure_service import DataverseTranslateDataStructureService
from translate_data_structure.epadd_translate_data_structure_service import EpaddTranslateDataStructureService
from translate_data_structure.etd_translate_data_structure_service import ETDTranslateDataStructureService

def test_translate_dvn_data_structure():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/doi-translation-service-test"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")
    
    dvn_translate_svc = DataverseTranslateDataStructureService()
    batch_dir = dvn_translate_svc.translate_data_structure(loc)
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
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))

def test_translate_dvn_data_structure_doc_only():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/doi-translation-service-test-doc-only"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")
    
    dvn_translate_svc = DataverseTranslateDataStructureService()
    batch_dir = dvn_translate_svc.translate_data_structure(loc)
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


def test_translate_epadd_data_structure_zip():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/epadd-export-test-zip"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    epadd_translate_svc = EpaddTranslateDataStructureService()
    batch_dir = epadd_translate_svc.translate_data_structure(loc)
    assert (expected_batch_dir == batch_dir)

    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir = os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "container", "test_export.zip"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))
    
def test_translate_epadd_data_structure_7z():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/epadd-export-test-7z"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    epadd_translate_svc = EpaddTranslateDataStructureService()
    batch_dir = epadd_translate_svc.translate_data_structure(loc)
    assert (expected_batch_dir == batch_dir)

    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir = os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "container", "test.7z"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))

    
def test_translate_epadd_data_structure_gz():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/epadd-export-test-gz"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    epadd_translate_svc = EpaddTranslateDataStructureService()
    batch_dir = epadd_translate_svc.translate_data_structure(loc)
    assert (expected_batch_dir == batch_dir)

    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir = os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "container", "test.gz"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))


def test_translate_etd_data_structure_document():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/document_cm"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc)
    assert (expected_batch_dir == batch_dir)

    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir = os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "document", "test.pdf"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))


def test_translate_etd_data_structure_text():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/text_cm"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc)
    assert (expected_batch_dir == batch_dir)

    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir = os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "text", "test.csv"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))


def test_translate_etd_data_structure_still_image():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/stillimage_cm"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc)
    assert (expected_batch_dir == batch_dir)

    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir = os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "image", "test.gif"))
    assert os.path.exists(os.path.join(obj_dir, "image", "test2.gif"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))


def test_translate_etd_data_structure_audio():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/audio_cm"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc)
    assert (expected_batch_dir == batch_dir)

    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir = os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "audio", "test.mp3"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))


def test_translate_etd_data_structure_opaque():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/opaque_etd_cm"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc)
    assert (expected_batch_dir == batch_dir)

    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir = os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "content", "test-zip.txt.gz"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))


def test_translate_etd_data_structure_multiple_cm():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/multiple_cm"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc)
    assert (expected_batch_dir == batch_dir)

    obj_dir = os.path.join(batch_dir, os.path.basename(loc))
    obj_aux_dir = os.path.join(loc, "_aux", os.path.basename(loc) + "-batch", os.path.basename(loc))

    assert os.path.exists(obj_dir)
    assert os.path.exists(obj_aux_dir)

    # Check that all files are where they are expected to be
    assert os.path.exists(os.path.join(obj_dir, "document", "test.pdf"))
    assert os.path.exists(os.path.join(obj_dir, "text", "test.csv"))
    assert os.path.exists(os.path.join(obj_dir, "image", "test.gif"))
    assert os.path.exists(os.path.join(obj_dir, "image", "test2.gif"))
    assert os.path.exists(os.path.join(obj_dir, "audio", "test.mp3"))
    assert os.path.exists(os.path.join(obj_dir, "content", "test-zip.txt.gz"))
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