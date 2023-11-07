import pytest, sys, os.path, shutil
sys.path.append('app')
from batch_builder_service.dataverse_batch_builder_service import DataverseBatchBuilderService 
from batch_builder_service.epadd_batch_builder_service import EpaddBatchBuilderService
from batch_builder_service.etd_batch_builder_service import ETDBatchBuilderService 

dvn_project_path = "/home/appuser/tests/data/samplepreparedprojects/doi-translation-service-test"
epadd_project_path = "/home/appuser/tests/data/samplepreparedprojects/epadd-test"
epadd_with_mods_project_path = "/home/appuser/tests/data/samplepreparedprojects/epadd-test-with-mods"
bb_script_name = os.getenv("BB_SCRIPT_NAME")
dvn_batch_name ="doi-translation-service-test-batch" 
epadd_batch_name = "epadd-test-batch"
epadd_with_mods_batch_name = "epadd-test-with-mods-batch"

def test_build_basic_command():
    '''Verifies that the build command returns properly'''
    dvn_bb_service = DataverseBatchBuilderService()
    command = dvn_bb_service.build_command(dvn_project_path, dvn_batch_name, {})
    assert command == "sh {} -a build -p {} -b {}".format(bb_script_name, dvn_project_path, dvn_batch_name)
 
def test_dvn_build_command_with_overrides():
    '''Verifies that the build command returns properly'''
     
    supplemental_data = {"accessFlag": "N",
              "contentModel": "opaque",
              "depositingSystem": "Harvard Dataverse",
              "firstGenerationInDrs": "yes",
              "objectRole": "CG:DATASET",
              "usageClass": "LOWUSE",
              "storageClass": "AR",
              "ownerCode": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "resourceNamePattern": "{n}",
              "urnAuthorityPath": "HUL.TEST",
              "depositAgent": "dimsdts1",
              "depositAgentEmail": "DTS@HU.onmicrosoft.com",
              "successEmail": "winner@mailinator.com",
              "failureEmail": "loser@mailinator.com",
              "successMethod": "dropbox",
              "adminCategory": "http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/27186"}
     
     
    bb_script_name = os.getenv("BB_SCRIPT_NAME")
         
    dvn_bb_service = DataverseBatchBuilderService()
    command = dvn_bb_service.build_command(dvn_project_path, dvn_batch_name, supplemental_data)
     
    overridestring = "-batchprop \"successEmail=winner@mailinator.com,failureEmail=loser@mailinator.com,successMethod=dropbox,depositAgent=dimsdts1,depositAgentEmail=DTS@HU.onmicrosoft.com\""
    overridestring += " -objectprop \"doi-translation-service-test::ownerCode=HUL.TEST,billingCode=HUL.TEST.BILL_0001,resourceNamePattern={n},urnAuthorityPath=HUL.TEST,accessFlag=N,adminCategory=http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/27186,role=CG_DATASET;\"" 
    overridestring += " -dirprop \"doi-translation-service-test::content::isFirstGenerationInDrs=yes,usageClass=LOWUSE,fileStorageClass=AR;"
    overridestring += "doi-translation-service-test::documentation::isFirstGenerationInDrs=yes,usageClass=LOWUSE,fileStorageClass=AR\""
    assert command == "sh {} -a build -p {} -b {} {}".format(bb_script_name, dvn_project_path, dvn_batch_name, overridestring)
     
 
