import pytest, sys, os.path, shutil, os
sys.path.append('app')
from translate_data_structure.dataverse_translate_data_structure_service import DataverseTranslateDataStructureService
from translate_data_structure.epadd_translate_data_structure_service import EpaddTranslateDataStructureService
from translate_data_structure.etd_translate_data_structure_service import ETDTranslateDataStructureService
from translation_service.translation_exceptions import TranslationException

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


def test_translate_etd_data_structure_missing_file_sec_data():
    '''Verifies that missing fileSec data results in a failure'''
    loc = "/home/appuser/tests/data/etd-missing-filesec-data"
    with pytest.raises(TranslationException):
        etd_translate_svc = ETDTranslateDataStructureService()
        batch_dir = etd_translate_svc.translate_data_structure(loc, {"school_dropbox_name": "dce"})
        
    cleanup_batch_dirs(os.path.join(loc, "etd-missing-filesec-data-batch"), os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))


def test_translate_etd_data_structure_without_mets():
    '''Verifies that lack of a mets file throws an exception'''
    with pytest.raises(TranslationException):
    
        loc = "/home/appuser/tests/data/etd-no-mets"
        etd_translate_svc = ETDTranslateDataStructureService()
        batch_dir = etd_translate_svc.translate_data_structure(loc, {"school_dropbox_name": "dce"})

def test_translate_etd_submission_1():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/etd-submission-1"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc, {"school_dropbox_name": "dce"})
    assert (expected_batch_dir == batch_dir)
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_THESIS_dce_2022_PQ_29161227", 
                                       "document", "ES_100_Final_Thesis_PDF_-_Liam_Nuttall.pdf"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_LICENSE_dce_2022_PQ_29161227", 
                                       "document", "Harvard_IR_License_-_LAA_for_ETDs__2020_.pdf"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_DOCUMENTATION_dce_2022_PQ_29161227", 
                                       "text", "mets.xml"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_DOCUMENTATION_dce_2022_PQ_29161227", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_LICENSE_dce_2022_PQ_29161227", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_THESIS_dce_2022_PQ_29161227", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(loc, "_aux", "template", 
                                        "object_mapping.txt"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))
    shutil.rmtree(os.path.join(loc, "extracted"))

def test_translate_etd_submission_2():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/etd-submission-2"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc, {"school_dropbox_name": "dce"})
    assert (expected_batch_dir == batch_dir)
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_THESIS_dce_2011_PQ_1496780", 
                                       "document", "TurkeyandtheEU-EuropeanSoftPowerandHowItHasImpactedTurkey.pdf"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_DOCUMENTATION_dce_2011_PQ_1496780", 
                                       "text", "mets.xml"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_THESIS_dce_2011_PQ_1496780", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_DOCUMENTATION_dce_2011_PQ_1496780", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(loc, "_aux", "template", 
                                        "object_mapping.txt"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))

def test_format_etd_osn():
    etd_translate_svc = ETDTranslateDataStructureService()
    thesis = etd_translate_svc.format_etd_osn("dce", "TurkeyandtheEU-EuropeanSoftPowerandHowItHasImpactedTurkey.pdf", 
                                              "/home/appuser/tests/data/etd-submission-2/mets.xml")
    expected_thesis = "ETD_THESIS_dce_2011_PQ_1496780"
    assert expected_thesis == thesis
    
    mets = etd_translate_svc.format_etd_osn("dce", "mets.xml", 
                                              "/home/appuser/tests/data/etd-submission-2/mets.xml")
    expected_mets = "ETD_DOCUMENTATION_dce_2011_PQ_1496780"
    assert expected_mets == mets

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