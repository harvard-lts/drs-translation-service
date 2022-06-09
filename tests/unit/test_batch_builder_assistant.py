import pytest, sys, os.path, shutil
sys.path.append('app')
from translation_service.batch_builder_assistant import BatchBuilderAssistant 

batch_builder_assistant = BatchBuilderAssistant()
project_path = "/home/appuser/tests/data/samplepreparedprojects/doi-translation-service-test"
bb_script_name = os.getenv("BB_SCRIPT_NAME")
batch_name ="doi-translation-service-test-batch" 

def test_build_basic_command():
    '''Verifies that the build command returns properly'''
    command = batch_builder_assistant.build_command(project_path, batch_name, {})
    assert command == "sh {} -a build -p {} -b {}".format(bb_script_name, project_path, batch_name)
 
def test_build_command_with_overrides():
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
              "adminCategory": "http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/611"}
     
     
    bb_script_name = os.getenv("BB_SCRIPT_NAME")
         
    command = batch_builder_assistant.build_command(project_path, batch_name, supplemental_data)
     
    overridestring = "-batchprop \"successEmail=winner@mailinator.com,failureEmail=loser@mailinator.com,successMethod=dropbox,depositAgent=dimsdts1,depositAgentEmail=DTS@HU.onmicrosoft.com\""
    overridestring += " -objectprop \"doi-translation-service-test::ownerCode=HUL.TEST,billingCode=HUL.TEST.BILL_0001,resourceNamePattern={n},urnAuthorityPath=HUL.TEST,accessFlag=N,adminCategory=http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/611,role=CG_DATASET;\"" 
    overridestring += " -dirprop \"doi-translation-service-test::content::isFirstGenerationInDrs=yes,usageClass=LOWUSE,fileStorageClass=AR;"
    overridestring += "doi-translation-service-test::documentation::isFirstGenerationInDrs=yes,usageClass=LOWUSE,fileStorageClass=AR\""
    assert command == "sh {} -a build -p {} -b {} {}".format(bb_script_name, project_path, batch_name, overridestring)
     
 
def test_run_batch_builder_basic():
     batch_builder_assistant.process_batch(project_path, batch_name, {})   
     expected_batch_file = os.path.join(project_path, batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(project_path, batch_name, os.path.basename(project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)  
     cleanup_created_files(expected_batch_file, expected_descriptor_file)   
      
def test_run_batch_builder_with_overrides():
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
               "adminCategory": "http://idtest.lib.harvard.edu:10020/wordshack/adminCategory/611"}
     batch_builder_assistant.process_batch(project_path, batch_name, supplemental_data)   
     expected_batch_file = os.path.join(project_path, batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(project_path, batch_name, os.path.basename(project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)     
     cleanup_created_files(expected_batch_file, expected_descriptor_file) 
     
def test_run_batch_builder_basic_doc_only():
     project_path_no_content="/home/appuser/tests/data/samplepreparedprojects/doi-translation-service-test-doc-only"
     batch_builder_assistant.process_batch(project_path_no_content, batch_name, {})   
     expected_batch_file = os.path.join(project_path_no_content, batch_name, "batch.xml")
     assert os.path.exists(expected_batch_file)
     expected_descriptor_file = os.path.join(project_path_no_content, batch_name, os.path.basename(project_path), "descriptor.xml")
     assert os.path.exists(expected_descriptor_file)  
     cleanup_created_files(expected_batch_file, expected_descriptor_file) 
     
    
def cleanup_created_files(batch_path, descriptor_path):
    '''Removes the newly created batch and descriptor files'''
    try:
        os.remove(batch_path)
        os.remove(descriptor_path)
    except OSError as e:
        print("Error in cleanup: %s" % (e.strerror))