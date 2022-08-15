import os, os.path, logging, shutil, glob

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
    
    extracted_path = os.path.join(extracted_files_dir, extracted_files[0])
    
    hascontent = __handle_content_files(object_dir, extracted_path)
    
    __copy_project_conf(package_path)
    __copy_object_xml_and_rename_object(aux_object_dir, hascontent)
    
    __handle_documentation_files(object_dir, extracted_path)
                
    return batch_dir

def __handle_content_files(object_dir, extracted_path):
    content_list_string = os.getenv("CONTENT_FILES_AND_DIRS", "")
    content_list = content_list_string.split(",")
    
    hascontent = False
    for item in content_list:
        item_path = os.path.join(extracted_path, item)
    
         #If there is a wildcard, then move all under that item
        if ("*" in item):
            for file in glob.glob(r'{}'.format(item_path)):
                shutil.copy2(file, os.path.join(doc_path, file)) 
        elif os.path.exists(item_path):
            logging.debug("Moving content for {}".format(item_path))
            content_path = os.path.join(object_dir, "content")
            if not os.path.exists(content_path):
                os.mkdir(content_path)
            #If it is a path to a file, move the file
            if (os.path.isfile(item_path)): 
                print("Moving {} to {}".format(item_path, os.path.join(dest_dir, os.path.basename(item_path))))
                logging.debug("Moving {} to {}".format(item_path, os.path.basename(item_path)))
                shutil.copy2(item_path, os.path.join(dest_dir, os.path.basename(item_path)))
            #If it is a directory, use the recursive call
            else:
                __move_files(item_path, item_path, content_path)
            hascontent = True
        else:
            hascontent = False
            logging.debug("No contents exist in {}".format(dir))
    
    return hascontent


def __move_files(root_dir, source, dest_dir):
    '''This method actually copies the files from source to destination rather than
    moves them to preserve the original structure and to aid in error handling'''
    if (os.path.isfile(source)):
        print("Moving {} to {}".format(os.path.join(root_dir, source), os.path.join(dest_dir, source)))
        logging.debug("Moving {} to {}".format(os.path.join(root_dir, source), os.path.join(dest_dir, source)))
        shutil.copy2(os.path.join(root_dir, source), os.path.join(dest_dir, os.path.basename(source)))
    else:
        for root, subdirs, files in os.walk(source):
            for subdir in subdirs:
                print("Subdir {} to {}".format(os.path.join(root, subdir), dest_dir))
                __move_files(os.path.join(root, subdir), os.path.join(root, subdir), dest_dir)
            for filename in files:
                print("File {} to {}".format(os.path.join(root, filename), os.path.join(dest_dir, filename)))
                shutil.copy2(os.path.join(root, filename), os.path.join(dest_dir, filename))

def __handle_documentation_files(object_dir, extracted_path):
    documentation_list_string = os.getenv("DOCUMENTATION_FILES_AND_DIRS", "")
    documentation_list = documentation_list_string.split(",")
    
    for item in documentation_list:
        item_path = os.path.join(extracted_path, item)
        #If there is a wildcard, then move all under that item
        if ("*" in item):
            print("Wildcard {} ".format(item_path))
            print(glob.glob('{}'.format(item_path)))
            for file in glob.glob('{}'.format(item_path)):
                print("file: {}".format(file))
                shutil.copy2(os.path.join(item_path,file), os.path.join(doc_path, file)) 
        elif os.path.exists(item_path):
            doc_path = os.path.join(object_dir, "documentation")
            if not os.path.exists(doc_path):
                os.mkdir(doc_path)
                
            #If it is a path to a file, move the file
            if (os.path.isfile(item_path)): 
                print("Moving {} to {}".format(item_path, os.path.join(doc_path, os.path.basename(item_path))))
                logging.debug("Moving {} to {}".format(item_path, os.path.basename(item_path)))
                shutil.copy2(item_path, os.path.join(doc_path, os.path.basename(item_path)))
            #If it is a directory, use the recursive call
            else:
                __move_files(item_path, item_path, doc_path)
    

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
    
   