def test_dvn_run_batch_builder_basic():
     dvn_bb_service = DataverseBatchBuilderService()
     dvn_bb_service.process_batch(dvn_project_path, dvn_batch_name, {})   
     expected_batch_file = os.path.join(dvn_project_path, dvn_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(dvn_project_path, dvn_batch_name, os.path.basename(dvn_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)  
     cleanup_created_files(expected_batch_file, expected_descriptor_file)   
      
def test_dvn_run_batch_builder_with_overrides():
     supplemental_data = {"accessFlag": "N",
               "contentModel": "opaque",
               "depositingSystem": "Harvard Dataverse",
               "firstGenerationInDrs": "yes",
               "objectRole": "CG:DATASET",
               "usageClass": "LOWUSE",
               "storageClass": "AR",
               "ownerCode": "HUL.TEST",
               "resourceNamePattern": "{n}",
               "urnAuthorityPath": "HUL.TEST",
               "depositAgent": "dimsdts1",
               "depositAgentEmail": "DTS@HU.onmicrosoft.com",
               "successEmail": "winner@mailinator.com",
               "failureEmail": "loser@mailinator.com",
               "successMethod": "dropbox",
               "adminCategory": "http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/27186"}

     dvn_bb_service = DataverseBatchBuilderService()
     dvn_bb_service.process_batch(dvn_project_path, dvn_batch_name, supplemental_data)   
     expected_batch_file = os.path.join(dvn_project_path, dvn_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(dvn_project_path, dvn_batch_name, os.path.basename(dvn_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)     
     cleanup_created_files(expected_batch_file, expected_descriptor_file) 
     
def test_dvm_run_batch_builder_basic_doc_only():
     project_path_no_content="/home/appuser/tests/data/samplepreparedprojects/doi-translation-service-test-doc-only"
     dvn_bb_service = DataverseBatchBuilderService()
     dvn_bb_service.process_batch(project_path_no_content, dvn_batch_name, {})   
     expected_batch_file = os.path.join(project_path_no_content, dvn_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(project_path_no_content, dvn_batch_name, os.path.basename(dvn_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)  
     cleanup_created_files(expected_batch_file, expected_descriptor_file) 
     
def test_epadd_run_batch_builder_basic():
     epadd_bb_service = EpaddBatchBuilderService()
     epadd_bb_service.process_batch(epadd_project_path, epadd_batch_name, {})   
     expected_batch_file = os.path.join(epadd_project_path, epadd_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(epadd_project_path, epadd_batch_name, os.path.basename(epadd_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)  
     cleanup_created_files(expected_batch_file, expected_descriptor_file) 
     extracted_dir = os.path.join(epadd_project_path, "extracted")  
     shutil.rmtree(extracted_dir)
      
def test_epadd_run_batch_builder_with_overrides():
     supplemental_data = {"accessFlag": "N",
               "contentModel": "opaque container",
               "depositingSystem": "ePADD",
               "firstGenerationInDrs": "yes",
               "objectRole": "CG:EMAIL",
               "usageClass": "LOWUSE",
               "storageClass": "AR",
               "ownerCode": "HUL.TEST",
               "resourceNamePattern": "{n}",
               "urnAuthorityPath": "HUL.TEST",
               "depositAgent": "dimsdts1",
               "depositAgentEmail": "DTS@HU.onmicrosoft.com",
               "successEmail": "winner@mailinator.com",
               "failureEmail": "loser@mailinator.com",
               "successMethod": "dropbox",
               "adminCategory": "http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/27186"}
     epadd_bb_service = EpaddBatchBuilderService()
     epadd_bb_service.process_batch(epadd_project_path, epadd_batch_name, supplemental_data)   
     expected_batch_file = os.path.join(epadd_project_path, epadd_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(epadd_project_path, epadd_batch_name, os.path.basename(epadd_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)     
     cleanup_created_files(expected_batch_file, expected_descriptor_file) 
     extracted_dir = os.path.join(epadd_project_path, "extracted")  
     shutil.rmtree(extracted_dir)

def test_epadd_build_command_with_overrides():
    '''Verifies that the build command returns properly'''
     
    supplemental_data = {"accessFlag": "N",
              "contentModel": "opaque",
              "depositingSystem": "ePADD",
              "firstGenerationInDrs": "yes",
              "objectRole": "CG:EMAIL",
              "usageClass": "LOWUSE",
              "storageClass": "AR",
              "ownerCode": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "resourceNamePattern": "{n}",
              "urnAuthorityPath": "HUL.TEST",
              "depositAgent": "dimsdts1",
              "depositAgentEmail": "DTS@HU.onmicrosoft.com",
              "successEmail": "winner@mailinator.com",
              "failureEmail": "loser@mailinator.com",
              "successMethod": "dropbox",
              "adminCategory": "http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/27186",
              "embargoBasis": "Harvard policy"}
     
     
    bb_script_name = os.getenv("BB_SCRIPT_NAME")
         
    epadd_bb_service = EpaddBatchBuilderService()
    command = epadd_bb_service.build_command(epadd_with_mods_project_path, epadd_with_mods_batch_name, supplemental_data)
    print(command)
    overridestring = "-batchprop \"successEmail=winner@mailinator.com,failureEmail=loser@mailinator.com,successMethod=dropbox,depositAgent=dimsdts1,depositAgentEmail=DTS@HU.onmicrosoft.com\""
    overridestring += " -objectprop \"epadd-test-with-mods::ownerCode=HUL.TEST,billingCode=HUL.TEST.BILL_0001,resourceNamePattern={n},urnAuthorityPath=HUL.TEST,accessFlag=N,adminCategory=http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/27186,role=CG_EMAIL," 
    overridestring += "identifier=eas-0001,titleInfoTitle=EAS Project Email Collection,abstract=Scope and content: EAS Test Scope and Content.Description: EAS Test Email Description.,Format version: MBOX version 1.2.13.Format name: MBOX.Overall unique attachment count: 2.,originInfoDateCreated=2012-05-16/2020-12-07,embargoBasis=Harvard policy,embargoGrantStart=2023-03-15,embargoDuration=2,embargoDurationUnit=years;\""
    overridestring += " -dirprop \"epadd-test-with-mods::container::isFirstGenerationInDrs=yes,usageClass=LOWUSE,fileStorageClass=AR\""
    assert command == "sh {} -a build -p {} -b {} {}".format(bb_script_name, epadd_with_mods_project_path, epadd_with_mods_batch_name, overridestring)
 

def test_epadd_with_mods_run_batch_builder_with_overrides():
     supplemental_data = {"accessFlag": "N",
               "contentModel": "opaque container",
               "depositingSystem": "ePADD",
               "firstGenerationInDrs": "yes",
               "objectRole": "CG:EMAIL",
               "usageClass": "LOWUSE",
               "storageClass": "AR",
               "ownerCode": "HUL.TEST",
               "resourceNamePattern": "{n}",
               "urnAuthorityPath": "HUL.TEST",
               "depositAgent": "dimsdts1",
               "depositAgentEmail": "DTS@HU.onmicrosoft.com",
               "successEmail": "winner@mailinator.com",
               "failureEmail": "loser@mailinator.com",
               "successMethod": "dropbox",
               "adminCategory": "http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/27186",
               "embargoBasis": "Harvard policy"}
     epadd_bb_service = EpaddBatchBuilderService()
     epadd_bb_service.process_batch(epadd_with_mods_project_path, epadd_with_mods_batch_name, supplemental_data)   
     expected_batch_file = os.path.join(epadd_with_mods_project_path, epadd_with_mods_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(epadd_with_mods_project_path, epadd_with_mods_batch_name, os.path.basename(epadd_with_mods_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)     
     cleanup_created_files(expected_batch_file, expected_descriptor_file)     

def test_etd_run_batch_builder_images():
     file_info = {"file_info": {"20210524_Thesis Archival Submission_JB Signed.pdf": {
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
                            },
                            "GIF_06_Room_3.Gym&Lau.gif": {
                                "modified_file_name": "GIF_06_Room_3.Gym_Lau.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_6",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_6_1"
                            },
                            "GIF_07_Room_4.Lib&Sto.gif": {
                                "modified_file_name": "GIF_07_Room_4.Lib_Sto.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_7",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_7_1"
                            },
                            "GIF_08_Room_5.KitDinRes.gif": {
                                "modified_file_name": "GIF_08_Room_5.KitDinRes.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_8",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_8_1"
                            },
                            "GIF_09_Room_6.BedClus1.gif": {
                                "modified_file_name": "GIF_09_Room_6.BedClus1.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_9",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_9_1"
                            },
                            "GIF_10_Room_7.BedClus2.gif": {
                                "modified_file_name": "GIF_10_Room_7.BedClus2.gif",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_10",
                                "file_osn": "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_10_1"
                            }
                        }}
     supplemental_data = {"alma_id": "99156631569803941",
              "pq_id": "1234",
              "dash_id": "dash1234",
              "ownerCode": "HUL.TEST",
              "urnAuthorityPath": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "urnAuthorityPath": "HUL.TEST",
              "file_info": file_info}
     
     etd_batch_name = "etd-images-batch"
     etd_project_path = "/home/appuser/tests/data/samplepreparedprojects/etd-images"
     etd_bb_service = ETDBatchBuilderService()
     command = etd_bb_service.process_batch(etd_project_path, etd_batch_name, supplemental_data) 
     print(command) 
     expected_batch_file = os.path.join(etd_project_path, etd_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_thesis_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_THESIS_gsd_2021-05_PQ_28542548", "descriptor.xml")
     expected_license_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_LICENSE_gsd_2021-05_PQ_28542548", "descriptor.xml")
     expected_doc_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_DOCUMENTATION_gsd_2021-05_PQ_28542548", "descriptor.xml")
     expected_gif_descriptor_file_1 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_1", "descriptor.xml")
     expected_gif_descriptor_file_2 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_2", "descriptor.xml")
     expected_gif_descriptor_file_3 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_3", "descriptor.xml")
     expected_gif_descriptor_file_4 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_4", "descriptor.xml")
     expected_gif_descriptor_file_5 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_5", "descriptor.xml")
     expected_gif_descriptor_file_6 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_6", "descriptor.xml")
     expected_gif_descriptor_file_7 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_7", "descriptor.xml")
     expected_gif_descriptor_file_8 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_8", "descriptor.xml")
     expected_gif_descriptor_file_9 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_9", "descriptor.xml")
     expected_gif_descriptor_file_10 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2021-05_PQ_28542548_10", "descriptor.xml")
     assert os.path.exists(expected_thesis_descriptor_file)  
     assert os.path.exists(expected_license_descriptor_file)  
     assert os.path.exists(expected_doc_descriptor_file)  
     assert os.path.exists(expected_gif_descriptor_file_1)  
     assert os.path.exists(expected_gif_descriptor_file_2)  
     assert os.path.exists(expected_gif_descriptor_file_3)  
     assert os.path.exists(expected_gif_descriptor_file_4)  
     assert os.path.exists(expected_gif_descriptor_file_5)  
     assert os.path.exists(expected_gif_descriptor_file_6)  
     assert os.path.exists(expected_gif_descriptor_file_7)  
     assert os.path.exists(expected_gif_descriptor_file_8)  
     assert os.path.exists(expected_gif_descriptor_file_9)  
     assert os.path.exists(expected_gif_descriptor_file_10)  
     cleanup_created_files(expected_batch_file, expected_thesis_descriptor_file) 
     os.remove(expected_license_descriptor_file)
     os.remove(expected_doc_descriptor_file)
     os.remove(expected_gif_descriptor_file_1)  
     os.remove(expected_gif_descriptor_file_2)  
     os.remove(expected_gif_descriptor_file_3)  
     os.remove(expected_gif_descriptor_file_4)  
     os.remove(expected_gif_descriptor_file_5)  
     os.remove(expected_gif_descriptor_file_6)  
     os.remove(expected_gif_descriptor_file_7)  
     os.remove(expected_gif_descriptor_file_8)  
     os.remove(expected_gif_descriptor_file_9)  
     os.remove(expected_gif_descriptor_file_10)  
     
def test_etd_run_batch_builder_opaque_image():
     file_info = {"file_info": {"Alfred_S_MArchI_F21 Thesis.pdf": {
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
     supplemental_data = {"alma_id": "99156631569803941",
              "pq_id": "1234",
              "dash_id": "dash1234",
              "ownerCode": "HUL.TEST",
              "urnAuthorityPath": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "urnAuthorityPath": "HUL.TEST",
              "file_info": file_info}
     
     etd_batch_name = "etd-opaque-image-batch"
     etd_project_path = "/home/appuser/tests/data/samplepreparedprojects/etd-opaque-image"
     etd_bb_service = ETDBatchBuilderService()
     command = etd_bb_service.process_batch(etd_project_path, etd_batch_name, supplemental_data) 
     print(command) 
     expected_batch_file = os.path.join(etd_project_path, etd_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_thesis_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_THESIS_gsd_2022-05_PQ_28963877", "descriptor.xml")
     expected_license_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_LICENSE_gsd_2022-05_PQ_28963877", "descriptor.xml")
     expected_doc_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_DOCUMENTATION_gsd_2022-05_PQ_28963877", "descriptor.xml")
     expected_gif_descriptor_file_1 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_1", "descriptor.xml")
     expected_gif_descriptor_file_2 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_2", "descriptor.xml")
     expected_gif_descriptor_file_3 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_3", "descriptor.xml")
     expected_gif_descriptor_file_4 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_gsd_2022-05_PQ_28963877_4", "descriptor.xml")
     assert os.path.exists(expected_thesis_descriptor_file)  
     assert os.path.exists(expected_license_descriptor_file)  
     assert os.path.exists(expected_doc_descriptor_file)  
     assert os.path.exists(expected_gif_descriptor_file_1)  
     assert os.path.exists(expected_gif_descriptor_file_2)  
     assert os.path.exists(expected_gif_descriptor_file_3)  
     assert os.path.exists(expected_gif_descriptor_file_4)  
     cleanup_created_files(expected_batch_file, expected_thesis_descriptor_file) 
     os.remove(expected_license_descriptor_file)
     os.remove(expected_doc_descriptor_file)
     os.remove(expected_gif_descriptor_file_1)  
     os.remove(expected_gif_descriptor_file_2)  
     os.remove(expected_gif_descriptor_file_3)  
     os.remove(expected_gif_descriptor_file_4)

def test_etd_run_batch_builder_audio():
     osn_unique_appender = "gsd_2023-05_PQ_28542548"
     file_info = {"file_info": {"MLA Thesis_Auger_Catherine_May2023.pdf": {
                                "modified_file_name": "MLA_Thesis_Auger_Catherine_May2023.pdf",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS",
                                "object_osn": "ETD_THESIS_" + osn_unique_appender,
                                "file_osn": "ETD_THESIS_" + osn_unique_appender + "_1"
                            },
                            "mets.xml": {
                                "modified_file_name": "mets.xml",
                                "file_role": "DOCUMENTATION",
                                "object_role": "DOCUMENTATION",
                                "object_osn": "ETD_DOCUMENTATION_" + osn_unique_appender,
                                "file_osn": "ETD_DOCUMENTATION_" + osn_unique_appender+"_1"
                            },
                            "setup_2E592954-F85C-11EA-ABB1-E61AE629DA94.pdf": {
                                "modified_file_name": "setup_2E592954-F85C-11EA-ABB1-E61AE629DA94.pdf",
                                "file_role": "LICENSE",
                                "object_role": "LICENSE",
                                "object_osn": "ETD_LICENSE_" + osn_unique_appender,
                                "file_osn": "ETD_LICENSE_" + osn_unique_appender+"_1"
                            },
                            "Gamelan_Islam.mp3": {
                                "modified_file_name": "Gamelan_Islam.mp3",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_1",
                                "file_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_1_1"
                            },
                            "Harry Styles.mp3": {
                                "modified_file_name": "Harry_Styles.mp3",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_2",
                                "file_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_2_1"
                            },
                            "Jalan Raya Ubud.mp3": {
                                "modified_file_name": "Jalan_Raya_Ubud.mp3",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_3",
                                "file_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_3_1"
                            },
                            "Kuningan.mp3": {
                                "modified_file_name": "Kuningan.mp3",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_4",
                                "file_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_4_1"
                            },
                            "Monkey Forest.mp3": {
                                "modified_file_name": "Monkey_Forest.mp3",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_5",
                                "file_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_5_1"
                            },
                            "Pasar Goris.mp3": {
                                "modified_file_name": "Pasar_Goris.mp3",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_6",
                                "file_osn": "ETD_SUPPLEMENT_" + osn_unique_appender+"_6_1"
                            },
                            "The Pipe.mp3": {
                                "modified_file_name": "The_Pipe.mp3",
                                "file_role": "ARCHIVAL_MASTER",
                                "object_role": "THESIS_SUPPLEMENT",
                                "object_osn": "ETD_SUPPLEMENT__" + osn_unique_appender + "_7",
                                "file_osn": "ETD_SUPPLEMENT__" + osn_unique_appender + "_7_1"
                            }
                        }}
     supplemental_data = {"alma_id": "99156631569803941",
              "pq_id": "1234",
              "dash_id": "dash1234",
              "ownerCode": "HUL.TEST",
              "urnAuthorityPath": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "urnAuthorityPath": "HUL.TEST",
              "file_info": file_info}
     
     etd_batch_name = "etd-audio-batch"
     etd_project_path = "/home/appuser/tests/data/samplepreparedprojects/etd-audio"
     etd_bb_service = ETDBatchBuilderService()
     command = etd_bb_service.process_batch(etd_project_path, etd_batch_name, supplemental_data) 
     print(command) 
     expected_batch_file = os.path.join(etd_project_path, etd_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_thesis_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_THESIS_" + osn_unique_appender, "descriptor.xml")
     expected_license_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_LICENSE_" + osn_unique_appender, "descriptor.xml")
     expected_doc_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_DOCUMENTATION_" + osn_unique_appender, "descriptor.xml")
     expected_gif_descriptor_file_1 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_" + osn_unique_appender+"_1", "descriptor.xml")
     expected_gif_descriptor_file_2 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_" + osn_unique_appender+"_2", "descriptor.xml")
     expected_gif_descriptor_file_3 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_" + osn_unique_appender+"_3", "descriptor.xml")
     expected_gif_descriptor_file_4 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_" + osn_unique_appender+"_4", "descriptor.xml")
     expected_gif_descriptor_file_5 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_" + osn_unique_appender+"_5", "descriptor.xml")
     expected_gif_descriptor_file_6 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_" + osn_unique_appender+"_6", "descriptor.xml")
     expected_gif_descriptor_file_7 = os.path.join(etd_project_path, etd_batch_name, "ETD_SUPPLEMENT_" + osn_unique_appender+"_7", "descriptor.xml")
     assert os.path.exists(expected_thesis_descriptor_file)  
     assert os.path.exists(expected_license_descriptor_file)  
     assert os.path.exists(expected_doc_descriptor_file)  
     assert os.path.exists(expected_gif_descriptor_file_1)  
     assert os.path.exists(expected_gif_descriptor_file_2)  
     assert os.path.exists(expected_gif_descriptor_file_3)  
     assert os.path.exists(expected_gif_descriptor_file_4)  
     assert os.path.exists(expected_gif_descriptor_file_5)  
     assert os.path.exists(expected_gif_descriptor_file_6)  
     assert os.path.exists(expected_gif_descriptor_file_7)  
     cleanup_created_files(expected_batch_file, expected_thesis_descriptor_file) 
     os.remove(expected_license_descriptor_file)
     os.remove(expected_doc_descriptor_file)
     os.remove(expected_gif_descriptor_file_1)  
     os.remove(expected_gif_descriptor_file_2)  
     os.remove(expected_gif_descriptor_file_3)  
     os.remove(expected_gif_descriptor_file_4)  
     os.remove(expected_gif_descriptor_file_5)  
     os.remove(expected_gif_descriptor_file_6)  
     os.remove(expected_gif_descriptor_file_7)  
     
def test_etd_run_batch_builder():
     file_info = {"file_info": {"Harvard_IR_License_-_LAA_for_ETDs_(2020).pdf": {
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
     supplemental_data = {"alma_id": "99156631569803941",
              "pq_id": "1234",
              "dash_id": "dash1234",
              "ownerCode": "HUL.TEST",
              "urnAuthorityPath": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "urnAuthorityPath": "HUL.TEST",
              "file_info": file_info}
     
     etd_batch_name = "etd-test-batch"
     etd_project_path = "/home/appuser/tests/data/samplepreparedprojects/etd-test"
     etd_bb_service = ETDBatchBuilderService()
     command = etd_bb_service.process_batch(etd_project_path, etd_batch_name, supplemental_data) 
     print(command) 
     expected_batch_file = os.path.join(etd_project_path, etd_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_thesis_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_THESIS_dce_2022_PQ_29161227", "descriptor.xml")
     expected_license_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_LICENSE_dce_2022_PQ_29161227", "descriptor.xml")
     expected_doc_descriptor_file = os.path.join(etd_project_path, etd_batch_name, "ETD_DOCUMENTATION_dce_2022_PQ_29161227", "descriptor.xml")
     assert os.path.exists(expected_thesis_descriptor_file)  
     assert os.path.exists(expected_license_descriptor_file)  
     assert os.path.exists(expected_doc_descriptor_file)  
     cleanup_created_files(expected_batch_file, expected_thesis_descriptor_file) 
     os.remove(expected_license_descriptor_file)
     os.remove(expected_doc_descriptor_file)
    
def cleanup_created_files(batch_path, descriptor_path):
    '''Removes the newly created batch and descriptor files'''
    try:
        os.remove(batch_path)
        os.remove(descriptor_path)
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))