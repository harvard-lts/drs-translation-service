import os, os.path, logging, shutil

logfile=os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel)

def translate_data_structure(package_path):
    #Project name is the doi-name
    #Batch name doi-name-batch
    batch_name= os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    #Object name is the doi-name
    object_name= os.path.basename(package_path)
    object_dir = os.path.join(batch_dir, object_name)
    
    aux_object_dir = os.path.join(package_path, "_aux", batch_name, object_name)
    os.makedirs(aux_object_dir, exist_ok=True)
    
    #Make batch dir and object dir
    os.makedirs(object_dir, exist_ok=True)
    #/package_path/extracted
    extracted_files_dir = os.path.join(package_path, "extracted")
    #/package_path/extracted/unzippeddir
    extracted_files = os.listdir(extracted_files_dir)
    if (len(extracted_files) != 1):
        raise Exception("{} directory expected 1 item but found {}".format(extracted_files_dir, len(extracted_files)))    
    
    data_dir = os.path.join(extracted_files_dir, extracted_files[0], "data")
    
    if os.path.exists(data_dir):
        logging.debug("Moving content for {}".format(data_dir))
        content_path = os.path.join(object_dir, "content")
        if not os.path.exists(content_path):
            os.mkdir(content_path)
        __move_content_files(data_dir, content_path)
        hascontent = True
    else:
        hascontent = False
        logging.debug("No contents exist in {}".format(data_dir))
    
    __copy_project_conf(package_path)
    __copy_object_xml_and_rename_object(aux_object_dir, hascontent)
        
    doc_path = os.path.join(object_dir, "documentation")
    if not os.path.exists(doc_path):
        os.mkdir(doc_path)
    __move_document_files(os.path.join(extracted_files_dir, extracted_files[0]), doc_path)
    
    #Move the DDI file (ends in XML)
    for f in os.listdir(package_path):
        if os.path.isfile(os.path.join(package_path, f)):
            if f.endswith(".xml"):
                __move_files(package_path, os.path.join(package_path, f), doc_path)
                
    return batch_dir

def __move_content_files(data_dir, content_path):
    __move_files(data_dir, data_dir, content_path)
    return True

def __move_files(root, source, dest_dir):
    '''This method actually copies the files from source to destination rather than
    moves them to preserve the original structure and to aid in error handling'''
    if (os.path.isfile(source)):
        print("Moving {} to {}".format(os.path.join(root, source), os.path.join(dest_dir, source)))
        logging.debug("Moving {} to {}".format(os.path.join(root, source), os.path.join(dest_dir, source)))
        shutil.copy2(os.path.join(root, source), os.path.join(dest_dir, os.path.basename(source)))
    else:
        for root, subdirs, files in os.walk(source):
            for subdir in subdirs:
                print("Subdir {} to {}".format(os.path.join(root, subdir), dest_dir))
                __move_files(os.path.join(root, subdir), os.path.join(root, subdir), dest_dir)
            for filename in files:
                print("File {} to {}".format(os.path.join(root, filename), os.path.join(dest_dir, filename)))
                shutil.copy2(os.path.join(root, filename), os.path.join(dest_dir, filename))

def __move_document_files(extracted_dir, doc_path):
    #Move the files in the extracted directory (bag-it info, manifest info)
    for f in os.listdir(extracted_dir):
        print(os.path.join(extracted_dir, f))
        if os.path.isfile(os.path.join(extracted_dir, f)):
            __move_files(extracted_dir, os.path.join(extracted_dir, f), doc_path)
        
    md_dir = os.path.join(extracted_dir, "metadata")
    if os.path.exists(md_dir):
        logging.debug("Moving docs for {}".format(md_dir))
        #Move the files in the metadata directory
        __move_files(md_dir, md_dir, doc_path)
    else:
        logging.debug("No docs exist in {}".format(md_dir))
    md_dir = os.path.join(extracted_dir, "metadata")
    return True

def __copy_project_conf(project_dir):
    project_conf = os.getenv("PROJECT_CONF_TEMPLATE")
    shutil.copy2(project_conf, os.path.join(project_dir, "project.conf"))

def __copy_object_xml_and_rename_object(aux_object_dir, hascontent):
    
    if not hascontent:
        object_xml_template = os.getenv("OBJECT_XML_DOC_ONLY_TEMPLATE")
    else:
        object_xml_template = os.getenv("OBJECT_XML_TEMPLATE")
        
    object_xml = os.path.join(aux_object_dir, "object.xml")
    object_name = os.path.basename(aux_object_dir)
    
    # Read in the template file
    with open(object_xml_template, 'r') as file:
        filedata = file.read()

    # Replace the object name
    filedata = filedata.replace('OBJECT_NAME', object_name)
    
    # Write the object.xml file out in the aux directory
    with open(object_xml, 'w') as file:
      file.write(filedata)
    
   
