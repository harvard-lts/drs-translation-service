import pytest, sys, os.path, shutil
sys.path.append('app')
from translation_service.batch_builder_assistant import BatchBuilderAssistant 

batch_builder_assistant = BatchBuilderAssistant()
dvn_project_path = "/home/appuser/tests/data/samplepreparedprojects/doi-translation-service-test"
epadd_project_path = "/home/appuser/tests/data/samplepreparedprojects/epadd-test"
epadd_with_mods_project_path = "/home/appuser/tests/data/samplepreparedprojects/epadd-test-with-mods"
bb_script_name = os.getenv("BB_SCRIPT_NAME")
dvn_batch_name ="doi-translation-service-test-batch" 
epadd_batch_name = "epadd-test-batch"
epadd_with_mods_batch_name = "epadd-test-with-mods-batch"

def test_build_basic_command():
    '''Verifies that the build command returns properly'''
    command = batch_builder_assistant.build_command(dvn_project_path, dvn_batch_name, {}, "Dataverse")
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
         
    command = batch_builder_assistant.build_command(dvn_project_path, dvn_batch_name, supplemental_data, "Dataverse")
     
    overridestring = "-batchprop \"successEmail=winner@mailinator.com,failureEmail=loser@mailinator.com,successMethod=dropbox,depositAgent=dimsdts1,depositAgentEmail=DTS@HU.onmicrosoft.com\""
    overridestring += " -objectprop \"doi-translation-service-test::ownerCode=HUL.TEST,billingCode=HUL.TEST.BILL_0001,resourceNamePattern={n},urnAuthorityPath=HUL.TEST,accessFlag=N,adminCategory=http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/27186,role=CG_DATASET;\"" 
    overridestring += " -dirprop \"doi-translation-service-test::content::isFirstGenerationInDrs=yes,usageClass=LOWUSE,fileStorageClass=AR;"
    overridestring += "doi-translation-service-test::documentation::isFirstGenerationInDrs=yes,usageClass=LOWUSE,fileStorageClass=AR\""
    assert command == "sh {} -a build -p {} -b {} {}".format(bb_script_name, dvn_project_path, dvn_batch_name, overridestring)
     
 
def test_dvn_run_batch_builder_basic():
     batch_builder_assistant.process_batch(dvn_project_path, dvn_batch_name, {}, "Dataverse")   
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

     batch_builder_assistant.process_batch(dvn_project_path, dvn_batch_name, supplemental_data, "Dataverse")   
     expected_batch_file = os.path.join(dvn_project_path, dvn_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(dvn_project_path, dvn_batch_name, os.path.basename(dvn_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)     
     cleanup_created_files(expected_batch_file, expected_descriptor_file) 
     
def test_dvm_run_batch_builder_basic_doc_only():
     project_path_no_content="/home/appuser/tests/data/samplepreparedprojects/doi-translation-service-test-doc-only"
     batch_builder_assistant.process_batch(project_path_no_content, dvn_batch_name, {}, "Dataverse")   
     expected_batch_file = os.path.join(project_path_no_content, dvn_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(project_path_no_content, dvn_batch_name, os.path.basename(dvn_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)  
     cleanup_created_files(expected_batch_file, expected_descriptor_file) 
     
def test_epadd_run_batch_builder_basic():
     batch_builder_assistant.process_batch(epadd_project_path, epadd_batch_name, {}, "ePADD")   
     expected_batch_file = os.path.join(epadd_project_path, epadd_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(epadd_project_path, epadd_batch_name, os.path.basename(epadd_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)  
     cleanup_created_files(expected_batch_file, expected_descriptor_file)   
      
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
     batch_builder_assistant.process_batch(epadd_project_path, epadd_batch_name, supplemental_data, "ePADD")   
     expected_batch_file = os.path.join(epadd_project_path, epadd_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(epadd_project_path, epadd_batch_name, os.path.basename(epadd_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)     
     cleanup_created_files(expected_batch_file, expected_descriptor_file) 

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
         
    command = batch_builder_assistant.build_command(epadd_with_mods_project_path, epadd_with_mods_batch_name, supplemental_data, "ePADD")
    print(command)
    overridestring = "-batchprop \"successEmail=winner@mailinator.com,failureEmail=loser@mailinator.com,successMethod=dropbox,depositAgent=dimsdts1,depositAgentEmail=DTS@HU.onmicrosoft.com\""
    overridestring += " -objectprop \"epadd-test-with-mods::ownerCode=HUL.TEST,billingCode=HUL.TEST.BILL_0001,resourceNamePattern={n},urnAuthorityPath=HUL.TEST,accessFlag=N,adminCategory=http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/27186,embargoBasis=Harvard policy,role=CG_EMAIL," 
    overridestring += "identifier=eas-0001,titleInfoTitle=EAS Project Email Collection,abstract=Scope and content: EAS Test Scope and Content.Description: EAS Test Email Description.,Format version: MBOX version 1.2.13.Format name: MBOX.Overall unique attachment count: 2.,originInfoDateCreated=2012-05-16/2020-12-07,embargoGrantStart=2023-03-15,embargoDuration=2,embargoDurationUnit=years;\""
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
     batch_builder_assistant.process_batch(epadd_with_mods_project_path, epadd_with_mods_batch_name, supplemental_data, "ePADD")   
     expected_batch_file = os.path.join(epadd_with_mods_project_path, epadd_with_mods_batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(epadd_with_mods_project_path, epadd_with_mods_batch_name, os.path.basename(epadd_with_mods_project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)     
     cleanup_created_files(expected_batch_file, expected_descriptor_file)     
     
    
def cleanup_created_files(batch_path, descriptor_path):
    '''Removes the newly created batch and descriptor files'''
    try:
        os.remove(batch_path)
        os.remove(descriptor_path)
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))