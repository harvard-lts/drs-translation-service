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

def test_translate_etd_submission_1():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/etd-submission-1"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    supplemental_deposit_data = {"alma_id": "Alma1234",
              "pq_id": "1234",
              "dash_id": "dash1234",
              "ownerCode": "HUL.TEST",
              "urnAuthorityPath": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "urnAuthorityPath": "HUL.TEST",
              "file_info": {"Harvard_IR_License_-_LAA_for_ETDs_(2020).pdf": {
                                "modified_file_name": "Harvard_IR_License_-_LAA_for_ETDs__2020_.pdf",
                                "file_role": "LICENSE",
                                "object_role": "LICENSE",
                                "object_osn": "ETD_LICENSE_dce_2022_PQ_29161227",
                                "file_osn": "ETD_LICENSE_dce_2022_PQ_29161227_1"
                            },
                            "ES 100 Final Thesis PDF - Liam Nuttall.pdf": {
                                "modified_file_name": "ES_100_Final_Thesis_PDF_-_Liam_Nuttall.pdf",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS",
                                "object_osn": "ETD_THESIS_dce_2022_PQ_29161227",
                                "file_osn": "ETD_THESIS_dce_2022_PQ_29161227_1"
                            },
                            "mets.xml": {
                                "modified_file_name": "mets.xml",
                                "file_role": "DOCUMENTATION",
                                "object_role": "DOCUMENTATION",
                                "object_osn": "ETD_DOCUMENTATION_dce_2022_PQ_29161227",
                                "file_osn": "ETD_DOCUMENTATION_dce_2022_PQ_29161227_1"
                            }
                            }}
    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc, supplemental_deposit_data)
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

    supplemental_deposit_data = {"alma_id": "Alma1234",
              "pq_id": "1234",
              "dash_id": "dash1234",
              "ownerCode": "HUL.TEST",
              "urnAuthorityPath": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "urnAuthorityPath": "HUL.TEST",
              "file_info": {"TurkeyandtheEU-EuropeanSoftPowerandHowItHasImpactedTurkey.pdf": {
                                                    "modified_file_name": "TurkeyandtheEU-EuropeanSoftPowerandHowItHasImpactedTurkey.pdf",
                                                    "file_role": "ARCHIVAL_MASTER",
                                                    "object_role": "THESIS",
                                                    "object_osn": "ETD_THESIS_dce_2011_PQ_1496780",
                                                    "file_osn": "ETD_THESIS_dce_2011_PQ_1496780_1"
                                               },
                                               "mets.xml": {
                                                    "modified_file_name": "mets.xml",
                                                    "file_role": "DOCUMENTATION",
                                                    "object_role": "DOCUMENTATION",
                                                    "object_osn": "ETD_DOCUMENTATION_dce_2011_PQ_1496780",
                                                    "file_osn": "ETD_DOCUMENTATION_dce_2011_PQ_1496780_1"
                                               }
                                 }}
    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc, supplemental_deposit_data)
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

def test_translate_etd_submission_images():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/etd-submission-image"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    supplemental_deposit_data = {"alma_id": "99156631569803941",
              "pq_id": "28542548",
              "dash_id": "dash1234",
              "ownerCode": "HUL.TEST",
              "urnAuthorityPath": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "urnAuthorityPath": "HUL.TEST",
              "file_info": {"20210524_Thesis Archival Submission_JB Signed.pdf": {
                                "modified_file_name": "20210524_Thesis_Archival_Submission_JB_Signed.pdf",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS",
                                "object_osn": "ETD_THESIS_gsd_2021-05_PQ_28542548",
                                "file_osn": "ETD_THESIS_gsd_2021-05_PQ_28542548_1"
                            },
                            "mets.xml": {
                                "modified_file_name": "mets.xml",
                                "file_role": "DOCUMENTATION",
                                "object_role": "DOCUMENTATION",
                                "object_osn": "ETD_DOCUMENTATION_gsd_2021-05_PQ_28542548",
                                "file_osn": "ETD_DOCUMENTATION_gsd_2021-05_PQ_28542548_1"
                            },
                            "setup_2E592954-F85C-11EA-ABB1-E61AE629DA94.pdf": {
                                "modified_file_name": "setup_2E592954-F85C-11EA-ABB1-E61AE629DA94_.pdf",
                                "file_role": "LICENSE",
                                "object_role": "LICENSE",
                                "object_osn": "ETD_LICENSE_gsd_2021-05_PQ_28542548",
                                "file_osn": "ETD_LICENSE_gsd_2021-05_PQ_28542548_1"
                            },
                            "GIF_01_SlabShift.gif": {
                                "modified_file_name": "GIF_01_SlabShift.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_1",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_1_1"
                            },
                            "GIF_02_Facade1NE.gif": {
                                "modified_file_name": "GIF_02_Facade1NE.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_2",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_2_1"
                            },
                            "GIF_03_Facade2SW.gif": {
                                "modified_file_name": "GIF_03_Facade2SW.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_3",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_3_1"
                            },
                            "GIF_04_Room_1.Gar.gif": {
                                "modified_file_name": "GIF_04_Room_1.Gar.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_4",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_4_1"
                            },
                            "GIF_05_Room_2.TwoLiv.gif": {
                                "modified_file_name": "GIF_05_Room_2.TwoLiv.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_5",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_5_1"
                            }
                        }}
    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc, supplemental_deposit_data)
    assert (expected_batch_dir == batch_dir)
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_THESIS_gsd_2021-05_PQ_28542548", 
                                       "document", "20210524_Thesis_Archival_Submission_JB_Signed.pdf"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_DOCUMENTATION_gsd_2021-05_PQ_28542548", 
                                       "text", "mets.xml"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_THESIS_gsd_2021-05_PQ_28542548", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_DOCUMENTATION_gsd_2021-05_PQ_28542548", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_LICENSE_gsd_2021-05_PQ_28542548", 
                                       "document", "setup_2E592954-F85C-11EA-ABB1-E61AE629DA94_.pdf"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_LICENSE_gsd_2021-05_PQ_28542548", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_1", 
                                       "image", "GIF_01_SlabShift.gif"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_1", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_2", 
                                       "image", "GIF_02_Facade1NE.gif"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_2", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_3", 
                                       "image", "GIF_03_Facade2SW.gif"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_3", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_4", 
                                       "image", "GIF_04_Room_1.Gar.gif"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_4", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_5", 
                                       "image", "GIF_05_Room_2.TwoLiv.gif"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_5", 
                                        "mapping.txt"))
    
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))
    shutil.rmtree(os.path.join(loc, "extracted"))
    
