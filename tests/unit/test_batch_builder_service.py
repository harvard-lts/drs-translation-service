import pytest, sys, os.path, shutil
sys.path.append('app')
from batch_builder_service.dataverse_batch_builder_service import DataverseBatchBuilderService 
from batch_builder_service.epadd_batch_builder_service import EpaddBatchBuilderService
from batch_builder_service.etd_batch_builder_service import ETDBatchBuilderService 

dvn_project_path = "/home/appuser/tests/data/samplepreparedprojects/doi-translation-service-test"
epadd_project_path = "/home/appuser/tests/data/samplepreparedprojects/epadd-test"
etd_project_path = "/home/appuser/tests/data/samplepreparedprojects/etd-test"
epadd_with_mods_project_path = "/home/appuser/tests/data/samplepreparedprojects/epadd-test-with-mods"
bb_script_name = os.getenv("BB_SCRIPT_NAME")
dvn_batch_name ="doi-translation-service-test-batch" 
epadd_batch_name = "epadd-test-batch"
etd_batch_name = "etd-test-batch"
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
     supplemental_data = {"alma_id": "Alma1234",
              "pq_id": "1234",
              "dash_id": "dash1234",
              "ownerCode": "HUL.TEST",
              "urnAuthorityPath": "HUL.TEST",
              "billingCode": "HUL.TEST.BILL_0001",
              "urnAuthorityPath": "HUL.TEST",
              "file_info": file_info}
     
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