def test_translate_etd_submission_opaque_image():
    '''Formats the directory and verifies that all files ended up where they should be'''
    loc = "/home/appuser/tests/data/etd-submission-opaque-image"
    expected_batch_dir = os.path.join(loc, os.path.basename(loc) + "-batch")

    supplemental_deposit_data = {"alma_id": "99156631569803941",
              "pq_id": "28963877",
              "dash_id": "dash1234",
              "ownerCode": "HUL.TEST",
              "urnAuthorityPath": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "urnAuthorityPath": "HUL.TEST",
              "file_info": {"Alfred_S_MArchI_F21 Thesis.pdf": {
                                "modified_file_name": "Alfred_S_MArchI_F21_Thesis.pdf",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS",
                                "object_osn": "ETD_THESIS_gsd_2022-05_PQ_28963877",
                                "file_osn": "ETD_THESIS_gsd_2022-05_PQ_28963877_1"
                            },
                            "mets.xml": {
                                "modified_file_name": "mets.xml",
                                "file_role": "DOCUMENTATION",
                                "object_role": "DOCUMENTATION",
                                "object_osn": "ETD_DOCUMENTATION_gsd_2022-05_PQ_28963877",
                                "file_osn": "ETD_DOCUMENTATION_gsd_2022-05_PQ_28963877_1"
                            },
                            "setup_2E592954-F85C-11EA-ABB1-E61AE629DA94.pdf": {
                                "modified_file_name": "setup_2E592954-F85C-11EA-ABB1-E61AE629DA94.pdf",
                                "file_role": "LICENSE",
                                "object_role": "LICENSE",
                                "object_osn": "ETD_LICENSE_gsd_2022-05_PQ_28963877",
                                "file_osn": "ETD_LICENSE_gsd_2022-05_PQ_28963877_1"
                            },
                            "Plan Gifs.zip": {
                                "modified_file_name": "Plan_Gifs.zip",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_1",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_1_1"
                            },
                            "Notation Gifs.zip": {
                                "modified_file_name": "Notation_Gifs.zip",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_2",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_2_1"
                            },
                            "Dance Gifs.zip": {
                                "modified_file_name": "Dance_Gifs.zip",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_3",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_3_1"
                            },
                            "Alfred_S_Model gif.gif": {
                                "modified_file_name": "Alfred_S_Model_gif.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_4",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_4_1"
                            }
                        }}
    etd_translate_svc = ETDTranslateDataStructureService()
    batch_dir = etd_translate_svc.translate_data_structure(loc, supplemental_deposit_data)
    assert (expected_batch_dir == batch_dir)
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_THESIS_gsd_2022-05_PQ_28963877", 
                                       "document", "Alfred_S_MArchI_F21_Thesis.pdf"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_DOCUMENTATION_gsd_2022-05_PQ_28963877", 
                                       "text", "mets.xml"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_THESIS_gsd_2022-05_PQ_28963877", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_DOCUMENTATION_gsd_2022-05_PQ_28963877", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_LICENSE_gsd_2022-05_PQ_28963877", 
                                       "document", "setup_2E592954-F85C-11EA-ABB1-E61AE629DA94.pdf"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_LICENSE_gsd_2022-05_PQ_28963877", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_1", 
                                       "content", "Plan_Gifs.zip"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_1", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_2", 
                                       "content", "Notation_Gifs.zip"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_2", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_3", 
                                       "content", "Dance_Gifs.zip"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_3", 
                                        "mapping.txt"))
    assert os.path.exists(os.path.join(batch_dir, 
                                       "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_4", 
                                       "image", "Alfred_S_Model_gif.gif"))
    assert os.path.exists(os.path.join(loc, "_aux", os.path.basename(batch_dir),
                                       "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_4", 
                                        "mapping.txt"))
    cleanup_batch_dirs(batch_dir, os.path.join(loc, "_aux"), os.path.join(loc, "project.conf"))
    shutil.rmtree(os.path.join(loc, "extracted"))

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